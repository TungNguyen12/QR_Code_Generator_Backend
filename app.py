from flask import Flask, render_template
from flask_cors import CORS
from src.app.auth.routes import auth
from src.app.qrcodes.routes import qrcodes




app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(qrcodes, url_prefix='/qrcodes')

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
