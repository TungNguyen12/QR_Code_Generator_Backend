from flask import Flask, render_template
from flask_cors import CORS

# Corrected relative imports for submodules within the src package
from src.app.auth.routes import auth
from src.app.qrcodes.routes import qrcodes
from src.app.analytics.routes import analytics

# Corrected relative import for configurations
from src.config import DEBUG, HOST, PORT, SECRET_KEY

# Initialize the Flask application
app = Flask(__name__)
# Enable Cross-Origin Resource Sharing (CORS) for all routes
CORS(app)

# Register blueprints for authentication, QR codes, and analytics
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(qrcodes, url_prefix='/qrcodes')
app.register_blueprint(analytics, url_prefix='/')

# Define the route for the index page
@app.route('/')
def index():
    """Renders the index.html template."""
    # Render the 'index.html' template for the root route
    return render_template('index.html')