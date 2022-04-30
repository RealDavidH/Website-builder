from flask import Flask
from flask_bcrypt import Bcrypt
import cloudinary

cloudinary.config( 
  cloud_name = "der4qbefc", 
  api_key = "485755482249258", 
  api_secret = "fxqrT8N6DKb_60WVyBPCm7G4MHo" 
)


app = Flask(__name__)
bcrypt = Bcrypt(app)
DATABASE = "pythonprojectdb"
app.secret_key = 'kekekekeke'
