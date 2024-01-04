from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

from models import Users

with app.app_context():
    db.create_all()

@app.route('/enqueue', methods=['POST', 'GET'])
def enqueue_data():
    users_content = request.args
    print(users_content)
    new_user = Users(
        lat=users_content['lat'],
        lon=users_content['lon'],
        order_id = users_content['order_id']
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Enqueue completed"})

@app.route('/all', methods=['GET'])
def get_all():
    users = Users.query.all()
    if users is None:
        return jsonify({"message": "Queue is empty"}), 404
    
    user_list = []
    for user in users:
        user_data = {
            'id' : user.id,
            'lat' : user.lat,
            'lon' : user.lon,
            'timestamp' : user.timestamp.isoformat(),
            'order_id' : user.order_id
        }
        user_list.append(user_data)
    return jsonify({"drivers": user_list}), 200

@app.route('/dequeue', methods=['GET'])
def dequeue_data():
    if len(request.args)==0:
        drivers = Users.query.group_by(Users.order_id).all()
        if drivers is None:
            return jsonify({"message": "Queue is empty"}), 404
        
        user_list = []
        for user in drivers:
            user_data = {
                'lat': user.lat,
                'lon': user.lon,
                'timestamp': user.timestamp.isoformat(),
                'order_id': user.order_id
            }
            db.session.delete(user)
            user_list.append(user_data)
        db.session.commit()
        return jsonify({"drivers": user_list})
    
    elif 'users' in request.args:
        print(request.args['users'])
        data = Users.query.filter_by(order_id=request.args['users']).first()
        if data is None:
            return jsonify({"message": "Queue is empty"}), 404
        
        db.session.delete(data)
        db.session.commit()

        return jsonify({'lat': data.lat,
                'lon': data.lon,
                'timestamp': data.timestamp.isoformat(),
                'order_id': data.order_id}), 200
    
if __name__ == '__main__':
    app.run(debug=True)
