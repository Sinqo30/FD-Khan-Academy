from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user

from ..extensions import db
from ..models import Booking, BlockedSlot


booking = Blueprint(
    "booking",
    __name__
)


@booking.route("/booking", methods=["GET", "POST"])
@login_required
def booking_page():

    if request.method == "POST":

        # Check if another student already booked this slot
        existing_booking = Booking.query.filter_by(
            date=request.form["date"],
            time=request.form["time"]
        ).first()

        if existing_booking:

            flash(
                "This time slot has already been booked. Please choose another time.",
                "danger"
            )

            return redirect(
                url_for("booking.booking_page")
            )

        # Check if this student already has a booking at this time
        my_booking = Booking.query.filter_by(
            student_id=current_user.id,
            date=request.form["date"],
            time=request.form["time"]
        ).first()

        if my_booking:

            flash(
                "You already have a booking at this date and time.",
                "danger"
            )

            return redirect(
                url_for("booking.booking_page")
            )

        booking = Booking(

            student_id=current_user.id,

            grade=request.form["grade"],

            subject=request.form["subject"],

            date=request.form["date"],

            time=request.form["time"],

            message=request.form["message"],

            status="Pending"

        )

        db.session.add(booking)

        db.session.commit()

        flash(
            "Your booking has been submitted successfully!",
            "success"
        )

        return redirect(
            url_for("student.dashboard")
        )

    return render_template(
        "booking.html"
    )


@booking.route("/get_available_slots")
@login_required
def get_available_slots():

    date = request.args.get("date")

    all_slots = [
        "08:00",
        "08:30",
        "09:00",
        "09:30",
        "10:00",
        "10:30",
        "11:00",
        "11:30",
        "12:00",
        "12:30",
        "13:00",
        "13:30",
        "14:00",
        "14:30",
        "15:00",
        "15:30",
        "16:00"
    ]

    bookings = Booking.query.filter_by(
        date=date
    ).all()

    booked = [b.time for b in bookings]

    blocked = BlockedSlot.query.filter_by(
        date=date
    ).all()

    for block in blocked:

        if block.whole_day:
            return jsonify([])

        booked.append(block.time)

    available = [
        slot for slot in all_slots
        if slot not in booked
    ]

    return jsonify(available)