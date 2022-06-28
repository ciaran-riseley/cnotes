from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash,check_password_hash
from functools import wraps
import uuid
import jwt
import datetime

import os





app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SECRET_KEY']=os.environ.get('SECRET_KEY')
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(32), index = True)
    password = db.Column(db.String(255))

class Note(db.Model):
    __tablename__ = 'notes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(255))
    text = db.Column(db.String(8192))


db.create_all()



def token_required(f):
   @wraps(f)
   def decorator(*args, **kwargs):
       token = None
       if 'x-access-tokens' in request.headers:
           token = request.headers['x-access-tokens']
 
       if not token:
           return jsonify({'message': 'a valid token is missing'})
       try:
           data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
           current_user = User.query.filter_by(id=data['id']).first()
       except:
           return jsonify({'message': 'token is invalid'})
 
       return f(current_user, *args, **kwargs)
   return decorator


@app.route('/login', methods=['POST']) 
def login_user():
    auth = request.authorization  
    if not auth or not auth.username or not auth.password: 
        return make_response('could not verify', 401, {'Authentication': 'login required"'})   
    
    user = User.query.filter_by(email=auth.username).first()  
    print(user)
    print(user.email)
    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'email' : user.email, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=5)}, app.config['SECRET_KEY'], "HS256")
    
        return jsonify({'token' : token})
    
    return make_response('could not verify',  401, {'Authentication': '"login required"'})


@app.route('/note', methods=['POST'])
@token_required
def create_note(current_user):
 
   data = request.get_json()
 
   new_note = Note(title=data['title'], text=data['text'], user_id=current_user.id) 
   db.session.add(new_note)  
   db.session.commit() 
   return jsonify({'message' : 'new note created'})

@app.route('/api/register', methods = ['POST'])
def new_user():
    email = request.json.get('email')
    password = request.json.get('password')
    if email is None or password is None:
        abort(400) # missing arguments
    if User.query.filter_by(email = email).first() is not None:
        abort(400) # existing user
    user = User(email = email, password = generate_password_hash(password))
    db.session.add(user)
    db.session.commit()
    return jsonify({ 'email': user.email }), 201#, {'Location': url_for('get_user', id = user.id, _external = True)}


if __name__=="__main__":
    

    app.run(debug=True)
    





