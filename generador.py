import csv
import os
from pathlib import Path

CSV_PATH = Path("csv/cinemafia.csv")

PLANTILLA_HOME = Path("plantilla_home.html")
PLANTILLA_SESION = Path("plantilla_sesion.html")
PLANTILLA_HIST = Path("plantilla_historico.html")

SALIDA_HOME = Path("index.html")
SALIDA_SESIONES = Path("sesiones")
SALIDA_HIST = Path("sesiones-anteriores.html")


def leer_csv_raw():
    with open(CSV_PATH, newline="", encoding="utf-8-sig") as f:
        return list(csv.reader(f))


def leer_home():
    rows = leer_csv_raw()

    headers = rows[0]
    data = rows[1:]

    for row in data:
        if not any(row):
            continue

        fila = dict(zip(headers, row))

        if fila.get("NEW SESSION", "").strip().upper() == "TRUE":
            return fila

    raise Exception("No encontré ninguna fila con NEW SESSION = TRUE")


def leer_historico():
    rows = leer_csv_raw()

    start = None
    for i, row in enumerate(rows):
        if len(row) > 1 and row[1].strip().upper() == "SESION":
            start = i
            break

    if start is None:
        raise Exception("No encontré la tabla de histórico")

    headers = rows[start]
    data = rows[start + 1:]

    filas = []
    for row in data:
        if not any(row):
            continue
        filas.append(dict(zip(headers, row)))

    return filas


def generar_home():
    nueva = leer_home()

    html = PLANTILLA_HOME.read_text(encoding="utf-8")

    reemplazos = {
        "{{NUMERO}}": nueva.get("NUMERO", ""),
        "{{FECHA}}": nueva.get("FECHA", ""),
        "{{HORA}}": nueva.get("HORA", ""),
        "{{SEDE}}": nueva.get("SEDE", ""),
        "{{MAPS}}": nueva.get("MAPS", ""),
        "{{FOTO}}": nueva.get("FOTO", ""),
    }

    for clave, valor in reemplazos.items():
        html = html.replace(clave, str(valor))

    SALIDA_HOME.write_text(html, encoding="utf-8")
    print("✅ index.html generado correctamente")


def generar_sesiones():
    filas = leer_historico()
    SALIDA_SESIONES.mkdir(exist_ok=True)

    lista_html = ""

    BASE_URL = "/cinemafia-web"  # GitHub Pages
    # BASE_URL = ""  # <-- usar esto si pruebas en local

    for fila in filas:
        if fila.get("ACTIVA", "").strip().upper() != "TRUE":
            continue

        sesion = fila.get("SESION", "").strip()
        sede = fila.get("SEDE", "").strip()
        fecha = fila.get("FECHA", "").strip()
        carpeta = fila.get("CARPETA_FOTOS", "").strip().lower()
        rating = fila.get("RATING", "").strip()

        if not sesion:
            continue

        ruta_assets = Path("assets") / carpeta
        media_html = ""

        if ruta_assets.exists():
            for archivo in sorted(os.listdir(ruta_assets)):

                ruta = f"{BASE_URL}/assets/{carpeta}/{archivo}"

                if archivo.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
                    media_html += f'<img src="{ruta}">\n'

                elif archivo.lower().endswith((".mp4", ".mov")):
                    media_html += f'<video controls src="{ruta}"></video>\n'

        html = PLANTILLA_SESION.read_text(encoding="utf-8")
        html = html.replace("{{SESION}}", sesion)
        html = html.replace("{{SEDE}}", sede)
        html = html.replace("{{FECHA}}", fecha)
        html = html.replace("{{MEDIA}}", media_html)

        salida = SALIDA_SESIONES / f"{sesion}.html"
        salida.write_text(html, encoding="utf-8")

        lista_html += f'<a class="item" href="sesiones/{sesion}.html">📷 Cinemafia {sesion} · {fecha} · {sede} · ⭐ {rating}</a>\n'

    html_hist = PLANTILLA_HIST.read_text(encoding="utf-8")
    html_hist = html_hist.replace("{{LISTA}}", lista_html)

    SALIDA_HIST.write_text(html_hist, encoding="utf-8")
    print("✅ sesiones generadas")


if __name__ == "__main__":
    generar_home()
    generar_sesiones()