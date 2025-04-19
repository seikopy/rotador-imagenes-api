from flask import Flask, request, jsonify, send_file
from PIL import Image
import io
import base64
import requests

app = Flask(__name__)

@app.route("/rotar", methods=["POST"])
def rotar_imagen():
    try:
        if request.is_json:
            data = request.get_json()
            url = data.get("url")
            if not url:
                return jsonify({"error": "Falta la URL"}), 400

            response = requests.get(url)
            if response.status_code != 200:
                return jsonify({"error": "No se pudo descargar la imagen"}), 400

            imagen = Image.open(io.BytesIO(response.content))
        elif 'imagen' in request.files:
            imagen = Image.open(request.files['imagen'])
        else:
            return jsonify({"error": "No se recibió archivo 'imagen' ni 'url'"}), 400

        ancho, alto = imagen.size
        if ancho > alto:
            imagen = imagen.rotate(270, expand=True)

        img_io = io.BytesIO()
        imagen.save(img_io, format='JPEG')
        img_io.seek(0)

        base64_img = base64.b64encode(img_io.read()).decode("utf-8")
        return jsonify({"imagen_base64": base64_img})

    except Exception as e:
        return jsonify({"error": f"Excepción: {str(e)}"}), 500

# ✅ Esto es obligatorio para Render (escucha el puerto asignado)
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
