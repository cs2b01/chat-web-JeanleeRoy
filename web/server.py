from flask import Flask,render_template, request, session, Response, redirect
from sqlalchemy import or_
from database import connector
from model import entities
import time
import json

db = connector.Manager()
engine = db.createEngine()

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/static/<content>')
def static_content(content):
    return render_template(content)


# #---- LOGIN AUTHENTICATION ---------------------------


@app.route('/authenticate', methods = ['POST'])
def authenticate():
    time.sleep(1)
    # 1. Get request
    message = json.loads(request.data)
    username = message['username']
    password = message['password']

    # 2. look in database
    db_session = db.getSession(engine)
    try:
        user = db_session.query(entities.User
            ).filter(entities.User.username == username
            ).filter(entities.User.password == password
            ).one()
        session['logged_user'] = user.id
        message = {'message': 'Authorized', 'user_id':user.id, 'username':user.username}
        #return Response(message, status=200, mimetype='applcation/json')
        return Response(json.dumps(message, cls=connector.AlchemyEncoder), status=200, mimetype='application/json')
    except Exception:
        message = {'message': 'Unauthorized'}
        return Response(json.dumps(message, cls=connector.AlchemyEncoder), status=401, mimetype='application/json')


# #---- USERS METHODS ---------------------------


@app.route('/users', methods = ['GET'])
def get_users():
    session = db.getSession(engine)
    dbResponse = session.query(entities.User)
    data = []
    for user in dbResponse:
        data.append(user)
    message = {"data":data}
    return Response(json.dumps(message, cls=connector.AlchemyEncoder), mimetype='application/json')


@app.route('/users/<id>', methods = ['GET'])
def get_user(id):
    db_session = db.getSession(engine)
    users = db_session.query(entities.User).filter(entities.User.id == id)
    for user in users:
        js = json.dumps(user, cls=connector.AlchemyEncoder)
        return  Response(js, status=200, mimetype='application/json')

    message = { 'status': 404, 'message': 'Not Found'}
    return Response(message, status=404, mimetype='application/json')


@app.route('/create_test_users', methods = ['GET'])
def create_test_users():
    db_session = db.getSession(engine)
    user = entities.User(name="David", fullname="Lazo", password="1234", username="qwerty")
    db_session.add(user)
    db_session.commit()
    return "Test user created!"


@app.route('/users', methods = ['POST'])
def create_user():
    c = json.loads(request.form['values'])
    user = entities.User(
        username=c['username'],
        name=c['name'],
        fullname=c['fullname'],
        password=c['password']
    )
    session = db.getSession(engine)
    session.add(user)
    session.commit()
    return 'Created User'


@app.route('/users', methods = ['PUT'])
def update_user():
    session = db.getSession(engine)
    id = request.form['key']
    user = session.query(entities.User).filter(entities.User.id == id).first()
    c =  json.loads(request.form['values'])
    for key in c.keys():
        setattr(user, key, c[key])
    session.add(user)
    session.commit()
    return 'Updated User'


@app.route('/users', methods = ['DELETE'])
def delete_message():
    id = request.form['key']
    session = db.getSession(engine)
    messages = session.query(entities.User).filter(entities.User.id == id)
    for message in messages:
        session.delete(message)
    session.commit()
    return "Deleted Message"


# #---- MESSAGES METHODS ---------------------------


@app.route('/messages', methods = ['GET'])
def get_Message():
    session = db.getSession(engine)
    dbResponse = session.query(entities.Message)
    data = []
    for messages in dbResponse:
        data.append(messages)
    return Response(json.dumps(data, cls=connector.AlchemyEncoder), mimetype='application/json')


@app.route('/create_test_messages', methods = ['GET'])
def create_test_messages():
    db_session = db.getSession(engine)
    message = entities.Message(content="Another message", user_from_id="2", user_to_id="4")
    db_session.add(message)
    db_session.commit()
    return "Test message created!"


# #---- CHAT METHODS ---------------------------


@app.route('/current', methods = ["GET"])
def current_user():
    db_session = db.getSession(engine)
    user = db_session.query(entities.User).filter(
        entities.User.id == session['logged_user']
        ).first()
    return Response(json.dumps(
            user,
            cls=connector.AlchemyEncoder),
            mimetype='application/json'
        )


@app.route('/current_chat/', methods=["POST"])
def current_chat():
    db_session = db.getSession(engine)
    id_data = json.loads(request.data)
    other_user = id_data['id']
    curr_id = session['logged_user']
    messages = db_session.query(entities.Message)\
        .filter(or_((entities.Message.user_from_id == curr_id) & (entities.Message.user_to_id == other_user),
                (entities.Message.user_from_id == other_user) & (entities.Message.user_to_id == curr_id)))
    data = []
    for msg in messages:
        data.append(msg)
    return Response(json.dumps(data, cls=connector.AlchemyEncoder), mimetype='application/json')


@app.route('/chats/<user_from_id>/<user_to_id>', methods = ['GET'])
def getChats(user_from_id, user_to_id):
    db_session = db.getSession(engine)
    chats = db_session.query(entities.Message)\
        .filter(or_((entities.Message.user_from_id == user_from_id) & (entities.Message.user_to_id == user_to_id),
                (entities.Message.user_from_id == user_to_id) & (entities.Message.user_to_id == user_from_id)))
    data = []
    for chat in chats:
        data.append(chat)
    return Response(json.dumps({'response':data}, cls=connector.AlchemyEncoder), mimetype='application/json')


@app.route('/send_message', methods=['POST'])
def send_message():
    msg_data = json.loads(request.data)
    print(msg_data)
    curr_id = session['logged_user']
    message = entities.Message(
        content=msg_data['content'],
        user_from_id=curr_id,
        user_to_id=msg_data['user_to_id'],
    )
    de_session = db.getSession(engine)
    de_session.add(message)
    de_session.commit()
    message = {'message': 'Se envio el mensaje :)'}
    return Response(json.dumps(message, cls=connector.AlchemyEncoder), mimetype='applcation/json')


@app.route('/messages', methods=['POST'])
def create_messages():
    msg_data = json.loads(request.data)
    message = entities.Message(
        content=msg_data['content'],
        user_from_id=msg_data['user_from_id'],
        user_to_id=msg_data['user_to_id'],
    )
    session = db.getSession(engine)
    session.add(message)
    session.commit()
    message = {'message': 'Se envio el mensaje mobile :)'}
    return Response(json.dumps(message, cls=connector.AlchemyEncoder), status=200, mimetype='applcation/json')
    #return "Mensaje enviado"

if __name__ == '__main__':
    app.secret_key = ".."
    app.run(port=8080, threaded=True, host=('10.100.224.106'))
