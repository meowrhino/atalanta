import json
import unicodedata
from bs4 import BeautifulSoup
from pathlib import Path

# Cambia estos nombres si usas archivos distintos
HTML_FILENAME = "ars_brevis.html"
CATALOGO_FILENAME = "catalogo_original.json"
OUTPUT_FILENAME = "catalogo_actualizado.json"
COLECCION_NOMBRE = "Ars Brevis"

def normalizar(texto):
    return unicodedata.normalize("NFKD", texto.lower()).encode("ascii", "ignore").decode("utf-8")

def extraer_libros(html_path):
    with open(html_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "lxml")

    libros = []
    for producto in soup.select("ul.products li.product"):
        nombre = producto.select_one("h2.woocommerce-loop-product__title").text.strip()
        autor = producto.select_one("h3.autor").text.strip()
        link = producto.select_one("a.woocommerce-LoopProduct-link")["href"]
        img = producto.select_one("img")
        portada = img["src"]
        # A veces hay mejores resoluciones en srcset:
        if "srcset" in img.attrs:
            portadas = img["srcset"].split(",")
            # Elige la más pequeña (la que incluye "324x509" si existe)
            for p in portadas:
                url = p.split()[0]
                if "324x" in url:
                    portada = url
                    break

        libros.append({
            "nombre": nombre,
            "autor": autor,
            "link": link,
            "portada": portada
        })
    return libros

def actualizar_catalogo(catalogo_path, libros_extraidos, coleccion):
    with open(catalogo_path, "r", encoding="utf-8") as f:
        catalogo = json.load(f)

    titulos_extraidos = {normalizar(libro["nombre"]): libro for libro in libros_extraidos}

    for item in catalogo:
        titulo_norm = normalizar(item["nombre"])
        if titulo_norm in titulos_extraidos:
            libro = titulos_extraidos[titulo_norm]
            if item.get("link", "") == "":
                item["link"] = libro["link"]
            if item.get("portada", "") == "":
                item["portada"] = libro["portada"]
            if item.get("coleccion", "") == "":
                item["coleccion"] = coleccion

    return catalogo

def main():
    if not Path(HTML_FILENAME).exists():
        print(f"❌ No se encontró el archivo HTML: {HTML_FILENAME}")
        return
    if not Path(CATALOGO_FILENAME).exists():
        print(f"❌ No se encontró el catálogo: {CATALOGO_FILENAME}")
        return

    print("📚 Extrayendo libros...")
    libros = extraer_libros(HTML_FILENAME)

    print("🛠️ Actualizando catálogo...")
    catalogo_actualizado = actualizar_catalogo(CATALOGO_FILENAME, libros, COLECCION_NOMBRE)

    with open(OUTPUT_FILENAME, "w", encoding="utf-8") as f:
        json.dump(catalogo_actualizado, f, indent=2, ensure_ascii=False)

    print(f"✅ Catálogo actualizado guardado en {OUTPUT_FILENAME}")

if __name__ == "__main__":
    main()