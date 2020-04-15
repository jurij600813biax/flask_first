from app import db, ma, bcrypt
from datetime import datetime
from marshmallow import Schema, fields
from marshmallow.validate import Length,Email

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100))
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False)
#    number_telephone = db.Column(db.String(16), nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
	    return "<{}:{}>".format(self.id, self.name)

    def set_password(self, password):
    	self.password_hash = bcrypt.generate_password_hash(password)

    def check_password(self, password):
    	return bcrypt.check_password_hash(self.password_hash, password)

class CreateInputSchema(Schema):
    name = fields.Str(required=True, validate=Length(min=1,max=100))
    username = fields.Str(required=True, validate=Length(min=1,max=50))
    email = fields.Str(required=True, validate=Email())
    number_telephone = fields.Int(required=True)
    password = fields.Str(required=True, validate=Length(min=1,max=10))

class CreateLoginSchema(Schema):
    username = fields.Str(required=True, validate=Length(min=1,max=50))
    password = fields.Str(required=True, validate=Length(min=1,max=10))


#class UserSchema(ma.ModelSchema):
#    class Meta:
#       model = User


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name','username','email','created_on','updated_on')
