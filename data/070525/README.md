
# 🐍 Atalanta Parser

Este script sirve para actualizar automáticamente tu catálogo JSON de libros de Ediciones Atalanta, extrayendo los campos `link`, `portada` y `colección` desde fragmentos HTML de las páginas de cada colección.

---

## 🗂 Estructura esperada

```
📁 tu_carpeta_de_trabajo/
│
├── ars_brevis.html
├── imaginatio_vera.html
├── liber_naturae.html
├── memoria_mundi.html
│
├── catalogo.json
├── atalanta_parser.py
```

---

## ✅ Requisitos

1. Python 3.9+
2. Tener instalada la librería `beautifulsoup4` y `lxml`. Si no las tienes:
```bash
python3 -m venv venv
source venv/bin/activate
pip install beautifulsoup4 lxml
```

---

## ▶️ Cómo usar

Desde la terminal, en la carpeta donde tengas los archivos:

```bash
python3 atalanta_parser.py
```

Este script:
- Procesará todos los archivos `.html`.
- Detectará automáticamente la colección por el nombre del archivo.
- Extraerá de cada libro: título, autor, link y portada (tamaño `324x509`).
- Buscará ese título en el `catalogo.json`.
- Si lo encuentra:
  - Si los campos están vacíos: los rellena.
  - Si los campos están llenos: los revisa y actualiza si son incorrectos.
- Si no lo encuentra: te guarda el libro en `libros_no_emparejados.json` para revisión manual.

---

## 📦 Salida esperada

- `catalogo_actualizado.json`: catálogo completo con campos `link`, `portada` y `coleccion` actualizados.
- `libros_no_emparejados.json`: libros que no se han podido emparejar automáticamente.

---

## 💡 Notas

- Asegúrate de que los archivos `.html` solo contengan el `<main>` de cada colección.
- Los nombres de archivo deben ser iguales al nombre de la colección pero en snake_case (por ejemplo: `ars_brevis.html`).

---

## ✨ Autoría

Desarrollado en colaboración con ChatGPT para el proyecto Atalanta 🌒


PD: hay algunos items que debido a que estan en un estuche o que tienen una colección distinta o lo que sea no los ha identificado este script, en ese caso se ha procedido a explciar a chatGPT como funcionaba el script y se buscó en la página de atalanta ese libro y se entregó a chatgpt el main de ese resultado de búsqueda para conseguir los datos

PD2: en caso de estuches como las mil y una noches se ha copiado y pegado el mismo link en link y la misma portada en portada y chao