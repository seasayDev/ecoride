from flask import Flask, g, jsonify, request, session, render_template
from flask_cors import CORS
from database.database import Database
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail, Message
import yaml
import string
import secrets
from datetime import datetime
import base64
from functools import wraps

app = Flask(__name__)
app.secret_key = 'CHANGE_ME_USE_ENV_OR_CONFIG_FILE'
CORS(app, supports_credentials=True)

with open('email.yaml') as f:
    email_settings = yaml.safe_load(f)

app.config['MAIL_SERVER'] = email_settings['email']['host']
app.config['MAIL_PORT'] = email_settings['email']['port']
app.config['MAIL_USERNAME'] = email_settings['email']['username']
app.config['MAIL_PASSWORD'] = email_settings['email']['password']
app.config['MAIL_USE_TLS'] = True
mail = Mail(app)

UNAUTHORIZED = lambda m='Unauthorized': (jsonify({'error': m}), 401)
FORBIDDEN = lambda m='Forbidden': (jsonify({'error': m}), 403)


def get_db() -> Database:
    db = getattr(g, '_database', None)
    if db is None:
        g._database = Database()
    return g._database


def require_auth(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        auth = request.headers.get('Authorization', '')
        if not auth.startswith('Bearer '):
            return UNAUTHORIZED('Missing token')
        token = auth.split(' ', 1)[1].strip()
        db = get_db()
        email = db.get_session(token)
        if not email:
            return UNAUTHORIZED('Invalid session')
        request.user_email = email
        request.user = db.get_user(email)
        return fn(*args, **kwargs)
    return wrapper


def require_admin(fn):
    @wraps(fn)
    @require_auth
    def wrapper(*args, **kwargs):
        user = getattr(request, 'user', None)
        if not user or user[4] != 'admin':
            return FORBIDDEN('Admin required')
        return fn(*args, **kwargs)
    return wrapper


@app.errorhandler(404)
def not_found(_):
    return jsonify({'error': 'Resource not found'}), 404


@app.errorhandler(Exception)
def on_error(_):
    return jsonify({'error': 'Internal server error'}), 500


@app.route('/register', methods=['POST'])
def inscription():
    data = request.get_json(silent=True) or {}
    required_fields = ["lastName", "firstName", "country", "address", "city",
                       "province", "postalCode", "birthdate", "email", "phone",
                       "password", "confirmPassword"]
    if not all(data.get(field) for field in required_fields):
        return jsonify({"error": "All fields are required."}), 400
    if data['password'] != data['confirmPassword']:
        return jsonify({"error": "Passwords do not match."}), 401
    if get_db().get_user_by_email(data['email']):
        return jsonify({"error": "User already exists"}), 403
    hashed_password = generate_password_hash(data['password'])
    get_db().create_user(data['firstName'], data['lastName'], data['email'], data['birthdate'], data['phone'],
                         data['address'], data['country'], data['city'], data['province'],
                         data['postalCode'], hashed_password)
    return jsonify({"message": "Registration successful!"}), 201


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json(silent=True) or {}
    username = data.get('email')
    password = data.get('password')
    if not username or not password:
        return jsonify({"error": "email and password are required"}), 400
    user = get_db().get_user(username)
    if not user:
        return jsonify({"error": "User does not exist"}), 401
    salt_and_hash, fname, lname, role, email, user_id = user
    if email != username or not check_password_hash(salt_and_hash, password):
        return jsonify({"error": "Invalid password"}), 401
    id_session = uuid.uuid4().hex
    get_db().save_session(id_session, username, fname, role)
    return jsonify({"message": "Login successful", "session": {
        'id': id_session, 'email': email, 'fname': fname, 'role': role, 'id_user': user_id
    }}), 200


@app.route('/logout', methods=['POST'])
def deconnexion():
    data = request.get_json(silent=True) or {}
    id_session = data.get('id')
    if not id_session:
        return jsonify({'error': 'Session id required'}), 400
    get_db().delete_session(id_session)
    return jsonify({'message': 'User logged out'}), 200


@app.route('/resetPassword', methods=['POST'])
def resetPassword():
    try:
        data = request.get_json(silent=True) or {}
        email = data.get('email')
        user_id = get_db().get_user_id_by_email(email)
        if not user_id:
            return jsonify({'error': 'user does not exist'}), 404
        alphabet = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(secrets.choice(alphabet) for _ in range(10))
        hashed_password = generate_password_hash(password)
        get_db().update_user_password(user_id, hashed_password)
        recipient = email
        sender = email_settings['email']['sender']
        message = Message(subject='Réinitialisation du mot de passe',
                          sender=sender, recipients=[recipient])
        message.html = render_template('reset_password_confirmation.html', password=password)
        mail.send(message)
        return jsonify({'message': 'email reset sent'}), 200
    except Exception as e:
        app.logger.exception('reset error')
        return jsonify({'message': 'Failed to send email'}), 500


@app.route('/', methods=['GET'])
def greetings():
    return "EcoRide API: healthy"


@app.route('/support', methods=['GET'])
def support_page():
    return render_template('support.html')


@app.route('/support', methods=['POST'])
def submit_support_request():
    data = request.get_json(silent=True) or {}
    user_id = data.get('user_id')
    support_option = data.get('support_option')
    message = data.get('message')
    if not user_id or not support_option or not message:
        return jsonify({'error': 'Missing data'}), 400
    get_db().create_support_request(user_id, support_option, message)
    return jsonify({'message': 'Support request received successfully'}), 201


@app.route('/getTrotinettes', methods=['GET'])
def get_trotinettes():
    rows = get_db().get_all_trottinettes()
    trotinettes = []
    for row in rows:
        image_data = base64.b64encode(row[15]).decode('utf-8') if row[15] is not None else None
        trotinettes.append({
            'id_trotinette': row[0],
            'name': row[1],
            'category': row[2],
            'price': row[3],
            'available': bool(row[4]),
            'location': {'id': row[5], 'name': row[8], 'id_address': row[9]},
            'address': {'id': row[9], 'address': row[10], 'country': row[11],
                        'city': row[12], 'province': row[13], 'postalCode': row[14]},
            'image': {'id': row[6], 'data': image_data},
            'qte': row[7],
        })
    return jsonify(trotinettes)


@app.route('/getLocations', methods=['GET'])
def get_locations():
    data = get_db().get_all_locations()
    locations = [{'id_location': row[0], 'name': row[1], 'address_id': row[2]} for row in data]
    return jsonify(locations)


@app.route('/reserveTrotinette', methods=['POST'])
@require_auth
def reserve_trotinette():
    data = request.get_json(silent=True) or {}
    trotinette_id = data.get('trotinette_id')
    user_id = data.get('user_id')
    try:
        start_date = datetime.strptime(data.get('start_date'), '%Y-%m-%d %H:%M')
        end_date = datetime.strptime(data.get('end_date'), '%Y-%m-%d %H:%M')
    except (TypeError, ValueError):
        return jsonify({'error': 'Invalid dates. Use YYYY-MM-DD HH:MM'}), 400
    pick_up_address = data.get('pick_up_address')
    drop_off_address = data.get('drop_off_address')
    options = data.get('options', '')

    db = get_db()
    trotinette = db.get_trotinette_by_id(trotinette_id)
    if not trotinette or trotinette[6] <= 0:
        return jsonify({'error': 'Trotinette not available'}), 400

    total_hours = max((end_date - start_date).seconds / 3600, 1)
    total_cost = total_hours * trotinette[2]
    db.create_reservation(start_date, end_date, pick_up_address, drop_off_address,
                          total_cost, trotinette_id, user_id, options, total_hours)
    db.update_trotinette_quantity(trotinette_id, trotinette[6] - 1)

    user = db.get_user_by_id(user_id)
    recipient = user[5]
    sender = email_settings['email']['sender']
    confirmation = Message(subject='Reservation Confirmation',
                           sender=sender, recipients=[recipient])
    confirmation.html = render_template('reservation_confirmation.html',
                                         start_date=start_date, end_date=end_date,
                                         total_cost=total_cost,
                                         pick_up_address=pick_up_address,
                                         drop_off_address=drop_off_address)
    mail.send(confirmation)
    return jsonify({'message': 'Reservation successful'}), 201


@app.route('/createScooter', methods=['POST'])
@require_admin
def create_scooter():
    data = request.get_json(silent=True) or {}
    name = data.get('name')
    category = data.get('category')
    price = data.get('price')
    available = 1 if data.get('available') else 0
    location_id = data.get('location', {}).get('id_location') or data.get('location', {}).get('id')
    image_data = data.get('image', {}).get('data')
    qte = data.get('qte')
    if not all([name, category, price, location_id, qte is not None]):
        return jsonify({'error': 'Missing required fields'}), 400
    image_id = uuid.uuid4().hex
    file_bytes = base64.b64decode(image_data) if image_data else None
    get_db().create_trotinette(name, category, price, available, location_id, image_id, qte, file_bytes)
    return jsonify({"message": "scooter added", "image_id": image_id}), 201


@app.route('/updateScooter', methods=['PUT'])
@require_admin
def update_scooter():
    data = request.get_json(silent=True) or {}
    id_trotinette = data.get('id_trotinette')
    name = data.get('name')
    category = data.get('category')
    price = data.get('price')
    available = 1 if data.get('available') else 0
    location_id = data.get('location', {}).get('id') or data.get('location', {}).get('id_location')
    image_data = data.get('image', {}).get('data')
    image_id = data.get('image', {}).get('id')
    qte = data.get('qte')
    if not id_trotinette:
        return jsonify({'error': 'id_trotinette is required'}), 400
    file_bytes = base64.b64decode(image_data) if image_data else None
    if image_data and not image_id:
        image_id = uuid.uuid4().hex
        get_db().create_picture(image_id, file_bytes)
    get_db().update_trotinette(id_trotinette, category, name, price, qte, location_id, file_bytes, image_id, available)
    return jsonify({'message': 'Scooter updated'}), 200


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
    data = request.get_json(silent=True) or {}
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
    get_db().update_user_infos(id_user, data.get('firstName'), data.get('lastName'), data.get('email'),
                               data.get('dateOfBirth'), data.get('phone'), data.get('address'),
                               data.get('country'), data.get('city'), data.get('province'),
                               data.get('postalCode'), profil['id_address'])
    return jsonify({"message": "Profile updated successfully!"}), 200


@app.route('/deleteScooter', methods=['POST'])
@require_admin
def delete_scooter():
    data = request.get_json(silent=True) or {}
    id_trotinette = data.get('id')
    if not id_trotinette:
        return jsonify({'error': 'id required'}), 400
    get_db().delete_trotinette(id_trotinette)
    return jsonify({'message': 'scooter is deleted'}), 200


@app.route('/process-payment', methods=['POST'])
@require_auth
def process_payment():
    data = request.get_json(silent=True) or {}
    card_number = (data.get('cardNumber') or '').replace(' ', '')
    expiry = data.get('expiry')
    cvv = data.get('cvv')
    card_name = data.get('cardName')
    amount = data.get('amount')
    user_id = data.get('user_id')
    reservation_date = data.get('reservationDate')
    reservation_duration = data.get('reservationDuration')
    total_cost = data.get('totalCost')
    trotinette = data.get('trotinette', {}) or {}
    trotinette_id = trotinette.get('id_trotinette')
    pick_up_location_id = trotinette.get('location', {}).get('id')
    drop_off_location = data.get('dropOutLocation')

    if not all([card_number, expiry, cvv, card_name, user_id, trotinette_id, pick_up_location_id]):
        return jsonify({'error': 'Missing payment or reservation data'}), 400

    db = get_db()
    card = db.get_credit_card(card_number)
    if not card:
        return jsonify({'error': 'Credit Card not valid'}), 400
    try:
        hours = float(reservation_duration or 1)
    except (TypeError, ValueError):
        hours = 1.0
    start_dt = datetime.strptime(reservation_date, '%Y-%m-%d') if reservation_date else datetime.now()
    end_dt = start_dt
    payment_id = db.add_payment_history(user_id, amount, card[0])
    db.create_reservation(start_dt, end_dt, pick_up_location_id, drop_off_location,
                          float(total_cost or 0), trotinette_id, user_id, None, hours)
    return jsonify({'message': 'Payment successful', 'payment_id': payment_id}), 201


@app.route('/reservations', methods=['GET'])
def get_reservations():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'user_id is required'}), 400
    try:
        reservations = get_db().get_reservations(int(user_id))
    except ValueError:
        return jsonify({'error': 'Invalid user_id'}), 400
    result = []
    for r in reservations:
        result.append({
            'id_reservation': r[0],
            'start_date': r[1],
            'end_date': r[2],
            'pick_up_location': {'name': r[3]},
            'drop_off_location': {'name': r[4]},
            'total_cost': r[5],
            'trotinette': {'model': r[6], 'category': r[7], 'price': r[8],
                           'image': {'id': r[9], 'data': base64.b64encode(r[13]).decode('utf-8') if r[13] else None}},
            'user': {'id_user': r[12], 'first_name': r[10], 'last_name': r[11]},
        })
    return jsonify(result)


