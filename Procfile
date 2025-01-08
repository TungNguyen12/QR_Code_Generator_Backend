web: gunicorn app:app --bind 0.0.0.0:$PORT

heroku config:set MONGODB_URI="mongodb+srv://qr_code_admin:admin@qrcode.d7rll.mongodb.net/?retryWrites=true&w=majority&appName=QRCode"
 heroku config:set JWT_SECRET_KEY="qr_code_app_jwtkey123"
 heroku config:set SECRET_KEY="qr_code_app_secretkey123"
 heroku config:set DEBUG=False
 heroku config:set ACCESS_TOKEN_EXPIRES=3600
 heroku config:set REFRESH_TOKEN_EXPIRES=86400

 heroku config:set MONGO_URI='mongodb+srv://qr_code_admin:admin@qrcode.d7rll.mongodb.net/?retryWrites=true&w=majority&appName=QRCode' --app qrcodegenerator2025