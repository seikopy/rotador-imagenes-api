from flask import Flask, request, jsonify, send_file
from PIL import Image
import io

app = Flask(__name__)

@app.route("/rotar", methods=["POST"])
def rotar_imagen():
    if 'imagen' not in request.files:
        return jsonify({"error": "No se recibió archivo 'imagen'"}), 400

    imagen = Image.open(request.files['imagen'])
    ancho, alto = imagen.size

    if ancho > alto:
        imagen = imagen.rotate(270, expand=True)

    img_io = io.BytesIO()
    imagen.save(img_io, format='JPEG')
    img_io.seek(0)

    return send_file(img_io, mimetype='image/jpeg')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)