from flask import Flask, render_template, redirect, url_for,request, flash, session, send_file
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy  import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bootstrap import Bootstrap
from sqlalchemy import or_ , and_
from models import initialize_db,User,db
import json, math
from math import radians, cos, sin, asin, sqrt
from io import BytesIO

from werkzeug.utils import secure_filename
import os
import urllib.request

from flask_mail import  Mail, Message


app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///data.db'

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
  
def allowed_file(filename):
 return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

bootstrap = Bootstrap(app)
initialize_db(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    lat=StringField('latitude')
    longi=StringField('longitude')
    #remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    lat=StringField('latitude')
    longi=StringField('longitude')



@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit() or request.method=='POST':
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                session['my_id'] = form.username.data
                if user.lat:
                    return redirect(url_for('shome'))
                else:
                    return redirect(url_for('home'))

        return '<h1>Invalid username or password</h1>'
        #return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

    return render_template('index.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit() or request.method=='POST':
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        shop=request.form.get('sk',None)
        new_user = User( username=form.username.data, password=hashed_password, lat=form.lat.data, longi=form.longi.data, status= shop)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
        #return '<h1>New user has been created!</h1>'
        #return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'

    return render_template('index.html', form=form)

@app.route('/home')
@login_required
def home():
    user_id = session.get('my_id', None)
    us = User.query.filter_by(username=user_id).first()
    if us.document!="N/A":
        f=1
        if us.progress=="done":
            c=1
            d=0
        else:
            c=0
            d=1
    else:
        f=0
        c=0
        d=0
    return render_template('hpage.html',post=us,f=f,c=c,d=d)

@app.route('/shome')
@login_required
def shome():
    
    user_id = session.get('my_id', None)
    us = User.query.filter_by(username=user_id).first()
    all_posts = User.query.order_by(User.date_posted).all()
    #al = User.query.filter(User.document!= "N/A").count()
    #aal = User.query.filter(User.progress== "done").count()
    al = User.query.filter(User.shop_id== user_id).count()
    #aal = User.query.filter(and_(User.progress== "done" ,User.shop_id== user_id)).all()
    return render_template('shpage.html', posts=all_posts,al=al,d=user_id)

@app.route('/home/contact')
def contact():
    return render_template('contact.html')

@app.route('/shome/contact')
def contact1():
    return render_template('scontact.html')

@app.route('/home/upload')
def upload():
    return render_template('upload.html')

@app.route('/')
def welcome():
    return render_template("welcome.html")

@app.route('/about')
def about():
    return render_template("about.html")



@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('welcome'))


@app.route('/home/upload/do', methods=['GET', 'POST'])
def upload2():
    file = request.files['inputFile']
    filename = secure_filename(file.filename)
    #user_id = User.query.filter_by(id).first()
    #user_id = User.query.filter_by(id=idd).first()
    user_id = session.get('my_id', None)
    us = User.query.filter_by(username=user_id).first()
    
    if file and allowed_file(file.filename) or request.method=='POST':
        
       us.document = file.filename
       us.data= file.read()
       us.no_pgs= request.form['pages']
       us.color= request.form['color']
       us.laminate= request.form['laminate']
       us.bind= request.form['bind']
       us.additional= request.form['additional']
       us.progress="---------"
       us.delete="--------------"
       us.longi_user= request.form['longg']
       us.lat_user= request.form['latt']
       db.session.commit()
    #return render_template('hpage.html')
       return redirect(url_for('shop'))
    else:
       return 'Invalid Uplaod only txt, pdf, png, jpg, jpeg, gif'
 
    #all_posts = User.query.order_by(User.date_posted).all()
    al = User.query.filter(User.status== "s").all()
    return render_template('upload.html', posts=al)

@app.route('/shop', methods=['GET', 'POST'])
def shop():
    al = User.query.filter(User.status== "s").all()
    user_id = session.get('my_id', None)
    us = User.query.filter_by(username=user_id).first()

    #p=[us.lat_user, us.longi_user]
    #p=list(map(float, p))
    
    count=0
    ls1=[]
    ls2=[]
    for post in al:
            #q=[post.lat, post.longi]
            #q=list(map(float, q))
            lon1 = radians(float(us.longi_user))
            lon2 = radians(float(post.longi))
            lat1 = radians(float(us.lat_user))
            lat2 = radians(float(post.lat))
            dlon = lon2 - lon1
            dlat = lat2 - lat1
            a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        
            c = 2 * asin(sqrt(a))
            
            # Radius of earth in kilometers. Use 3956 for miles
            r = 6371
            
            # calculate the result
            eDistance= c * r
            ls2.append(eDistance)
            ls1.append(post.username)

    #ls3=list(zip(ls1, ls2))
    def Convert(lst):
        res_dct = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)}
        return res_dct

    p=1
    for i in range(len(ls1)):
        ls1.insert(p,ls2[i])
        p+=2
        
    d=Convert(ls1)

    d=sorted(d.items(), key = lambda kv:(kv[1], kv[0]))

    if request.method=='POST':
        us.shop_id = request.form['check2']
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('shop.html', posts=al,d=d)
 

@app.route('/download/<int:idd>')
def download(idd):
    all_posts = User.query.filter_by(id=idd).first()
    return send_file(BytesIO(all_posts.data), attachment_filename='downloaded.pdf', as_attachment=True)

@app.route('/sendif/<int:idd>', methods=['GET','POST'])
def sendif(idd):
    all_posts = User.query.filter_by(id=idd).first()
    all_posts.progress= request.form['check']
    db.session.commit()
    return redirect(url_for('shome'))


@app.route('/sendiff/<int:idd>', methods=['GET','POST'])
def sendiff(idd):
    all_posts = User.query.filter_by(id=idd).first()
    all_posts.delete= request.form['check2']
    db.session.commit()
    return redirect(url_for('shome'))


@app.route('/message', methods=['GET','POST'])
def message():
    if request.method == 'POST':
        em=request.form['email']
        ps=request.form['password']
        ms=request.form['message']
        app.config['DEBUG']=True
        app.config['TESTING']=False
        app.config['MAIL_SERVER']='smtp.gmail.com'
        app.config['MAIL_PORT']=587
        app.config['MAIL_USE_TLS']=True
        app.config['MAIL_USE_SSL']=False
        app.config['MAIL_USERNAME']='kartikeyprit@gmail.com'
        app.config['MAIL_PASSWORD']='Mailid@21'
        app.config['MAIL_DEFAULT_SENDER']='kartikeyprit@gmail.com'

        mail=Mail(app)

        msg=Message('hey', recipients=['2KSmart.Printing@gmail.com'])
        msg.body=ms
        mail.send(msg)
        return render_template('scontact.html')





if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1", port=8080)