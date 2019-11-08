from flask import Flask, render_template
from parsers.afisha import BaseAfisha as Afisha
from parsers.currrate import BaseCurrRate as CurrRate


app = Flask(__name__)
afisha = Afisha()
curr_rate = CurrRate()

@app.route('/')
def main():
    return render_template('basic.html')

@app.route('/movies/')
def route_afisha():
    films = afisha.get_data()
    return render_template('movies.html', films=films)

@app.route('/courses')
def route_courses():
    courses = curr_rate.get_data()
    return render_template('courses.html', courses=courses)


if __name__ == '__main__':
    app.run()