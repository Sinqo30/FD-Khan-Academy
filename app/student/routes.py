from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

from ..extensions import db
from ..models import (
    Booking,
    Purchase,
    Course,
    Video,
    BusinessSettings
)


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



@student.route("/courses")
@login_required
def courses():

    courses = Course.query.all()


    return render_template(
        "student_courses.html",
        courses=courses
    )



@student.route("/course/<int:course_id>")
@login_required
def course(course_id):

    course = Course.query.get_or_404(course_id)


    lessons = Video.query.filter_by(
        course_id=course.id
    ).order_by(Video.order).all()


    return render_template(
        "student_course.html",
        course=course,
        lessons=lessons
    )



@student.route("/lesson/<int:lesson_id>")
@login_required
def lesson(lesson_id):

    lesson = Video.query.get_or_404(lesson_id)


    purchase = Purchase.query.filter_by(
        student_id=current_user.id,
        video_id=lesson.id,
        payment_status="Completed"
    ).first()


    payment_settings = BusinessSettings.query.first()


    return render_template(
        "student_lesson.html",
        lesson=lesson,
        purchased=bool(purchase),
        payment_settings=payment_settings
    )



@student.route("/payment-success/<int:lesson_id>")
@login_required
def payment_success(lesson_id):

    lesson = Video.query.get_or_404(lesson_id)


    existing_purchase = Purchase.query.filter_by(
        student_id=current_user.id,
        video_id=lesson.id,
        payment_status="Completed"
    ).first()


    if not existing_purchase:

        purchase = Purchase(
            student_id=current_user.id,
            video_id=lesson.id,
            amount=lesson.price,
            payment_status="Completed"
        )


        db.session.add(purchase)

        db.session.commit()


    return redirect(
        url_for(
            "student.lesson",
            lesson_id=lesson.id
        )
    )