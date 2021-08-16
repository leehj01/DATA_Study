from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import PasswordField
from wtforms.validators import DataRequired, EqualTo

class RegisterForm(FlaskForm):
    # 내가 입력받고자 하는 폼을 여기에 넣어주면 됨
    studentid = StringField('studentid', validators=[DataRequired()])
    studentname = StringField('studentname', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired(), EqualTo('repassword')])
    repassword = PasswordField('repassword', validators=[DataRequired()])