from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from mercado.models import User

class Cadastroform(FlaskForm):
     def validate_username(self, check_user):
          user = User.query.filter_by(Usuario = check_user.data).first()
          if user:
               raise ValidationError("Usuário já existe! Cadastre outro nome de usuário.")
     def validate_email(self, check_email):
          email = User.query.filter_by(email = check_email.data).first()
          if email: 
              raise ValidationError("Email já existe! Cadastre outro email.")
 
     def validate_senha(self, check_senha):
          senha = User.query.filter_by(senha = check_senha.data).first()
          if senha:
               raise ValidationError("Senha já existe! Cadastre outra senha.")
         

     usuario = StringField(label='Username: ', validators=[Length(min=2, max=30), DataRequired()])
     email = StringField(label = 'E-mail:', validators=[Email(),DataRequired()])
     senha1 = PasswordField(label='senha: ', validators=[Length(min=6),DataRequired()])
     senha2 = PasswordField(label='Comfirmação de senha: ',validators=[EqualTo('senha1'),DataRequired()])
     submit=SubmitField(label='Cadastrar')

class LoginForm(FlaskForm):
     usuario = StringField(label="Usuario", validators=[DataRequired()])
     senha1 = PasswordField(label="Senha", validators=[DataRequired()])
     submit = SubmitField(label="Login")