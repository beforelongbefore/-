from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo,Length
from app.models import User
from wtforms import TextAreaField


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')



class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')
#当添加任何匹配模式validate_ <field_name>的方法时，WTForms将这些方法作为自定义验证器，并在已设置验证器之后调用它们。
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')

class Decisions1Form(FlaskForm):
    batch = StringField('订货批量', validators=[DataRequired()])
    quality = RadioField('订货质量', choices=[('h','高'),('m','中'),('l','低')],validators=[DataRequired()])
    contract = RadioField('合约类型',choices=[('w','the wholesale price contract'),('m','the buyback contract'),('s','revenue sharing'),('e','EOQ')],validators=[DataRequired()])
    stock = RadioField('库存管理模式',choices=[('t','传统模式'),('c','CS'),('v','VMI')],validators=[DataRequired()])
    submit = SubmitField('保存')

class Decisions2Form(FlaskForm):
    dc = StringField('仓库', validators=[DataRequired()])
    location = StringField('选址', validators=[DataRequired()])
    submit = SubmitField('保存')

class GameForm(FlaskForm):
    ps = StringField('备注', validators=[DataRequired()])
    state = StringField('选址', validators=[DataRequired()])
    submit = SubmitField('保存')

