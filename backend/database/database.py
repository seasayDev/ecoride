import sqlite3
import uuid

class Database:
    def __init__(self):
        self.connection = None

    def get_connection(self):
        if self.connection is None:
            self.connection = sqlite3.connect('./database/data.db')
        return self.connection

    def disconnect(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None

    def create_user(self, first_name, last_name, email, date_of_birth,
                    phone, address, country, city, province, postal_code, salt, hash):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO addresses (address,country,city,province,postal_code) VALUES (?,?,?,?,?)",
                       (address, country, city, province, postal_code))
        address_id = cursor.lastrowid
        cursor.execute(
            "INSERT INTO users(first_name,last_name,email,address_id,date_of_birth,phone,salt,hash) VALUES(?,?,?,?,?,?,?,?)",
            (first_name, last_name, email, address_id, date_of_birth, phone, salt, hash))
        connection.commit()

    def get_user(self, email):
        cursor = self.get_connection().cursor()
        cursor.execute(("select salt, hash,first_name,last_name,user_type,email,id_user from users where email=?"),
                       (email,))
        user = cursor.fetchone()
        if user is None:
            return None
        else:
            return user[0], user[1], user[2], user[3], user[4], user[5], user[6]

    def get_user_by_email(self, email):
        cursor = self.get_connection().cursor()
        cursor.execute(("select email from users where email=?"),
                       (email,))
        user = cursor.fetchone()
        if user is None:
            return None
        else:
            return user[0]

    def get_user_id_by_email(self, email):
        cursor = self.get_connection().cursor()
        cursor.execute(("select id_user from users where email=?"),
                       (email,))
        user = cursor.fetchone()
        if user is None:
            return None
        else:
            return user[0]

    def save_session(self, id_session, email, name, role):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO sessions(id_session, email, name, user_type) VALUES (?, ?, ?, ?)",
                       (id_session, email, name, role))
        connection.commit()
        cursor.execute("SELECT id_session, email, name, user_type FROM sessions WHERE id_session = ?", (id_session,))
        userSession = cursor.fetchone()
        return userSession

    def delete_session(self, id_session):
        connection = self.get_connection()
        connection.execute(("delete from sessions where id_session=?"),
                           (id_session,))
        connection.commit()

    def get_session(self, id_session):
        cursor = self.get_connection().cursor()
        cursor.execute(("select email from sessions where id_session=?"),
                       (id_session,))
        data = cursor.fetchone()
        if data is None:
            return None
        else:
            return data[0]

    def update_user(self, id_user, user_type):
        cursor = self.get_connection()
        cursor.execute(
            ('UPDATE users set user_type = ? where id_user =?'), (user_type, id_user))
        cursor.commit()

    def get_user_id(self, id):
        cursor = self.get_connection().cursor()
        cursor.execute(("select * from users where id_user=?"), (id,))
        user = cursor.fetchall()
        if not user:  # Si la liste est vide
            return None
        elif len(user) > 1:  # Si la liste contient plusieurs éléments
            raise ValueError("La requête retourne plusieurs utilisateurs.")
        else:
            return user[0]  # Renvoyer le premier élément de la liste

    def get_user_adress(self, id):
        cursor = self.get_connection().cursor()
        cursor.execute(("select address_id from users where id_user=?"),
                       (id,))
        userAddId = cursor.fetchone()
        print(userAddId[0])
        cursor.execute(("select * from addresses where id_address=?"),
                       (userAddId[0],))
        userAdd = cursor.fetchone()
        if userAdd is None:
            return None
        else:
            return userAdd

    def get_reservation_admin(self):
        cursor = self.get_connection().cursor()
        cursor.execute("SELECT reservations.id_reservation, reservations.start_date, reservations.end_date," +
                       "reservations.pick_up_address, reservations.drop_off_address, reservations.total_cost, " +
                       "trotinette.name AS model, trotinette.category AS category, trotinette.price AS price, users.first_name, users.last_name " +
                       "FROM reservations " +
                       "INNER JOIN trotinette ON reservations.trotinette_id = trotinette.id_trotinette " +
                       "INNER JOIN users ON reservations.user_id = users.id_user;")
        reservations = cursor.fetchall()
        return reservations

    def update_reservation_admin(self, id_reservation, start_date, end_date, total_cost, category):
        cursor = self.get_connection()
        cursor.execute("UPDATE reservations " +
                       "SET start_date = ?, end_date = ?, total_cost = ?, trotinette_id = " +
                       "(SELECT id_trotinette FROM trotinette WHERE category = ?) " +
                       "WHERE id_reservation = ?", (start_date, end_date, total_cost, category, id_reservation))
        cursor.commit()

    def update_reservation_dropout(self, id_reservation, end_date):
        cursor = self.get_connection()
        cursor.execute("UPDATE reservations " +
                       "SET end_date = ?" +
                       "WHERE id_reservation = ?", (end_date, id_reservation))
        cursor.commit()

    def delete_reservation(self, id_reservation):
        cursor = self.get_connection()
        cursor.execute(
            "DELETE FROM reservations where id_reservation = ?", (id_reservation,))
        cursor.commit()

    def update_user_infos(self, id_user, first_name, last_name, email, date_of_birth,
                          phone, address, country, city, province, postal_code, id_address):
        print(postal_code)
        cursor = self.get_connection().cursor()
        cursor.execute(
            ('UPDATE users set first_name = ?, last_name = ?, email = ?,  date_of_birth = ?,'
             'phone = ?  WHERE id_user = ?'),
            (first_name, last_name, email,  date_of_birth, phone, id_user))
        cursor.connection.commit()
        cur = self.get_connection().cursor()
        cur.execute(
            ('UPDATE addresses set address = ?, country = ?, city = ?, province = ?, postal_code = ? WHERE id_address = ?'),
            (address, country, city, province, postal_code, id_address))
        cur.connection.commit()

    def get_user_adress(self, idUser):
        cursor = self.get_connection().cursor()
        cursor.execute(("select address_id from users where id_user=?"),
                       (idUser,))
        userAddId = cursor.fetchone()
        print(userAddId)
        cursor.execute(("select * from addresses where id_address=?"),
                       (userAddId[0],))
        userAdd = cursor.fetchone()
        print(userAdd)
        if userAdd is None:
            return None
        else:
            return userAdd

    def get_all_clients(self):
        cursor = self.get_connection().cursor()
        cursor.execute(("SELECT * FROM users WHERE user_type=?"), ("user",))
        users = cursor.fetchall()
        return users

    def get_id_adress(self, id):
        cursor = self.get_connection().cursor()
        cursor.execute(("select address_id from users where id_user=?"),
                       (id,))
        userAddId = cursor.fetchone()
        if userAddId is None:
            return None
        else:
            return userAddId

    def get_reservation(self, id):
        cursor = self.get_connection().cursor()
        cursor.execute("SELECT * from reservations where user_id = ?", (id,))
        reservations = cursor.fetchall()
        return reservations

    def create_reservations(self, dateDepar, dateRetour, locaDepart, locRetour, totalCost, userid, idTrotinette, option):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM reservations WHERE start_date = ? AND end_date = ? AND pick_up_address = ? AND drop_off_address = ? AND total_cost = ? AND user_id = ?",
                       (dateDepar, dateRetour, locaDepart, locRetour, totalCost, userid))
        existing_reservation = cursor.fetchone()
        if existing_reservation is None:
            cursor.execute(
                "INSERT INTO reservations(start_date,end_date,pick_up_address, drop_off_address, total_cost, user_id, trotinette_id, options) VALUES(?,?,?,?,?,?,?,?)",
                (dateDepar, dateRetour, locaDepart, locRetour, totalCost, userid, idTrotinette, option))
            connection.commit()

    # def create_trotinette(self, categorie, modele, prix, qte, image_id):
    #     connection = self.get_connection()
    #     cursor = connection.cursor()
    #     cursor.execute("SELECT * FROM trotinette WHERE category = ? AND name = ?",
    #                    (categorie, modele))
    #     existing_trotinette = cursor.fetchone()
    #     if existing_trotinette is None:
    #         cursor.execute(
    #             "INSERT INTO trotinette (category,name,price,qte,image_id) VALUES (?,?,?,?,?)",
    #             (categorie.lower(), modele.lower(), prix, qte, image_id))
    #         connection.commit()
    def create_trotinette(self,name, category, price, available, location_id, image_id, qte, file_data):
        connection = self.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute("INSERT INTO pictures(id_pictures, data) VALUES(?, ?)", (image_id, sqlite3.Binary(file_data)))
            # Insert into trotinette table
            cursor.execute("""
                INSERT INTO trotinette(name, category, price, available, location_id, image_id, qte)
                VALUES( ?, ?, ?, ?, ?, ?, ?)
            """, (name, category, price, available, location_id, image_id, qte))
            connection.commit()
        except Exception as e:
            connection.rollback()
            print(f"Error inserting trotinette: {e}")
        finally:
            connection.close()

    def create_picture(self, pic_id, file_data):
        connection = self.get_connection()
        connection.execute("insert into pictures(id_pictures, data) values(?, ?)", [
                           pic_id, sqlite3.Binary(file_data.read())])
        connection.commit()

    def load_picture(self, pic_id):
        cursor = self.get_connection().cursor()
        cursor.execute(
            ("select data from pictures where id_pictures=?"), (pic_id,))
        picture = cursor.fetchone()
        if picture is None:
            return None
        else:
            blob_data = picture[0]
            return blob_data
    def create_trotinette(self,name, category, price, available, location_id, image_id, qte, file_data):
        connection = self.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute("INSERT INTO pictures(id_pictures, data) VALUES(?, ?)", (image_id, sqlite3.Binary(file_data)))
            # Insert into trotinette table
            cursor.execute("""
                INSERT INTO trotinette(name, category, price, available, location_id, image_id, qte)
                VALUES( ?, ?, ?, ?, ?, ?, ?)
            """, (name, category, price, available, location_id, image_id, qte))
            connection.commit()
        except Exception as e:
            connection.rollback()
            print(f"Error inserting trotinette: {e}")
        finally:
            connection.close()
    def get_trotinette_facture(self, idTrotinette):
        cursor = self.get_connection().cursor()
        cursor.execute("SELECT * FROM trotinette where id_trotinette=?", (idTrotinette,))
        trottinettes = cursor.fetchone()
        return trottinettes

    def get_all_trottinettes(self):
        query = """
        SELECT t.id_trotinette, t.name, t.category, t.price, t.available, t.location_id, t.image_id, t.qte,
               l.name as location_name, l.address_id,
               a.address, a.country, a.city, a.province, a.postal_code,
               p.data as picture_data
        FROM trotinette t
        LEFT JOIN locations l ON t.location_id = l.id_location
        LEFT JOIN addresses a ON l.address_id = a.id_address
        LEFT JOIN pictures p ON t.image_id = p.id_pictures
        """

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            result = cursor.fetchall()

        return result

    def delete_trotinette(self, id_trotinette):
        cursor = self.get_connection()
        cursor.execute(
            "DELETE FROM trotinette where id_trotinette = ? ", (id_trotinette,))
        cursor.commit()

    def update_trotinette(self, id_trotinette, categorie, modele, prix, qte, location_id, image_data, image_id,available):
        connection = self.get_connection()
        cursor = connection.cursor()
        try:
            # Update pictures table if image data is provided
            if image_data:
                cursor.execute("UPDATE pictures SET data = ? WHERE id_pictures = ?", (sqlite3.Binary(image_data), image_id))
            # Update trotinette table
            cursor.execute("""
                UPDATE trotinette
                SET category = ?, name = ?, price = ?, qte = ?, location_id = ?, available = ?
                WHERE id_trotinette = ? AND image_id = ?
            """, (categorie, modele, prix, qte, location_id, available, id_trotinette, image_id))
            connection.commit()
        except Exception as e:
            connection.rollback()
            print(f"Error updating trotinette: {e}")

    def update_trotinette_qte_Dec(self, id_trotinette):
        cursor = self.get_connection().cursor()
        cursor.execute(
            "SELECT qte FROM trotinette where id_trotinette=?", (id_trotinette,))
        oldqte = cursor.fetchone()
        print(oldqte)
        newQte = oldqte[0] - 1
        print(newQte)
        cursor = self.get_connection()
        cursor.execute("UPDATE trotinette set qte = ? where id_trotinette= ?",
                       (newQte, id_trotinette))
        cursor.commit()

    def update_trotinette_qte_Inc(self, id_trotinette):
        cursor = self.get_connection().cursor()
        cursor.execute(
            "SELECT qte FROM trotinette where id_trotinette=?", (id_trotinette,))
        oldqte = cursor.fetchone()
        print(oldqte)
        newQte = oldqte[0] + 1
        print(newQte)
        cursor = self.get_connection()
        cursor.execute("UPDATE trotinette set qte = ? where id_trotinette= ?",
                       (newQte, id_trotinette))
        cursor.commit()

    def create_pub(self, name, valeur, code, date_depart, date_fin, pic_id):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM rabais WHERE name = ? AND value = ? AND code = ? AND start_date = ? AND end_date = ?",
                    (name, valeur, code, date_depart, date_fin))
        existing_rabais = cursor.fetchone()
        if existing_rabais is None:
            cursor.execute(
                "INSERT INTO rabais (name, value, code, start_date,end_date, image_id) VALUES(?,?,?,?,?,?)",
                (name, valeur, code, date_depart, date_fin, pic_id))
            connection.commit()
            return cursor.lastrowid
        else:
            return None

    def create_picture(self, image_id, file_data):
        connection = self.get_connection()
        connection.execute("INSERT INTO pictures(id_pictures, data) VALUES(?, ?)", (image_id, sqlite3.Binary(file_data)))
        connection.commit()

    def get_picture_data(self, picture_id):
        cursor = self.get_connection().cursor()
        cursor.execute("SELECT * FROM pictures WHERE id_pictures = ?", (picture_id,))
        row = cursor.fetchone()
        if row is None:
            return None
        else:
            return row[1]

    def get_pub(self):
        cursor = self.get_connection().cursor()
        cursor.execute("SELECT * FROM rabais")
        rabais = cursor.fetchall()
        return rabais

    def get_pub_id(self, id):
        cursor = self.get_connection().cursor()
        cursor.execute("SELECT * FROM rabais where id_rabais = ?", (id,))
        rabais = cursor.fetchall()
        return rabais
    
    def get_pub_active(self):
        cursor = self.get_connection().cursor()
        cursor.execute("SELECT * FROM rabais where active = ?", (1,))
        rabais = cursor.fetchall()
        print(rabais)
        return rabais
    
    def delete_pub(self, id_rabais):
        cursor = self.get_connection()
        cursor.execute(
            "DELETE FROM rabais where id_rabais = ?", (id_rabais,))
        cursor.commit()

    def update_pub(self, id_rabais, name, valeur, code, date_depart, date_fin, pic_id):
        cursor = self.get_connection()
        cursor.execute("UPDATE rabais set name = ?, value =?, code =?, start_date =?, end_date=?, image=? where id_rabais =?",
                       (name, valeur, code, date_depart, date_fin, pic_id, id_rabais))
        cursor.commit()

    def update_pub_active(self, bool, id_rabais):
        cursor = self.get_connection()
        cursor.execute("UPDATE rabais set active = ? where id_rabais =?",
                       (bool, id_rabais))
        cursor.commit()

    def get_reservation_par_id(self, id_reservation):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM reservations WHERE id_reservation=?", (id_reservation,))
        reservation = cursor.fetchone()
        return reservation

    def update_reservation(self, idReservation, date_return, date_pick_up, emplacementRecup, emplacementRetour, totalFacture, iduser, idTrotinette, donnees_encodees):
        cursor = self.get_connection()
        cursor.execute("""
            UPDATE reservations
            SET end_date = ?,
                start_date = ?,
                pick_up_address = ?,
                drop_off_address = ?,
                total_cost = ?,
                trotinette_id = ?,
                user_id = ?,
                options = ?
            WHERE id_reservation = ?
        """, (date_pick_up, date_return, emplacementRecup, emplacementRetour, totalFacture, idTrotinette, iduser, donnees_encodees, idReservation))
        cursor.commit()

    def get_user_admin(self):
        cursor = self.get_connection().cursor()
        cursor.execute("SELECT users.id_user, users.first_name, users.last_name,"
                       + "users.email, users.date_of_birth, "
                         + "users.phone, users.user_type, users.salt, users.hash," +
                       "addresses.address AS address, addresses.city AS city, addresses.province AS province, addresses.postal_code AS postal_code " +
                       "FROM users " +
                       "INNER JOIN addresses ON users.address_id = addresses.id_address")
        users = cursor.fetchall()
        return users

    def update_user_admin(self, id_user, first_name, last_name, email,  date_of_birth, phone, role, address, city, province, postal_code):
        cursor = self.get_connection().cursor()
        cursor.execute(
            ('UPDATE users SET first_name = ?,last_name = ? , email = ?,  date_of_birth = ?,'
             'phone = ? ,user_type = ? WHERE id_user = ?'),
            (first_name, last_name, email, date_of_birth, phone, role, id_user))
        cursor.execute(
            ('UPDATE addresses SET address = ?, city = ?, province = ?,'
             'postal_code = ? WHERE id_address = (SELECT  address_id  FROM users WHERE id_user = ?)'),
            (address, city, province, postal_code, id_user))
        cursor.connection.commit()

    def delete_user(self, id_user):
        cursor = self.get_connection()
        cursor.execute(
            "DELETE FROM users where id_user = ?", (id_user))
        cursor.commit()

    def update_user_password(self, id, salt, hash):
        cursor = self.get_connection().cursor()
        cursor.execute(
            'UPDATE users SET salt =? ,hash =? where id_user =? ', (salt, hash, id))
        cursor.connection.commit()

    def get_trotinette_info(self, id):
        cursor = self.get_connection().cursor()
        cursor.execute('SELECT * FROM trotinette where id_trotinette=? ', (id,))
        trotinette = cursor.fetchone()
        return trotinette

    def create_support_request(self, user_id, support_option, message):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO support_requests (user_id, support_option, message) VALUES (?, ?, ?)",
            (user_id, support_option, message)
        )
        connection.commit()
        return cursor.lastrowid

    def get_support_request(self, request_id):
        cursor = self.get_connection().cursor()
        cursor.execute("SELECT * FROM support_requests WHERE id = ?", (request_id,))
        return cursor.fetchone()

    def update_support_request_status(self, request_id, status):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE support_requests SET status = ? WHERE id = ?",
            (status, request_id)
        )
        connection.commit()

    def delete_support_request(self, request_id):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM support_requests WHERE id = ?", (request_id,))
        connection.commit()



    def get_user_info(self, id_user):
        cursor = self.get_connection().cursor()
        cursor.execute(("SELECT users.first_name, users.last_name, users.email, users.date_of_birth, users.phone, " +
                        "addresses.address, addresses.country, addresses.city, addresses.province, addresses.postal_code, addresses.id_address " +
                        "FROM users " +
                        "JOIN addresses ON users.address_id = addresses.id_address " +
                        "WHERE users.id_user = ?"),
                       (id_user,))
        user = cursor.fetchone()
        if user is None:
            return None
        else:
            return {
                'firstName': user[0],
                'lastName': user[1],
                'email': user[2],
                'dateOfBirth': user[3],
                'phone': user[4],
                'address': user[5],
                'country': user[6],
                'city': user[7],
                'province': user[8],
                'postalCode': user[9],
                'id_address': user[10]
            }

    def update_user_infos(self, id_user, first_name, last_name, email, date_of_birth, phone, address, country, city, province, postal_code, id_address):
        cursor = self.get_connection().cursor()
        cursor.execute(
            ('UPDATE users set first_name = ?, last_name = ?, email = ?,  date_of_birth = ?,'
             'phone = ?  WHERE id_user = ?'),
            (first_name, last_name, email, date_of_birth, phone, id_user))
        cursor.connection.commit()
        cur = self.get_connection().cursor()
        cur.execute(
            ('UPDATE addresses set address = ?, country = ?, city = ?, province = ?, postal_code = ? WHERE id_address = ?'),
            (address, country, city, province, postal_code, id_address))
        cur.connection.commit()
    def get_all_locations(self):
        cursor = self.get_connection().cursor()
        cursor.execute("SELECT * FROM locations")
        locations = cursor.fetchall()
        return locations

    # Method to get trotinette by ID
    def get_trotinette_by_id(self, id_trotinette):
        cursor = self.get_connection().cursor()
        cursor.execute("SELECT * FROM trotinette WHERE id_trotinette=?", (id_trotinette,))
        return cursor.fetchone()

    # Method to create a reservation
    def create_reservation(self, start_date, end_date, pick_up_address, drop_off_address, total_cost, trotinette_id, user_id, options):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO reservations (start_date, end_date, pick_up_address, drop_off_address, total_cost, trotinette_id, user_id, options) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (start_date, end_date, pick_up_address, drop_off_address, total_cost, trotinette_id, user_id, options)
        )
        connection.commit()

    # Method to update trotinette quantity
    def update_trotinette_quantity(self, id_trotinette, new_quantity):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("UPDATE trotinette SET qte=? WHERE id_trotinette=?", (new_quantity, id_trotinette))
        connection.commit()

    # Method to get user by ID
    def get_user_by_id(self, user_id):
        cursor = self.get_connection().cursor()
        cursor.execute("SELECT * FROM users WHERE id_user=?", (user_id,))
        return cursor.fetchone()

    # Credit card logic 
    def get_credit_card(self, card_number):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM credit_cards WHERE card_number = ?", (card_number,))
        return cursor.fetchone()

    def add_payment_history(self, user_id, amount, card_id):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO payment_history (user_id, amount, card_id) VALUES (?, ?, ?)",
                   (user_id, amount, card_id))
        connection.commit()
        return cursor.lastrowid
        
    
    # Facturation Logic 
    def add_facturation(self, user_id, nom, prenom, adresse, ville, province, code_postal, telephone, montant):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO facturation (nom, prenom, adresse, ville, province, code_postal, telephone, amount, user_id) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (nom, prenom, adresse, ville, province, code_postal, telephone, montant, user_id))
        connection.commit()

    def get_facturation(self, user_id):
        cursor = self.get_connection().cursor()
        cursor.execute("SELECT nom, prenom, adresse, ville, province, code_postal, telephone, amount FROM facturation WHERE user_id = ? ORDER BY date_facturation DESC LIMIT 1", (user_id,))
        facturation = cursor.fetchone()
        if facturation:
            return {
                'nom': facturation[0],
                'prenom': facturation[1],
                'adresse': facturation[2],
                'ville': facturation[3],
                'province': facturation[4],
                'codePostal': facturation[5],
                'telephone': facturation[6],
                'montant': facturation[7]
            }
        return None

    def update_facturation(self, user_id, nom, prenom, adresse, ville, province, code_postal, telephone, montant):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(
        "UPDATE facturation SET nom = ?, prenom = ?, adresse = ?, ville = ?, "
        "province = ?, code_postal = ?, telephone = ?, amount = ? WHERE user_id = ?",
        (nom, prenom, adresse, ville, province, code_postal, telephone, montant, user_id))
        connection.commit()