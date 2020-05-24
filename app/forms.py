from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email

class AdminUserForm(FlaskForm):
    admin_username = StringField("Username: ", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")

class AdminUserAddForm(FlaskForm):
    admin_username = StringField("Username: ", validators=[DataRequired()])
    password = PasswordField("Password: ", validators=[DataRequired()])
    role = StringField("Role: ", validators=[DataRequired()])
    submit = SubmitField("Submit")
