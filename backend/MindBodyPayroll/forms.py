from wtforms import StringField, FloatField, Form


class AppendForm(Form):
    amount = FloatField('Amount')
    description = StringField('Description')
