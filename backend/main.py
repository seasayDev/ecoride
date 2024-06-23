from flask import Flask ,g,jsonify,request
from flask_cors import CORS
from database.database import Database
import hashlib
import uuid

app =Flask(__name__)

app.config.from_object(__name__)


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
    print("Received data:", data)
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
        return jsonify({"error": "Les mots de passes ne sont pas identiques!"}), 400
    # Hash the password
    salt = uuid.uuid4().hex
    hashed_password = hashlib.sha512((password + salt).encode("utf-8")).hexdigest()
    db = get_db()
    db.create_user(prenom, nom, email, date_de_naissance, phone,
                   addresse, pays, ville, province, code_postal, salt, hashed_password)
    return jsonify({"message": "Inscription reussie!"}), 201

@app.route('/',methods=['GET'])
def greetings():
    return ("hello word")

@app.route('/shark',methods=['GET'])
def shark():
    return ("hello, this is a new shark your calling from flask app")


if __name__=="__main__":
    app.run(debug=True)
