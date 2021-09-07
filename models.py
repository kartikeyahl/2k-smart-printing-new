from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

def initialize_db(app):
  app.app_context().push()
  db.init_app(app)
  db.create_all()

class User(UserMixin, db.Model):
    __tablename__ = "userTable"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    password = db.Column(db.String(80),nullable=False)
    lat = db.Column(db.String(15), nullable=False, default="-")
    longi = db.Column(db.String(15), nullable=False, default="--")
    document = db.Column(db.String(150), nullable=False, default="N/A")
    data = db.Column(db.String(500), nullable=False, default="N")
    no_pgs= db.Column(db.String(150), nullable=False, default="----")
    color = db.Column(db.String(150), nullable=False, default="-----")
    laminate= db.Column(db.String(150), nullable=False, default="------")
    bind= db.Column(db.String(150), nullable=False, default="-------")
    additional= db.Column(db.String(150), nullable=False, default="--------")
    progress= db.Column(db.String(150), nullable=False, default="---------")
    status= db.Column(db.String(150), nullable=False, default="----------")
    longi_user = db.Column(db.String(15), nullable=False, default="-----------")
    lat_user = db.Column(db.String(15), nullable=False, default="------------")
    shop_id = db.Column(db.String(15), nullable=False, default="-------------")
    delete= db.Column(db.String(15), nullable=False, default="--------------")
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    