@app.route('/get_all_reservations', methods=['GET'])
@require_admin
def get_all_reservations():
    reservations = get_db().get_all_reservations()
    result = []
    for r in reservations:
        result.append({
            'id_reservation': r[0],
            'start_date': r[1],
            'end_date': r[2],
            'reservation_hours': r[3],
            'pick_up_location': {'name': r[4]},
            'drop_off_location': {'name': r[5]},
            'total_cost': r[6],
            'trotinette': {'model': r[7], 'category': r[8], 'price': r[9]},
            'user': {'id_user': r[10], 'first_name': r[11], 'last_name': r[12]},
        })
    return jsonify(result)


@app.route('/delete_reservation', methods=['DELETE'])
@require_auth
def delete_reservation():
    reservation_id = request.args.get('id_reservation')
    if not reservation_id:
        return jsonify({'error': 'Reservation ID is required'}), 400
    ok = get_db().delete_reservation_by_id(int(reservation_id))
    return (jsonify({'message': 'Reservation deleted'}) if ok else jsonify({'error': 'Failed'})), 200 if ok else 500


@app.route('/update_reservation', methods=['PUT'])
def update_reservation():
    data = request.get_json(silent=True) or {}
    reservation_id = data.get('id_reservation')
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    reservation_hours = data.get('reservation_hours')
    total_cost = data.get('total_cost')
    if not all([reservation_id, start_date, end_date, reservation_hours, total_cost]):
        return jsonify({'error': 'Missing fields'}), 400
    result = get_db().update_reservation(reservation_id, start_date, end_date, reservation_hours, total_cost)
    return (jsonify({'message': 'Reservation updated successfully'}) if result else jsonify({'error': 'Failed'})), 200 if result else 500


