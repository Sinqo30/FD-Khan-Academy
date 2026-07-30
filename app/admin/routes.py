import os

from werkzeug.utils import secure_filename
from flask import current_app
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user

from ..extensions import db
from ..models import Booking, Course, Video


admin = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin"
)


@admin.route("/dashboard")
@login_required
def dashboard():

    if not current_user.is_admin:
        return redirect(
            url_for("student.dashboard")
        )

    bookings = Booking.query.order_by(
        Booking.date,
        Booking.time
    ).all()

    return render_template(
        "admin_dashboard.html",
        bookings=bookings
    )

@admin.route("/courses")

@login_required
def courses():

    if not current_user.is_admin:
        return redirect(
            url_for("student.dashboard")
        )


    courses = Course.query.all()

    return render_template(
    "admin_courses.html",
    courses=courses
)


@admin.route("/courses/add", methods=["GET", "POST"])
@login_required
def add_course():

    if not current_user.is_admin:
        return redirect(url_for("student.dashboard"))

    if request.method == "POST":

        course = Course(
            title=request.form["title"],
            description=request.form["description"],
            grade=request.form["grade"],
            subject=request.form["subject"],
            price=float(request.form["price"])
        )

        db.session.add(course)
        db.session.commit()

        flash("Course added successfully!", "success")

        return redirect(url_for("admin.courses"))

    return render_template("add_course.html")


@admin.route("/booking/<int:booking_id>/approve")
@login_required
def approve_booking(booking_id):

    if not current_user.is_admin:
        return redirect(
            url_for("student.dashboard")
        )

    booking = Booking.query.get_or_404(booking_id)

    booking.status = "Confirmed"

    db.session.commit()

    return redirect(
        url_for("admin.dashboard")
    )


@admin.route("/booking/<int:booking_id>/decline")
@login_required
def decline_booking(booking_id):

    if not current_user.is_admin:
        return redirect(
            url_for("student.dashboard")
        )

    booking = Booking.query.get_or_404(booking_id)

    booking.status = "Declined"

    db.session.commit()

    return redirect(
        url_for("admin.dashboard")
    )


@admin.route("/booking/<int:booking_id>/delete")
@login_required
def delete_booking(booking_id):

    if not current_user.is_admin:
        return redirect(
            url_for("student.dashboard")
        )

    booking = Booking.query.get_or_404(booking_id)

    db.session.delete(booking)

    db.session.commit()

    return redirect(
        url_for("admin.dashboard")
    )
@admin.route("/lessons/add", methods=["GET", "POST"])
@login_required
def add_lesson():

    if not current_user.is_admin:
        return redirect(url_for("student.dashboard"))

    courses = Course.query.all()

    if request.method == "POST":

        title = request.form["title"]
        caption = request.form["caption"]
        price = float(request.form["price"])
        order = int(request.form["order"])
        course_id = int(request.form["course_id"])

        video = request.files["video"]

        filename = secure_filename(video.filename)

        video.save(
            os.path.join(
                current_app.config["UPLOAD_FOLDER"],
                filename
            )
        )

        lesson = Video(
            course_id=course_id,
            title=title,
            caption=caption,
            video_file=filename,
            price=price,
            order=order
        )

        db.session.add(lesson)
        db.session.commit()

        flash("Lesson uploaded successfully!", "success")

        return redirect(url_for("admin.courses"))

    return render_template(
        "add_lesson.html",
        courses=courses
    )