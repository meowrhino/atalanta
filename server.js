const express = require('express');
const fs = require('fs');
const path = require('path');
const simpleGit = require('simple-git');
const app = express();
const PORT = process.env.PORT || 10000;

app.use(express.json());
app.use(express.static('public'));

const CATALOGO_PATH = path.join(__dirname, 'data', 'catalogo.json');

app.get('/catalogo', (req, res) => {
  const data = fs.readFileSync(CATALOGO_PATH, 'utf-8');
  res.json(JSON.parse(data));
});

app.post('/catalogo', async (req, res) => {
  const jsonData = req.body;
  try {
    fs.writeFileSync(CATALOGO_PATH, JSON.stringify(jsonData, null, 2));
    console.log("✔ Catálogo actualizado localmente");

    // GitHub auto-commit
    const token = process.env.GH_TOKEN;
    const gitUrl = `https://${token}@github.com/meowrhino/atalanta.git`;
    const tmpDir = '/tmp/atalanta-sync';

    // Clona el repo en una carpeta temporal
    const git = simpleGit();
    await git.clone(gitUrl, tmpDir);

    // Reemplaza el catálogo en el repo clonado
    const filePath = path.join(tmpDir, 'data', 'catalogo.json');
    fs.writeFileSync(filePath, JSON.stringify(jsonData, null, 2));

    const repo = simpleGit(tmpDir);
    await repo.add('./data/catalogo.json');
    await repo.commit('actualizado desde interfaz de stock');
    await repo.push('origin', 'main');

    console.log("✔ Cambios enviados a GitHub");

    res.sendStatus(200);
  } catch (err) {
    console.error("❌ Error actualizando el catálogo:", err);
    res.status(500).send("Error actualizando el catálogo.");
  }
});

app.listen(PORT, () => {
  console.log(`Servidor escuchando en http://localhost:${PORT}`);
});