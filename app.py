import os
from os.path import join, dirname 
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify, send_from_directory
from pymongo import MongoClient
from werkzeug.utils import secure_filename

# Set up
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME = os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]
app = Flask(__name__)

# Konfigurasi folder penyimpanan
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/save_material", methods=["POST"])
def save_material():
    # Proses upload gambar
    image = request.files['image']
    image_filename = secure_filename(image.filename)
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
    image.save(image_path)

    # Simpan informasi lain
    price = 5000  # Harga tetap
    type = request.form['type']
    location = request.form['location']

    doc = {
        'image': image_path,  # simpan path gambar
        'price': price,
        'type': type,
        'location': location
    }
    db.materials.insert_one(doc)
    return jsonify({'msg': 'Material saved successfully!'})

@app.route("/save_product", methods=["POST"])
def save_product():
    # Proses upload gambar
    image = request.files['image']
    image_filename = secure_filename(image.filename)
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
    image.save(image_path)

    # Simpan informasi produk
    name = request.form['name']
    price = request.form['price']
    location = request.form['location']

    doc = {
        'image': image_path,  # simpan path gambar
        'name': name,
        'price': price,
        'location': location
    }
    db.products.insert_one(doc)
    return jsonify({'msg': 'Product saved successfully!'})

@app.route("/products", methods=["GET"])
def get_products():
    products = list(db.products.find({}, {'_id': False}))
    return jsonify({'products': products})

@app.route('/hasil')
def hasil():
    materials = list(db.materials.find({}, {'_id': False}))
    products = list(db.products.find({}, {'_id': False}))
    return render_template('hasil.html', materials=materials, products=products)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/about')
def about():
    return render_template('about.html')  # Menambahkan route untuk halaman About

@app.route('/contact')
def contact():
    return render_template('contact.html')  # Menambahkan route untuk halaman Contact

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
