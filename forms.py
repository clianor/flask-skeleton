from flask_wtf import FlaskForm
from werkzeug.security import check_password_hash
from wtforms import StringField
from wtforms import PasswordField
from wtforms.validators import DataRequired, EqualTo

from models import Fcuser


class RegisterForm(FlaskForm):
    userid = StringField('userid', validators=[DataRequired()])
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired(), EqualTo('repassword')])
    repassword = PasswordField('repassword', validators=[DataRequired()])


class LoginForm(FlaskForm):

    class UserPassword(object):
        def __init__(self, message=None):
            self.message = message

        def __call__(self, form, field):
            userid = form['userid'].data
            password = field.data

            fcuser = Fcuser.query.filter_by(userid=userid).first()
            if check_password_hash(fcuser.password, password):
                raise ValueError('Wrong password')

    userid = StringField('userid', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired(), UserPassword()])
