from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,SelectField, TextAreaField,ValidationError,RadioField
from wtforms.validators import Required,Email,EqualTo


class UpdateProfile(FlaskForm):
    bio=TextAreaField('write a brief bio about you.', validators=[Required()])
    submit=SubmitField('save')


class PitchForm(FlaskForm):
    title=StringField('Title', validators=[Required()])
    category=SelectField('Category',choices=[ ('education','education'), ('music','music'),('religion','religion'),], validators=[Required()])
    post=TextAreaField('Your Pitch.', validators=[Required()])
    submit=SubmitField('Pitch')

class CommentForm(FlaskForm):
    comment=TextAreaField('Leave a comment',validators=[Required()])
    submit=SubmitField('Comment')
       
  