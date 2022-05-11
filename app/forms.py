from flask_wtf import FlaskForm
from wtforms import SubmitField,TextAreaField,StringField,SelectField
from wtforms.validators import DataRequired


class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you',validators=[DataRequired()])
    submit = SubmitField('Submit')

class PitchForm(FlaskForm):
    category = SelectField('Category', choices=[('CHEEZY', 'CHEEZY'), ('PROJECT IDEA', 'PROJECT IDEA'), ('POETIC', 'POETIC'),('FINANCE', 'FINANCE')],
                           validators=[DataRequired()])
    text = TextAreaField('Pitch', validators=[DataRequired()])
    
    submit = SubmitField('Post')
