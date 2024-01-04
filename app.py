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
    user_list = []
    for user in users:
        user_data = {
            'id': user.id,
            'lat': user.lat,
            'lon': user.lon,
            'timestamp': user.timestamp.isoformat(),
            'order_id': user.order_id
        }
        user_list.append(user_data)

    return jsonify({"orders": user_list})

@app.route('/dequeue', methods=['GET'])
def dequeue_data():
    data = Users.query.first()

    if data is None:
        return jsonify({"message": "Queue is empty"}), 404

    db.session.delete(data)
    db.session.commit()

    user_data = {
            
        }

    return jsonify({'lat': data.lat,
            'lon': data.lon,
            'timestamp': data.timestamp.isoformat(),
            'order_id': data.order_id}), 200

if __name__ == '__main__':
    
    print(db)
    print("tite")
    app.run(debug=True)