@app.route('/unlockTrotinette', methods=['POST'])
@require_auth
def unlock_trotinette():
    data = request.get_json(silent=True) or {}
    id_reservation = data.get('id_reservation')
    if not id_reservation:
        return jsonify({'error': 'Reservation ID is required'}), 400
    db = get_db()
    reservation = db.get_reservation_par_id(id_reservation)
    if not reservation:
        return jsonify({'error': 'Reservation not found'}), 404
    id_trotinette = reservation[6]
    db.delete_reservation(id_reservation)
    db.decrease_trotinette_quantity(id_trotinette)
    return jsonify({'message': 'Réservation annulée avec succès'}), 200


@app.route('/facturation', methods=['POST'])
@require_auth
def add_facturation():
    data = request.get_json(silent=True) or {}
    required = ["nom", "prenom", "adresse", "ville", "province", "codePostal", "telephone", "montant"]
    if not all(data.get(f) for f in required):
        return jsonify({"error": "All fields are required."}), 400
    get_db().add_facturation(request.user_email, data['nom'], data['prenom'], data['adresse'],
                             data['ville'], data['province'], data['codePostal'], data['telephone'], data['montant'])
    return jsonify({"message": "Facturation ajoutée avec succès"}), 201


@app.route('/facturation', methods=['GET'])
def get_facturation():
    id_user = request.args.get('id_user')
    if not id_user:
        return jsonify({'error': 'id_user required'}), 400
    facturation = get_db().get_facturation(int(id_user))
    return (jsonify(facturation) if facturation else jsonify({'message': 'Aucune facturation trouvée'})), 200


