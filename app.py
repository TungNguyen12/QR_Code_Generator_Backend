from flask import Flask, render_template, request, send_file
from flask_cors import CORS
from src.app.auth.routes import auth
import qrcode
import io
from PIL import Image


app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

app.register_blueprint(auth, url_prefix='/auth')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_qr():
    print('Received data:', request.json)

    url = request.json.get('url')  # Using JSON for URL
    foreground_color = request.json.get('foregroundColor', '#000000')  # Default black
    background_color = request.json.get('backgroundColor', '#ffffff')  # Default white
    logo = request.files.get('logo')  # Get logo file if uploaded
    
    if not url:
        return "Error: No URL provided", 400
    
    # Generate QR code
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill=foreground_color, back_color=background_color)

    if logo:
        logo_img = Image.open(logo)
        logo_img = logo_img.resize((50, 50))  # Resize logo as needed
        img.paste(logo_img, ((img.size[0] - logo_img.size[0]) // 2, (img.size[1] - logo_img.size[1]) // 2), logo_img)

    # Save to a BytesIO stream
    img_io = io.BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)

    return send_file(img_io, mimetype='image/png', as_attachment=True, download_name='qrcode.png')

if __name__ == '__main__':
    app.run(debug=True)
