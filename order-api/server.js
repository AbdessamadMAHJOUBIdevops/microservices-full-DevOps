const express = require('express');
const cors = require('cors');
const app = express();
const port = 3001;

app.use(cors());
app.use(express.json());

// Notre base de données simulée (en mémoire)
let orders = [];

app.post('/orders', (req, res) => {
    const newOrder = req.body;
    console.log("💰 NOUVELLE COMMANDE RECUE :", newOrder);
    
    // Simulation d'enregistrement
    orders.push(newOrder);
    
    res.status(201).json({
        message: "Commande validée chef !",
        orderId: orders.length,
        status: "confirmed"
    });
});

app.get('/', (req, res) => {
    res.json({ status: "alive", service: "order-api" });
});

app.listen(port, () => {
    console.log(`🚀 Order API écoute sur le port ${port}`);
});
