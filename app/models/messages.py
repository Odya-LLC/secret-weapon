from app import db
from datetime import datetime
from hashlib import sha256
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField
from wtforms.validators import DataRequired

def create_hash(text, secret):
    s = text + secret + str(datetime.now())
    return sha256(s.encode('utf-8')).hexdigest()

class SetForm(FlaskForm):
    message = TextAreaField('Message', [DataRequired()])
    secret = PasswordField('Secret', validators=[DataRequired()])
    
class GetForm(FlaskForm):
    hash = StringField('Hash', [DataRequired()])
    secret = PasswordField('Secret', validators=[DataRequired()])

class Messages(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    secret = db.Column(db.String, nullable=False)
    hash = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    @staticmethod
    def set(text, secret):
        h = create_hash(text, secret)
        m = Messages(text=text, secret=secret, hash=h).save()
        
        return h
    
    @staticmethod
    def get(hash, secret):
        m = Messages.query.filter_by(hash=hash, secret=secret).first()
        if m:
            t = m.text
            db.session.delete(m)
            db.session.commit()
            return t
        return None