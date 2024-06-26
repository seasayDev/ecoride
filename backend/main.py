from flask import Flask ,g,jsonify,request,session
from flask_cors import CORS
from database.database import Database
import hashlib
import uuid
from flask_mail import Mail, Message
# import yaml
# import string
# import secrets
from bcrypt import hashpw, gensalt,checkpw


app =Flask(__name__)

app.config.from_object(__name__)
app.secret_key = 'Xp2s5v8y/B?D(G+KbPeShVmYq3t6w9z$'

CORS(app,resources={r"/*":{'origins':"*"}})
# CORS(app,resources={r"/*":{'origins':'http://localhost:8080',"allow_headers":"Acces-Control-Allow-Origins"}})
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        g._database = Database()
    return g._database


@app.route('/register', methods=['POST'])
def inscription():
    data = request.get_json()
    required_fields = ["lastName", "firstName", "country", "address", "city",
                       "province", "postalCode", "birthdate", "email", "phone",
                       "password", "confirmPassword"]
    if not all(data.get(field) for field in required_fields):
        return jsonify({"error": "All fields are required."}), 400

    if data['password'] != data['confirmPassword']:
        return jsonify({"error": "Passwords do not match."}), 401

    if get_db().get_user_by_email(data['email']):
        return jsonify({"error": "User already exists"}), 403

    # Securely hash the password
    salt = uuid.uuid4().hex
    hashed_password = hashpw((data['password'] + salt).encode('utf-8'), gensalt()).decode('utf-8')
    get_db().create_user(data['firstName'], data['lastName'], data['email'], data['birthdate'], data['phone'],
                         data['address'], data['country'], data['city'], data['province'], 
                         data['postalCode'], salt, hashed_password)
    
    return jsonify({"message": "Registration successful!"}), 201

@app.route('/login',methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('email')
    password = data.get('password')
    if not username or not password:
        return jsonify({"error": "Invalid password or username"}), 400
    user = get_db().get_user(username)
    if not user:
        return jsonify({"error": "User does not exist"}), 401
    salt, hash_p, fname, name, role, email, user_id = user
    hashed_password = hashpw(password.encode(), gensalt())

    if checkpw(password.encode(), hashed_password) and username == email:
        id_session = uuid.uuid4().hex
        get_db().save_session(id_session, username, fname, role)
        session_user = {
            'id': id_session, 
            'email': email,
            'fname': fname,
            'role': role,
        }
        return jsonify({"message": "Login successful", "session": session_user}), 200
    else:
        return jsonify({"error": "Invalid password"}), 401

@app.route('/logout',methods=['POST'])
def deconnexion():
    data = request.get_json()
    id_session = data.get('id')
    get_db().delete_session(id_session)
    return jsonify({'message': 'User logged out'}), 201

@app.route('/resetPassword',methods=['POST'])
def resetPassword():
    return jsonify({'message':"email reset sended"}), 201

@app.route('/',methods=['GET'])
def greetings():
    return ("hello word")


@app.route('/support', methods=['POST'])  # NEW
def submit_support_request():  # NEW
    data = request.json  # NEW
    user_id = data.get('user_id')  # NEW
    support_option = data.get('support_option')  # NEW
    message = data.get('message')  # NEW

    if not user_id or not support_option or not message:  # NEW
        return jsonify({'error': 'Missing data'}), 400  # NEW

    support_request_id = get_db().create_support_request(user_id, support_option, message)  # NEW
    return jsonify({'message': 'Support request submitted successfully', 'request_id': support_request_id}), 200 


if __name__=="__main__":
    app.run(debug=True)