@app.route('/facturation', methods=['PUT'])
@require_auth
def update_facturation():
    data = request.get_json(silent=True) or {}
    required = ["nom", "prenom", "adresse", "ville", "province", "codePostal", "telephone", "montant"]
    if not all(data.get(f) for f in required):
        return jsonify({"error": "All fields are required."}), 400
    get_db().update_facturation(request.user_email, data['nom'], data['prenom'], data['adresse'],
                                data['ville'], data['province'], data['codePostal'], data['telephone'], data['montant'])
    return jsonify({"message": "Facturation mise à jour"}), 200


# Admin + reviews + promotions

@app.route('/stats/admin', methods=['GET'])
@require_admin
def admin_stats():
    db = get_db()
    users = db.get_user_admin()
    reservations = db.get_all_reservations()
    scooters = db.get_all_trottinettes()
    return jsonify({
        'users': len(users),
        'reservations': len(reservations),
        'scooters': len(scooters),
        'usersList': [{'id_user': u[0], 'name': f"{u[1]} {u[2]}", 'email': u[3],
                       'user_type': u[6]} for u in users],
    }), 200


@app.route('/reviews', methods=['POST'])
@require_auth
def create_review():
    data = request.get_json(silent=True) or {}
    trotinette_id = data.get('trotinette_id')
    rating = data.get('rating')
    comment = data.get('comment')
    if trotinette_id is None or rating is None:
        return jsonify({'error': 'trotinette_id and rating are required'}), 400
    review_id = get_db().create_review(request.user_email, int(trotinette_id), int(rating), comment)
    return jsonify({'id': review_id}), 201


@app.route('/reviews/<int:trotinette_id>', methods=['GET'])
def list_reviews(trotinette_id):
    reviews = get_db().get_reviews(trotinette_id)
    return jsonify(reviews), 200


@app.route('/rabais/active', methods=['GET'])
def active_rabais():
    rows = get_db().get_pub_active()
    return jsonify(rows), 200


@app.route('/rabais', methods=['POST'])
@require_admin
def create_rabais():
    data = request.get_json(silent=True) or {}
    name = data.get('name')
    value = data.get('value')
    code = data.get('code')
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    active = 1 if data.get('active') else 0
    image_id = data.get('image_id')
    if not all([name, value, code, start_date, end_date]):
        return jsonify({'error': 'Missing fields'}), 400
    inserted = get_db().create_pub(name, value, code, start_date, end_date, image_id)
    if not inserted:
        return jsonify({'error': 'Duplicate rabais'}), 409
    get_db().update_pub_active(active, inserted)
    return jsonify({'message': 'Rabais created'}), 201


if __name__ == '__main__':
    app.run(debug=True)
