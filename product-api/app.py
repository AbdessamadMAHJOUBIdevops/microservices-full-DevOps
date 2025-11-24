from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Important pour que React puisse nous parler !

# Notre base de données simulée
products = [
    {"id": 1, "name": "MacBook Pro M2", "price": 1999, "image": "💻"},
    {"id": 2, "name": "Iphone 15", "price": 999, "image": "📱"},
    {"id": 3, "name": "Casque Sony WH-1000XM5", "price": 350, "image": "🎧"},
    {"id": 4, "name": "Clavier Mécanique", "price": 120, "image": "⌨️"}
]

@app.route('/products', methods=['GET'])
def get_products():
    print("📞 Appel reçu : Quelqu'un veut la liste des produits !")
    return jsonify(products)

@app.route('/', methods=['GET'])
def health_check():
    return jsonify({"status": "alive", "service": "product-api"})

if __name__ == '__main__':
    # On écoute sur le port 5000
    app.run(host='0.0.0.0', port=5000, debug=True)
