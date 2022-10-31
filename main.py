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


# first_film = Movie(
#     id=1,
#     title="The Social Network",
#     year=2010,
#     description="Or, I'm Gonna Git You Zuckerberg. Portrayed as an über-ruthless ultra-nerd by Jesse Eisenberg, it's fair to say the Facebook founder came out of David Fincher's social-media drama smelling less of roses than the stuff you grow them in. But it is great drama, expertly wrought by screenwriter Aaron Sorkin, who exploits the story's central paradox (a guy who doesn't get people makes a fortune getting people together online) to supremely juicy effect.",
#     rating=7.3,
#     ranking=5,
#     review="A rich, understated character drama that gleefully exposes the petty playground politics at the centre of one of the internet-era's most bitter court cases.",
#     img_url="https://flxt.tmsimg.com/assets/p8078163_p_v8_ad.jpg"
# )
#
# with app.app_context():
#     db.session.add(first_film)
#     db.session.commit()


if __name__ == '__main__':
    app.run(debug=True)


