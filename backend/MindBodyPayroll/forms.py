from wtforms import StringField, FloatField, Form, HiddenField


class AppendForm(Form):
    amount = FloatField('Amount')
    description = StringField('Description')
    id = HiddenField()
    instructor = HiddenField()
    total = HiddenField()
