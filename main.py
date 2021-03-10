from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3

def init_sqlite_db():
    conn = sqlite3.connect('database.db')
    conn.execute('CREATE TABLE IF NOT EXISTS register (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT, confirm_password TEXT)')
    print("Table created successfully")



    conn.execute('CREATE TABLE IF NOT EXISTS products(id INTEGER PRIMARY KEY AUTOINCREMENT, item_name TEXT, image TEXT, price DECIMAL(5,2), category TEXT)')
    print("products created successfully")

init_sqlite_db()

app = Flask(__name__)
CORS(app)


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d




@app.route('/add-new/', methods=['POST'])
def add_new_record():

    msg = None
    try:
        post_data = request.get_json()
        username = post_data['username']
        password = post_data['password']
        confirm_password = post_data['confirm_password']

        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute("INSERT INTO register(username, password, confirm_password) VALUES (?, ?, ?)",(username, password, confirm_password))
            con.commit()
            msg = username + " was successfully added to the database."
    except Exception as e:
        con.rollback()
        msg = "Error occurred in insert operation: " + str(e)

    finally:
        con.close()
    return jsonify(msg=msg)


@app.route('/show-sub/', methods=["GET"])
def show_sub():
    if request.method == 'GET':
        try:
            with sqlite3.connect('database.db') as con:
                con.row_factory = dict_factory
                cur = con.cursor()
                cur.execute("SELECT * FROM register")
                records = cur.fetchall()
        except Exception as e:
            con.rollback()
            print("There was an error fetching results from the database: " + str(e))
        finally:
            con.close()
        return jsonify(records)

 #PRODUCTS

