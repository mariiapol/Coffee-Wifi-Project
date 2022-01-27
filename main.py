from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import csv


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField('Cafe Location on Google Maps', validators=[DataRequired(), URL()])
    time_open = StringField('Open time e.g. 8AM', validators=[DataRequired()])
    time_close = StringField('Closing time e.g. 7:30PM', validators=[DataRequired()])
    rating_coffee = SelectField('Coffee Rating', choices=["✘","☕","☕☕","☕☕☕","☕☕☕☕","☕☕☕☕☕"],validators=[DataRequired()])
    rating_wifi = SelectField('Wifi Strength Rating', choices=["✘","💪","💪💪","💪💪💪","💪💪💪💪","💪💪💪💪💪"],validators=[DataRequired()])
    power_rating = SelectField('Power Socket Availability', choices=["✘","🔌","🔌🔌","🔌🔌🔌","🔌🔌🔌🔌","🔌🔌🔌🔌🔌"],validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        # Make the form write a new row into cafe-data.csv
        row = [form.cafe.data, form.location.data, form.time_open.data, form.time_close.data, form.rating_coffee.data, form.rating_wifi.data, form.power_rating.data]

        with open('cafe-data.csv', 'a', newline='', encoding="utf8") as csv_file:
            writer_object = csv.writer(csv_file)
            writer_object.writerow(row)

        return redirect(url_for('cafes'))

    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding="utf8") as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
