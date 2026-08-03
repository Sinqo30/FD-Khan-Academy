import os

from werkzeug.utils import secure_filename
from flask import current_app
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user

from ..extensions import db
from ..models import Booking, Course, Video, SiteSetting


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

@admin.route("/courses/edit/<int:course_id>", methods=["GET", "POST"])
@login_required
def edit_course(course_id):

    if not current_user.is_admin:
        return redirect(url_for("student.dashboard"))

    course = Course.query.get_or_404(course_id)

    if request.method == "POST":

        course.title = request.form["title"]
        course.description = request.form["description"]
        course.grade = request.form["grade"]
        course.subject = request.form["subject"]
        course.price = float(request.form["price"])

        print("NEW TITLE:", request.form["title"])

        db.session.commit()

        db.session.refresh(course)
        print("SAVED TITLE:", course.title)

        flash("Course updated successfully!", "success")

        return redirect(url_for("admin.courses"))

    return render_template(
        "edit_course.html",
        course=course
    )

@admin.route("/courses/delete/<int:course_id>")
@login_required
def delete_course(course_id):

    if not current_user.is_admin:
        return redirect(url_for("student.dashboard"))


    course = Course.query.get_or_404(course_id)


    # delete lessons belonging to course first
    lessons = Video.query.filter_by(
        course_id=course.id
    ).all()


    for lesson in lessons:
        db.session.delete(lesson)


    db.session.delete(course)

    db.session.commit()


    flash("Course deleted successfully!", "success")


    return redirect(
        url_for("admin.courses")
    )
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
@admin.route("/lessons/add/<int:course_id>", methods=["GET", "POST"])
@login_required
def add_lesson(course_id):

    if not current_user.is_admin:
        return redirect(url_for("student.dashboard"))

    course = Course.query.get_or_404(course_id)

    if request.method == "POST":

        title = request.form["title"]
        caption = request.form["caption"]
        price = float(request.form["price"])
        order = int(request.form["order"])

        video = request.files["video"]

        filename = secure_filename(video.filename)

        video.save(
            os.path.join(
                current_app.config["UPLOAD_FOLDER"],
                filename
            )
        )

        lesson = Video(
            course_id=course.id,
            title=title,
            caption=caption,
            video_file=filename,
            price=price,
            order=order
        )

        db.session.add(lesson)
        db.session.commit()

        flash("Lesson uploaded successfully!", "success")

        return redirect(
            url_for("admin.manage_lessons", course_id=course.id)
        )

    return render_template(
        "add_lesson.html",
        course=course
    )
@admin.route("/courses/<int:course_id>/lessons")
@login_required
def manage_lessons(course_id):

    if not current_user.is_admin:
        return redirect(url_for("student.dashboard"))

    course = Course.query.get_or_404(course_id)

    lessons = Video.query.filter_by(
        course_id=course.id
    ).order_by(Video.order).all()

    return render_template(
        "manage_lessons.html",
        course=course,
        lessons=lessons
    )
@admin.route("/settings", methods=["GET", "POST"])
@login_required
def settings():

    if not current_user.is_admin:
        return redirect(
            url_for("student.dashboard")
        )

    setting = SiteSetting.query.first()

    if setting is None:

        setting = SiteSetting()

        db.session.add(setting)

        db.session.commit()

    if request.method == "POST":

        setting.paypal_client_id = request.form["paypal_client_id"]

        db.session.commit()

        flash(
            "Settings updated successfully!",
            "success"
        )

        return redirect(
            url_for("admin.settings")
        )

    return render_template(
        "admin_settings.html",
        setting=setting
    )