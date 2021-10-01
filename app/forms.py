from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired

class LabelForm(FlaskForm):
    labeltext = TextAreaField('Label Text', validators=[DataRequired()], render_kw={"rows": 4, "cols": 80})
    generate_pdf_only = BooleanField('Generate PDF only')
    submit = SubmitField('Print label')
