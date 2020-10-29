"""Models and database functions for Ratings project."""

from flask_sqlalchemy import SQLAlchemy

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions

class User(db.Model):
    """User of ratings website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(64), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    zipcode = db.Column(db.String(15), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f'user_id={self.user_id} email={self.email}>'


class Movie(db.Model):
    """Movie on ratings website."""

    __tablename__ = "movies"

    movie_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(64))
    released_at = db.Column(db.DateTime)
    imdb_url = db.Column(db.String(200))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Movie movie_id={movie_id} title={title}>".format(
            movie_id=self.movie_id,
            title=self.title)


class Rating(db.Model):
    """Rating of a movie by a user."""

    __tablename__ = "ratings"

    rating_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.movie_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    score = db.Column(db.Integer)

    # Define relationship to user
    user = db.relationship("User",
                           backref=db.backref("ratings", order_by=rating_id))

    # Define relationship to movie
    movie = db.relationship("Movie",
                            backref=db.backref("ratings", order_by=rating_id))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return ("<Rating rating_id={rating_id} movie_id={movie_id} "
                "user_id={user_id} score={score}>").format(
            rating_id=self.rating_id,
            movie_id=self.movie_id,
            user_id=self.user_id,
            score=self.score)


##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///hw_ratings'
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    # So that we can use Flask-SQLAlchemy, we'll make a Flask app
    from flask import Flask

    app = Flask(__name__)

    connect_to_db(app)
    print("Connected to DB.")


# 1.    Find the user with the email cats@gmail.com.
#       User.query.filter_by(email = 'cats@gmail.com').all()
#       user = db.session.query(User).filter(User.email == "cats@gmail.com").one()

# 2.    Find any movies with the exact title “Cape Fear”.
#       Movie.query.filter(Movie.title == 'Cape Fear').all()
#       Movie.query.filter_by(title='Cape Fear').all()

# 3.    Find all users with the zipcode 90703.
#       users = User.query.filter_by(zipcode='90703').all()
#       User.query.filter(User.zipcode == '90703').all()

# 4.    Find all ratings of with the score of 5.
#       Rating.query.filter_by(score = 5).all()
#       ratings_of_five = Rating.query.filter_by(score=5).all()

# 5.    Find the rating for the movie whose id is 7, from the user whose id is 6.
#       Rating.query.filter(Rating.movie_id ==7, Rating.user_id == 6).all()
#       rating = Rating.query.filter_by(user_id=6, movie_id=7).first()

# 6.    Find all ratings that are larger than 3.
        # Rating.query.filter(Rating.score > 3).all()
        # ratings = Rating.query.filter(Rating.score > 3).all()

# db.session.rollback()
