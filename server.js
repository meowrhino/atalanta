const express = require("express");
const fs = require("fs");
const path = require("path");

const app = express(); // ← ESTA LÍNEA ES LA QUE FALTABA
const PORT = process.env.PORT || 3000;

const DATA_PATH = path.join(__dirname, "data", "catalogo.json");

app.use(express.json());
app.use(express.static("public"));

// GET /catalogo
app.get("/catalogo", (req, res) => {
  fs.readFile(DATA_PATH, "utf8", (err, data) => {
    if (err) return res.status(500).send("Error leyendo catálogo.");
    res.type("json").send(data);
  });
});

// POST /catalogo
app.post("/catalogo", (req, res) => {
  const nuevoCatalogo = JSON.stringify({ catalogo: req.body.catalogo }, null, 2);
  fs.writeFile(DATA_PATH, nuevoCatalogo, "utf8", (err) => {
    if (err) return res.status(500).send("Error guardando catálogo.");
    res.send({ ok: true });
  });
});

app.listen(PORT, () => {
  console.log(`Servidor escuchando en http://localhost:${PORT}`);
});