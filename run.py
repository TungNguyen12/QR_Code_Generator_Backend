from dotenv import load_dotenv
load_dotenv()
from src import app

from src.config import DEBUG, HOST, PORT, SECRET_KEY

if __name__ == '__main__':
    app.run(debug=DEBUG, host=HOST, port=PORT)