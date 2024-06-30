from flask import Flask, g, jsonify, request, session, render_template
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

with open('email.yaml') as f:
    email_settings = yaml.safe_load(f)

app.config['MAIL_SERVER'] = email_settings['email']['host']
app.config['MAIL_PORT'] = email_settings['email']['port']
app.config['MAIL_USERNAME'] = email_settings['email']['username']
app.config['MAIL_PASSWORD'] = email_settings['email']['password']
app.config['MAIL_USE_TLS'] = True
mail = Mail(app)

CORS(app, resources={r"/*": {"origins": "*"}})

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
    try:
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
        db.update_user_password(user_id, salt, hashed_password)
        recipient = email
        sender = email_settings['email']['sender']
        message = Message(subject='PASSWORD RESETED',
                          sender=sender, recipients=[recipient])
        message.html = render_template('reset_password_confirmation.html', password=password)
        mail.send(message)
        return jsonify({'message':"email reset sended"}), 201
    except Exception as e:
        return jsonify({'message':'Failed to send email'}),500

@app.route('/', methods=['GET'])
def greetings():
    return ("hello INF6150")

@app.route('/support', methods=['GET'])
def support_page():
    return render_template('support.html')

@app.route('/support', methods=['POST'])
def submit_support_request():
    data = request.json
    user_id = data.get('user_id')
    support_option = data.get('support_option')
    message = data.get('message')

    if not user_id or not support_option or not message:
        return jsonify({'error': 'Missing data'}), 400

    return jsonify({'message': 'Support request received successfully'})

@app.route('/getTrotinettes', methods=['GET'])
def get_trotinettes():
    data = get_db().get_all_trottinettes()
    trotinettes = []
    for row in data:
        trotinette = {
            'id_trotinette': row[0],
            'name': row[1],
            'category': row[2],
            'price': row[3],
            'available': row[4],
            'location': {
                'id': row[5],
                'name': row[8],
                'address': {
                    'id': row[9],
                    'address': row[10],
                    'country': row[11],
                    'city': row[12],
                    'province': row[13],
                    'postal_code': row[14]
                }
            },
            'image': {
                'id': row[6],
                'data': row[15]
            },
            'qte': row[7]
        }
        trotinettes.append(trotinette)

    return jsonify(trotinettes)

@app.route('/getLocations', methods=['GET'])
def get_locations():
    data = get_db().get_all_locations()
    locations = []
    for row in data:
        location = {
            'id_location': row[0],
            'name': row[1],
            'address_id': row[2]
        }
        locations.append(location)
    return jsonify(locations)

if __name__ == "__main__":
    app.run(debug=True)
