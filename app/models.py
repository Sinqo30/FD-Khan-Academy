from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import UserMixin

from .extensions import db

from .extensions import login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    first_name = db.Column(db.String(100), nullable=False)

    last_name = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)

    password_hash = db.Column(db.String(255), nullable=False)

    is_admin = db.Column(db.Boolean, default=False)

    bookings = db.relationship(
        "Booking",
        backref="student",
        lazy=True
    )

    purchases = db.relationship(
        "Purchase",
        backref="student",
        lazy=True
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(
            self.password_hash,
            password
        )


class Booking(db.Model):

    __tablename__ = "bookings"

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(
    db.Integer,
    db.ForeignKey("users.id"),
    nullable=False
)

    grade = db.Column(db.String(20))

    subject = db.Column(db.String(50))

    date = db.Column(db.String(30))

    time = db.Column(db.String(30))

    message = db.Column(db.Text)

    status = db.Column(
        db.String(30),
        default="Pending"
    )


class BlockedSlot(db.Model):

    __tablename__ = "blocked_slots"

    id = db.Column(db.Integer, primary_key=True)

    date = db.Column(db.String(30))

    time = db.Column(db.String(30))

    whole_day = db.Column(
        db.Boolean,
        default=False
    )


class Course(db.Model):

    __tablename__ = "courses"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(200))

    description = db.Column(db.Text)

    grade = db.Column(db.String(20))

    subject = db.Column(db.String(100))

    thumbnail = db.Column(db.String(255))

    price = db.Column(db.Float)


class Video(db.Model):

    __tablename__ = "videos"

    id = db.Column(db.Integer, primary_key=True)

    course_id = db.Column(
        db.Integer,
        db.ForeignKey("courses.id"),
        nullable=False
    )

    title = db.Column(db.String(200))

    caption = db.Column(db.Text)

    video_file = db.Column(db.String(255))

    price = db.Column(db.Float)

    order = db.Column(db.Integer)
class Purchase(db.Model):

    __tablename__ = "purchases"

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    course_id = db.Column(
        db.Integer,
        db.ForeignKey("courses.id"),
        nullable=True
    )

    video_id = db.Column(
        db.Integer,
        db.ForeignKey("videos.id"),
        nullable=True
    )

    amount = db.Column(db.Float)

    payment_status = db.Column(
        db.String(50),
        default="Pending"
    )
<<<<<<< HEAD
class SiteSetting(db.Model):

    __tablename__ = "site_settings"
=======
class BusinessSettings(db.Model):

    __tablename__ = "business_settings"
>>>>>>> restore-de6a5d5

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    paypal_client_id = db.Column(
<<<<<<< HEAD
        db.String(255),
        default=""
=======
        db.String(255)
    )

    paypal_secret = db.Column(
        db.String(255)
    )

    currency = db.Column(
        db.String(10),
        default="USD"
>>>>>>> restore-de6a5d5
    )