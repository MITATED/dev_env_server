from wtforms import Form, StringField, TextAreaField, validators


class TaskForm(Form):
    landing_url = StringField('landing_url', [validators.Length(min=10, max=256)])
    tds_url = StringField('tds_url', [validators.Length(min=0, max=256)])
    traffic_type = StringField('traffic_type', [validators.Length(min=3, max=3)])
    email_type = StringField('email_type', [validators.DataRequired()])
    country = StringField('country', [validators.DataRequired()])