# @app.route('/products/', methods=['POST'])
# def list_products():
#     with sqlite3.connect('database.db') as con:
#             con.row_factory = dict_factory
#             cur = con.cursor()
#
#             #BEEF
#             cur.execute("INSERT INTO products(item_name, image, price, category) VALUES (?, ?, ?, ?)", ('Korean style and Kymich Sauce', 'https://i.postimg.cc/02qdR8KJ/korean-syle-kymich-slaw.jpg', 'R119.99', 'beef' ))
#             cur.execute("INSERT INTO products(item_name, image, price, category) VALUES (?, ?, ?, ?)", ('Original Beef Burger', 'https://i.postimg.cc/TPsLfXQb/tumblr-n5441ru-W0-H1rr6inlo1-500.jpg', 'R79,99', 'beef' ))
#
#             #CHEESE
#             cur.execute("INSERT INTO products(item_name, image, price, category) VALUES (?, ?, ?, ?)", ('Cheddar Cheese and Chips', 'https://i.postimg.cc/5yRkmym0/cheddar.jpg', 'R89,99', 'cheese' ))
#             cur.execute("INSERT INTO products(item_name, image, price, category) VALUES (?, ?, ?, ?)", ('Double Cheese', 'https://i.postimg.cc/jdyFfx7s/double-cheese.jpg', 'R119,99', 'cheese' ))
#             cur.execute("INSERT INTO products(item_name, image, price, category) VALUES (?, ?, ?, ?)", ('Spicy Cheese', 'https://i.postimg.cc/L5t3Js0w/SPICY.jpg', 'R99,99', 'cheese' ))
#
#             #DOUBLE
#             cur.execute("INSERT INTO products(item_name, image, price, category) VALUES (?, ?, ?, ?)", ('Frankys Double Bacon', 'https://i.postimg.cc/kGvWnp2d/Frankys-bacon.jpg', 'R189,99', 'double'))
#             cur.execute("INSERT INTO products(item_name, image, price, category) VALUES (?, ?, ?, ?)", ('Street Style', 'https://i.postimg.cc/QCmWLKz8/street.jpg', 'R169,99', 'double'))
#             cur.execute("INSERT INTO products(item_name, image, price, category) VALUES (?, ?, ?, ?)", ('Double Beef with Ogre Sauce', 'https://i.postimg.cc/T1bfmzrZ/orge-sauce.jpg', 'R179,99', 'double'))
#
#             #MINI
#             cur.execute("INSERT INTO products(item_name, image, price, category) VALUES (?, ?, ?, ?)", ('2-for-1 Gourme', 'https://i.postimg.cc/YCHY4k6B/2-for1.jpg', 'R39,99', 'mini'))
#             cur.execute("INSERT INTO products(item_name, image, price, category) VALUES (?, ?, ?, ?)", ('Mini Bacon', 'https://i.postimg.cc/sgHjk4DH/BACON.jpg', 'R39,99', 'mini'))
#             cur.execute("INSERT INTO products(item_name, image, price, category) VALUES (?, ?, ?, ?)", ('Mini Beef Burger and Chips', 'https://i.postimg.cc/TYhHkVF3/images.jpg','R39,99', 'mini'))
#
#
#             #CHICKEN
#             cur.execute("INSERT INTO products(item_name, image, price, category) VALUES (?, ?, ?, ?)", ('Pulled Chicken Burger', 'https://i.postimg.cc/W11rm8H5/double-2-for-1.jpg', 'R99,99', 'chicken'))
#             cur.execute("INSERT INTO products(item_name, image, price, category) VALUES (?, ?, ?, ?)", ('Kutsu Chicken Curry', 'https://i.postimg.cc/y82dJT4g/kutsu-curry-fried.jpg', 'R119,99', 'chicken'))
#             cur.execute("INSERT INTO products(item_name, image, price, category) VALUES (?, ?, ?, ?)", ('Zinger Burger', 'https://i.postimg.cc/QtK5vMQw/spicy.jpg', 'R99,99', 'chicken'))
#
#             #CHEFsSPECIALITY
#             cur.execute("INSERT INTO products(item_name, image, price, category) VALUES (?, ?, ?, ?)", ('Bacon Cheese Burger', 'https://i.postimg.cc/9M2CH8Z2/bacon-cheeseburger.jpg', 'R139,99', 'chefs_speciality'))
#             cur.execute("INSERT INTO products(item_name, image, price, category) VALUES (?, ?, ?, ?)", ('The Animal Box', 'https://i.postimg.cc/cHcZxRBn/animal-style.jpg', 'R199,99', 'chefs_speciality'))
#             cur.execute("INSERT INTO products(item_name, image, price, category) VALUES (?, ?, ?, ?)", ('His and Hers', 'https://i.postimg.cc/NjrKgn92/double-2-for-1.jpg', '189,99', 'chefs_speciality'))
#             cur.execute("INSERT INTO products(item_name, image, price, category) VALUES (?, ?, ?, ?)", ('The Secret One', 'https://i.postimg.cc/Px6Xbbvk/1920x366.jpg', '89,99', 'chefs_speciality'))
#
#             #FAMILY_PLATTER
#             cur.execute("INSERT INTO products(item_name, image, price, category) VALUES (?, ?, ?, ?)", ('Family_platter2', 'https://i.postimg.cc/SxDzVMV6/family-platter2.jpg', 'R249,99', 'family_platter'))
#             cur.execute("INSERT INTO products(item_name, image, price, category) VALUES (?, ?, ?, ?)", ('Family_platter1', 'https://i.postimg.cc/cJ0XtwCf/family-platter4.jpg', 'R249,99', 'family_platter'))
#             cur.execute("INSERT INTO products(item_name, image, price, category) VALUES (?, ?, ?, ?)", ('Family_platter4', 'https://i.postimg.cc/cJ0XtwCf/family-platter4.jpg', 'R119,99', 'family_platter'))
#             cur.execute("INSERT INTO products(item_name, image, price, category) VALUES (?, ?, ?, ?)", ('Family_platter3', 'https://i.postimg.cc/HxSZgnpX/family-platter-3.jpg', 'R219,99', 'family_platter'))
#             cur.execute("INSERT INTO products(item_name, image, price, category) VALUES (?, ?, ?, ?)", ('8_Bacon_Burgers', 'https://i.postimg.cc/dtgf3hG9/x8-bacon-cheese.jpg', 'R219,99', 'family_platter'))
#
#             #FORTHEROAD
#             cur.execute("INSERT INTO products(item_name, image, price, category) VALUES (?, ?, ?, ?)", ('Fried Chicken and Slaw', 'https://i.postimg.cc/k5SsHsZr/fried-chicken-with-slaw.jpg', '59,99', 'for_the_road'))
#             cur.execute("INSERT INTO products(item_name, image, price, category) VALUES (?, ?, ?, ?)", ('Grilled Halomi', 'https://i.postimg.cc/xT9ZbwZX/grilled-halomi-portebello.jpg', '59,99', 'for_the_road'))
#
#             con.commit()
#
# list_products()


@app.route('/show-products/', methods=["GET"])
def show_products():
        try:
            with sqlite3.connect('database.db') as con:
                con.row_factory = dict_factory
                cur = con.cursor()
                cur.execute("SELECT * FROM products")
                records = cur.fetchall()
        except Exception as e:
            con.rollback()
            print("There was an error fetching results from the database: " + str(e))
        finally:
            con.close()
        return jsonify(records)



if __name__ == "__main__":
    app.run(debug=True)
