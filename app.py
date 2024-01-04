from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
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
        driver_name = users_content['driver_name']
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
            'driver_name' : user.driver_name
        }
        user_list.append(user_data)
    return jsonify({"drivers": user_list}), 200

@app.route('/dequeue', methods=['GET'])
def dequeue_data():
    if len(request.args)==0:
        drivers = Users.query.group_by(Users.driver_name).all()
        if drivers is None:
            return jsonify({"message": "Queue is empty"}), 404
        
        user_list = []
        for user in drivers:
            user_data = {
                'lat': user.lat,
                'lon': user.lon,
                'timestamp': user.timestamp.isoformat(),
                'driver_name': user.driver_name
            }
            db.session.delete(user)
            user_list.append(user_data)
        db.session.commit()
        return jsonify({"drivers": user_list})
    
    elif 'users' in request.args:
        print(request.args['users'])
        data = Users.query.filter_by(driver_name=request.args['users']).first()
        if data is None:
            return jsonify({"message": "Queue is empty"}), 404
        
        db.session.delete(data)
        db.session.commit()

        return jsonify({
                'lat': data.lat,
                'lon': data.lon,
                'timestamp': data.timestamp.isoformat(),
                'driver_name': data.driver_name}), 200
    
if __name__ == '__main__':
    app.run(debug=True)
