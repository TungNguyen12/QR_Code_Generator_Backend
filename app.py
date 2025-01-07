
from dotenv import load_dotenv

load_dotenv()

from flask import Flask, render_template
from flask_cors import CORS
from src.app.auth.routes import auth
from src.app.qrcodes.routes import qrcodes
from src.app.analytics.routes import analytics

from src.config import DEBUG, HOST, PORT, SECRET_KEY


app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(qrcodes, url_prefix='/qrcodes')
app.register_blueprint(analytics, url_prefix='/')

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=DEBUG, host=HOST, port=PORT)
