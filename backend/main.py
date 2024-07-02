from flask import Flask, g, jsonify, request, session
from flask_cors import CORS
from database.database import Database
import hashlib
import uuid
from flask_mail import Mail, Message
import yaml
import string
import secrets
from bcrypt import hashpw, gensalt, checkpw

app = Flask(__name__)

app.config.from_object(__name__)
app.secret_key = 'Xp2s5v8y/B?D(G+KbPeShVmYq3t6w9z$'

CORS(app, resources={r"/*": {'origins': "*"}})
CORS(app, supports_credentials=True)

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

    salt = uuid.uuid4().hex
    hashed_password = hashpw((data['password'] + salt).encode('utf-8'), gensalt()).decode('utf-8')
    get_db().create_user(data['firstName'], data['lastName'], data['email'], data['birthdate'], data['phone'],
                         data['address'], data['country'], data['city'], data['province'], 
                         data['postalCode'], salt, hashed_password)
    
    return jsonify({"message": "Registration successful!"}), 201

@app.route('/login', methods=['POST'])
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
            'id_user': user_id
        }
        return jsonify({"message": "Login successful", "session": session_user}), 200
    else:
        return jsonify({"error": "Invalid password"}), 401

@app.route('/logout', methods=['POST'])
def deconnexion():
    data = request.get_json()
    id_session = data.get('id')
    get_db().delete_session(id_session)
    return jsonify({'message': 'User logged out'}), 201

@app.route('/resetPassword', methods=['POST'])
def resetPassword():
    data = request.get_json()
    email = data.get('email')
    user_id = get_db().get_user_id_by_email(email)
    if not user_id:
        return jsonify({'error':'user does not exist'}),400
    alphabet = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(alphabet) for i in range(10))
    salt = uuid.uuid4().hex
    hashed_password = hashpw((password + salt).encode('utf-8'), gensalt()).decode('utf-8')
    db = get_db()
    db.update_user_password(user_id,salt,hashed_password)
    return jsonify({'message':"email reset sended"}), 201

@app.route('/', methods=['GET'])
def greetings():
    return "hello INF6150"

@app.route('/support', methods=['POST'])  
def submit_support_request():  
    data = request.json  
    user_id = data.get('user_id')  
    support_option = data.get('support_option')  
    message = data.get('message')  

    if not user_id or not support_option or not message:  
        return jsonify({'error': 'Missing data'}), 400  

    support_request_id = get_db().create_support_request(user_id, support_option, message) 
    return jsonify({'message': 'Support request submitted successfully', 'request_id': support_request_id}), 200 

@app.route('/profil', methods=['GET'])
def get_user():
    id_user = request.args.get('id_user')
    
    if not id_user:
        return jsonify({"error": "User not logged in"}), 401

    try:
        id_user = int(id_user)
    except ValueError:
        return jsonify({"error": "Invalid user ID"}), 400

    profil = get_db().get_user_info(id_user)
    if not profil:
        return jsonify({"error": "User not found"}), 404

    return jsonify(profil), 200

@app.route('/editProfil', methods=['PUT'])
def edit_user():
    data = request.get_json()
    id_user = request.args.get('id_user')

    if not id_user:
        return jsonify({"error": "User not logged in"}), 401

    try:
        id_user = int(id_user)
    except ValueError:
        return jsonify({"error": "Invalid user ID"}), 400

    profil = get_db().get_user_info(id_user)
    if not profil:
        return jsonify({"error": "User not found"}), 404

    get_db().update_user_infos(id_user, data['firstName'], data['lastName'], data['email'], data['dateOfBirth'],
                               data['phone'], data['address'], data['country'], data['city'], data['province'], data['postalCode'], profil['id_address'])
    return jsonify({"message": "Profile updated successfully!"}), 200

if __name__ == "__main__":
    app.run(debug=True)