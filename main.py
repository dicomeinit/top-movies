from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///movies.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Bootstrap(app)


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    ranking = db.Column(db.Integer, nullable=True)
    review = db.Column(db.String(250), nullable=True)
    img_url = db.Column(db.String(250), nullable=False)


class RateMovieForm(FlaskForm):
    rating = StringField("Your Rating Out of 10 e.g. 7.5")
    review = StringField("Your Review")
    submit = SubmitField("Done")


class FindMovieForm(FlaskForm):
    title = StringField("Movie Title", validators=[DataRequired()])
    submit = SubmitField("Add Movie")

# with app.app_context():
#     db.create_all()


@app.route("/")
def home():
    all_movies = Movie.query.all()
    return render_template("index.html", movies=all_movies)


@app.route("/edit", methods=["GET", "POST"])
def rate_movie():
    form = RateMovieForm()
    movie_id = request.args.get("id")
    movie = Movie.query.get(movie_id)
    if form.validate_on_submit():
        movie.rating = float(form.rating.data)
        movie.review = form.review.data
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("edit.html", movie=movie, form=form)


@app.route("/delete")
def delete_movie():
    movie_id = request.args.get('id')
    movie_to_delete = Movie.query.get(movie_id)
    db.session.delete(movie_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


@app.route("/add", methods=["GET", "POST"])
def add_movie():
    form = FindMovieForm()
    return render_template("add.html", form=form)



# third_film = Movie(
#     id=3,
#     title="Up",
#     year=2009,
#     description="A lot has been said about the opening to Pete Docter's Pixar masterpiece, and rightly so, wringing tears from the hardest of hearts with a wordless sequence set to Michael Giacchino's lovely, Oscar-winning score that charts the ups and downs of a couple's marriage. Yet while the majority of the film is more of a straight-ahead adventure tale (albeit one with a wacky bird and talking dogs), that doesn't make it any less satisfying. And let's be honest — the story of a man who uses balloons to float his house to a foreign land, accidentally picking up a young wilderness explorer scout as he does, feels perfectly Pixar.",
#     rating=9.0,
#     ranking=6,
#     review="Inspired by his childhood hero, adventurer Charles F. Muntz (Plummer), and the wishes of his late wife Ellie, octogenarian Carl Fredricksen (Asner) uses a bundle of balloons to fly his house to the jungles of Paradise Falls. His problems start when he discovers a stowaway, boy scout Russell (Nagai).",
#     img_url="https://upload.wikimedia.org/wikipedia/en/0/05/Up_%282009_film%29.jpg"
# )
#
# with app.app_context():
#     db.session.add(third_film)
#     db.session.commit()


if __name__ == '__main__':
    app.run(debug=True)


