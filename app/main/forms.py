from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,FileField,SubmitField
from wtforms.validators import Required

class CommentForm(FlaskForm):
    title = StringField('Comment title',validators= [Required()])
    comment = TextAreaField('Comment review')
    submit = SubmitField('submit')


class BlogForm(FlaskForm):
    title = StringField('Blog title',validators= [Required()]) 
    message = TextAreaField('Blog Message',validators=[Required()])
    submit = SubmitField('Submit')

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about yourself',validators=[Required()])
    submit = SubmitField('submit')       