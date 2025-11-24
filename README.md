# 🛍️ Shop-Mini Project

Ce projet est une démonstration d'architecture microservices pour un portfolio DevOps.

## 📂 Structure

- `/product-api` : Backend Python (Flask) qui gère le catalogue.
- `/order-api` : Backend Node.js (Express) qui gère les commandes.
- `/frontend` : Frontend React (Static) qui consomme les APIs.

## 🚀 Comment lancer le projet (Mode Manuel)

Il faut 3 terminaux ouverts en même temps.

### Terminal 1 : Lancer le service Python
```bash
cd product-api
pip install -r requirements.txt
python app.py
```
> Il doit afficher : `Running on http://0.0.0.0:5000`

### Terminal 2 : Lancer le service Node.js
```bash
cd order-api
npm install
node server.js
```
> Il doit afficher : `Order API écoute sur le port 3001`

### Terminal 3 : Lancer le Frontend
Ouvre simplement le fichier `frontend/index.html` dans ton navigateur (Chrome/Firefox).
Ou utilise un petit serveur web :
```bash
cd frontend
npx serve
```

## 🐳 Prochaine étape : Docker
L'objectif est de créer un `Dockerfile` pour chaque dossier !
