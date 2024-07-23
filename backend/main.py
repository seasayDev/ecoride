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
from datetime import datetime
from bcrypt import hashpw, gensalt,checkpw
import base64

app = Flask(__name__)

app.config.from_object(__name__)
app.secret_key = 'Xp2s5v8y/B?D(G+KbPeShVmYq3t6w9z$'

CORS(app, resources={r"/*": {'origins': "*"}})
CORS(app, supports_credentials=True)
with open('email.yaml') as f:
    email_settings = yaml.safe_load(f)

app.config['MAIL_SERVER'] = email_settings['email']['host']
app.config['MAIL_PORT'] = email_settings['email']['port']
app.config['MAIL_USERNAME'] = email_settings['email']['username']
app.config['MAIL_PASSWORD'] = email_settings['email']['password']
app.config['MAIL_USE_TLS'] = True
mail = Mail(app)



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
        message = Message(subject=password,
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
        image_data = base64.b64encode(row[15]).decode('utf-8') if row[15] is not None else None
        trotinette = {
            'id_trotinette': row[0],
            'name': row[1],
            'category': row[2],
            'price': row[3],
            'available': row[4],
            'location': {
                'id': row[5],
                'name': row[8],
                'id_address':row[9]
            },
            'address': {
                    'id': row[9],
                    'address': row[10],
                    'country': row[11],
                    'city': row[12],
                    'province': row[13],
                    'postal_code': row[14]
                },
            'image': {
                'id': row[6],
                'data': image_data
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

@app.route('/reserveTrotinette', methods=['POST'])
def reserve_trotinette():
    data = request.get_json()
    trotinette_id = data.get('trotinette_id')
    user_id = data.get('user_id')
    start_date = datetime.strptime(data.get('start_date'), '%Y-%m-%d %H:%M')
    end_date = datetime.strptime(data.get('end_date'), '%Y-%m-%d %H:%M')
    pick_up_address = data.get('pick_up_address')
    drop_off_address = data.get('drop_off_address')
    options = data.get('options', '')

    db = get_db()
    trotinette = db.get_trotinette_by_id(trotinette_id)

    if not trotinette or trotinette['qte'] <= 0:
        return jsonify({'error': 'Trotinette not available'}), 400

    total_cost = (end_date - start_date).seconds / 3600 * trotinette['price']
    db.create_reservation(start_date, end_date, pick_up_address, drop_off_address, total_cost, trotinette_id, user_id, options)
    db.update_trotinette_quantity(trotinette_id, trotinette['qte'] - 1)

    user = db.get_user_by_id(user_id)
    recipient = user['email']
    sender = email_settings['email']['sender']
    message = Message(subject='Reservation Confirmation',
                      sender=sender, recipients=[recipient])
    message.html = render_template('reservation_confirmation.html', 
                                   start_date=start_date, 
                                   end_date=end_date, 
                                   total_cost=total_cost,
                                   pick_up_address=pick_up_address,
                                   drop_off_address=drop_off_address)
    mail.send(message)

    return jsonify({'message': 'Reservation successful'}), 201

@app.route('/createScooter',methods=['POST'])
def create_scooter():
    try:
        data = request.get_json()
        name = data.get('name')
        category = data.get('category')
        price = data.get('price')
        available = data.get('available', False)  # Default to False if not provided
        location_id = data.get('location', {}).get('id_location')
        image_data = data.get('image', {}).get('data')
        qte = data.get('qte')
        # print(name,category,price,location_id,qte,image_data)
        if not (name and category and price and location_id and qte is not None):
            return jsonify({'error': 'Missing required fields'}), 400
        image_id = str(uuid.uuid4().hex)
        file_data = base64.b64decode(image_data) if image_data else None
        get_db().create_trotinette(name, category, price, available, location_id, image_id, qte, file_data)
        return jsonify({'message':"sccoter added"}), 201
    except Exception as e:
        return jsonify({'error': 'An error occurred while processing your request'}), 500

@app.route('/updateScooter',methods=['PUT'])
def update_scooter():
    try:
        data = request.get_json()
        id_trotinette = data.get('id_trotinette')
        name = data.get('name')
        category = data.get('category')
        price = data.get('price')
        available = data.get('available', False)  # Default to False if not provided
        location_id = data.get('location', {}).get('id')
        image_data = data.get('image', {}).get('data')
        image_id = data.get('image', {}).get('id')
        qte = data.get('qte')

        # Decode the base64 image data if it exists
        file_data = base64.b64decode(image_data) if image_data else None
        if not image_id:
            image_id = str(uuid.uuid4().hex)
            get_db().create_picture(image_id,file_data)
        # Print for debugging
        # print(id_trotinette, name, category, price, available, location_id, image_id, qte)

        # Call the update function
        get_db().update_trotinette(id_trotinette, category, name, price, qte, location_id, file_data, image_id, available)
        return jsonify({'message': 'Scooter updated'}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'An error occurred while processing your request'}), 500


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


@app.route('/deleteScooter',methods=['POST'])
def delete_scooter():
    data =request.get_json()
    id_trotinette = data.get('id')
    get_db().delete_trotinette(id_trotinette)
    return jsonify({'message':'scooter is deleted '}),200


@app.route('/process-payment', methods=['POST'])
def process_payment():
    data = request.json
    card_number = data.get('cardNumber').replace(' ', '')
    expiry = data.get('expiry')
    cvv = data.get('cvv')
    card_name = data.get('cardName')
    amount = data.get('amount')  # Future amount of the cart
    user_id = data.get('user_id')
    
    reservation_date = data.get('reservationDate')
    reservation_duration = data.get('reservationDuration')
    reservation_time = data.get('reservationTime')
    total_cost = data.get('totalCost')
    
    trotinette = data.get('trotinette')
    trotinette_id = trotinette.get('id_trotinette')
    location = trotinette.get('location')
    pick_up_location_id = location.get('id')
    dropOutLocation = data.get('dropOutLocation')
  

    db = get_db()
    card = db.get_credit_card(card_number)

    if not card:
        return jsonify({'error': 'Credit Card not valid'}), 400

    if card[2] != expiry or card[3] != cvv or card[4] != card_name:
        return jsonify({'error': 'Card info invalid'}), 400

    # Process payment
    payment_id = db.add_payment_history(user_id, amount, card[0])

    # Create reservation
    end_date = reservation_date  # Start date and end date are the same for the reservation
    reservation_hours = reservation_duration  # Reservation duration

    db.create_reservation(
        start_date=reservation_date,
        end_date=end_date,
        pick_up_location_id=pick_up_location_id,
        drop_off_location_id=dropOutLocation, 
        total_cost=total_cost,
        trotinette_id=trotinette_id,
        user_id=user_id,
        options=None,  # Assuming no additional options
        reservation_hours=reservation_hours
    )

    return jsonify({'message': 'Payment successful', 'payment_id': payment_id}), 200

@app.route('/reservations', methods=['GET'])
def get_reservations():
    user_id = request.args.get('user_id')

    if user_id is None:
        return jsonify({'error': 'User ID is required'}), 400

    try:
        reservations = get_db().get_reservations(user_id)
        result = []

        for reservation in reservations:
            # Base64 encode the image data
            image_data = base64.b64encode(reservation[13]).decode('utf-8') if reservation[13] else None

            result.append({
                'id_reservation': reservation[0],
                'start_date': reservation[1],
                'end_date': reservation[2],
                'pick_up_location': {
                    'name': reservation[3]
                },
                'drop_off_location': {
                    'name': reservation[4]
                },
                'total_cost': reservation[5],
                'trotinette': {
                    'model': reservation[6],
                    'category': reservation[7],
                    'price': reservation[8],
                    'image': {
                        'id': reservation[9],
                        'data': image_data
                    }
                },
                'user': {
                    'id_user': reservation[12],
                    'first_name': reservation[10],
                    'last_name': reservation[11]
                }
            })

        return jsonify(result)
    except Exception as e:
        app.logger.error(f"Error fetching reservations: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

# Logique facturation
@app.route('/facturation', methods=['POST'])
def add_facturation():
    data = request.get_json()
    id_user = data.get('id_user')
    if not id_user:
        return jsonify({"error": "User ID is required"}), 400
    
    required_fields = ["nom", "prenom", "adresse", "ville", "province", "codePostal", "telephone", "montant"]
    if not all(data.get(field) for field in required_fields):
        return jsonify({"error": "All fields are required."}), 400
    
    try:
        get_db().add_facturation(id_user, data['nom'], data['prenom'], data['adresse'], 
                                 data['ville'], data['province'], data['codePostal'], 
                                 data['telephone'], data['montant'])
        return jsonify({"message": "Facturation ajoutée avec succès"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/facturation/<id_user>', methods=['GET'])
def get_facturation(id_user):
    try:
        facturation = get_db().get_facturation(id_user)
        if facturation:
            return jsonify(facturation), 200
        else:
            return jsonify({"message": "Aucune facturation trouvée"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/facturation/<id_user>', methods=['PUT'])
def update_facturation(id_user):
    data = request.get_json()
    required_fields = ["nom", "prenom", "adresse", "ville", "province", "codePostal", "telephone", "montant"]
    if not all(data.get(field) for field in required_fields):
        return jsonify({"error": "All fields are required."}), 400
    
    try:
        get_db().update_facturation(id_user, data['nom'], data['prenom'], data['adresse'], 
                                    data['ville'], data['province'], data['codePostal'], 
                                    data['telephone'], data['montant'])
        return jsonify({"message": "Facturation mise à jour avec succès"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500




if __name__ == "__main__":
    app.run(debug=True)