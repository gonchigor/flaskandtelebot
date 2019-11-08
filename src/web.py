from flask import Flask, render_template
from parsers.afisha import BaseAfisha as Afisha


app = Flask(__name__)
afisha = Afisha()

@app.route('/')
def main():
    return "Hello"

@app.route('/movies/')
def route_afisha():
    films = afisha.get_data()
    return render_template('movies.html', films=films)


if __name__ == '__main__':
    app.run()