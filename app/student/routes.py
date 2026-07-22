from flask import Blueprint, render_template
from flask_login import login_required, current_user

from ..models import Booking, Purchase


student = Blueprint(
    "student",
    __name__
)


@student.route("/student/dashboard")
@login_required
def dashboard():

    bookings = Booking.query.filter_by(
        student_id=current_user.id
    ).all()


    purchases = Purchase.query.filter_by(
        student_id=current_user.id
    ).all()


    return render_template(
        "student_dashboard.html",
        bookings=bookings,
        purchases=purchases
    )