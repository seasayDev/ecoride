from flask import Flask ,g,jsonify,request,session
from flask_cors import CORS
from database.database import Database
import hashlib
import uuid


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
    nom = data.get("lastName")
    prenom = data.get("firstName")
    pays = data.get("country")
    addresse = data.get("address")
    ville = data.get("city")
    province = data.get("province")
    code_postal = data.get("postalCode")
    date_de_naissance = data.get("birthdate")
    email = data.get("email")
    phone = data.get("phone")
    password = data.get("password")
    password1 = data.get("confirmPassword")

    # Vérifier que les champs ne sont pas vides
    if not all([nom, prenom, password, email, pays, addresse, ville, province, code_postal, date_de_naissance, phone, password1]):
        return jsonify({"error": "Tous les champs sont obligatoires."}), 400
    if password != password1:
        return jsonify({"error": "Les mots de passes ne sont pas identiques!"}), 401
    user = get_db().get_user_by_email(email)
    print(user)
    if(user == email):
        return jsonify({"error": "user already exist"}), 403
    # Hash the password
    salt = uuid.uuid4().hex
    hashed_password = hashlib.sha512((password + salt).encode("utf-8")).hexdigest()
    db = get_db()
    db.create_user(prenom, nom, email, date_de_naissance, phone,
                   addresse, pays, ville, province, code_postal, salt, hashed_password)
    return jsonify({"message": "Inscription reussie!"}), 201

@app.route('/login',methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('email')
    password = data.get('password')
    if username == "" or password == "":
        return jsonify({"error", "Ivalide password or username"}),400
    user = get_db().get_user(username)
    if user is None:
        return jsonify({'error',"User does not exist"}),401
    salt = user[0]
    hash_p = user[1]
    fname = user[2]
    name = user[3]
    role = user[4]
    email = user[5]
    user_id = user[6]
    hashed_password = hashlib.sha512((password + salt).encode("utf-8")).hexdigest()
    if hashed_password == hash_p and username == email:
        # Access granted
        id_session = uuid.uuid4().hex
        get_db().save_session(id_session, username, name, role)
        session['user'] = {
            'id': id_session,
            'name': name,
            'fname': fname,
            'role': role,
            'email': username,
            'id_user': user_id
        }
        return jsonify({"message": "Login successful", "session": session['user']}), 200
    else:
        return jsonify({"error": "Invalid password"}), 401


@app.route('/',methods=['GET'])
def greetings():
    return ("hello word")

@app.route('/shark',methods=['GET'])
def shark():
    return ("hello, this is a new shark your calling from flask app")


if __name__=="__main__":
    app.run(debug=True)
