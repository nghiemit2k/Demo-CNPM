from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from  flask_login import LoginManager
import cloudinary

app = Flask(__name__)
app.secret_key = '@#djjdjdjd$%^'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost/saleapp?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['PAGE_SIZE'] = 8
db = SQLAlchemy(app=app)
admin = Admin(app=app, name="Khai Nghiem", template_mode='bootstrap4')

cloudinary.config(
    cloud_name='dytjbx5cb',
    api_key='456365515787292',
    api_secret='FV_9Uvv86HTs9Skvt8qFYS-H5hk'
)
login = LoginManager(app=app)
