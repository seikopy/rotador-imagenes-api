from flask import Flask, request, jsonify, send_file
from PIL import Image
import io

app = Flask(__name__)

@app.route("/rotar", methods=["POST"])
def rotar_imagen():
    try:
        if request.is_json:
            data = request.get_json()
            url = data.get("url")
            if not url:
                return jsonify({"error": "Falta la URL"}), 400

            import requests
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

        import base64
        base64_img = base64.b64encode(img_io.read()).decode("utf-8")
        return jsonify({"imagen_base64": base64_img})

    except Exception as e:
        return jsonify({"error": f"Excepción: {str(e)}"}), 500
