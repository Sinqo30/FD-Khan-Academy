from flask import Blueprint, render_template, current_app, redirect, url_for
from flask_login import login_required, current_user

from ..extensions import db
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



@student.route("/courses")
def courses():

    from ..models import Course

    courses = Course.query.all()


    return render_template(
        "student_courses.html",
        courses=courses
    )



@student.route("/course/<int:course_id>")
@login_required
def course(course_id):

    from ..models import Course, Video

    course = Course.query.get_or_404(course_id)

    print("COURSE:", course.id, course.title)

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

    from ..models import Video


    lesson = Video.query.get_or_404(lesson_id)


    purchase = Purchase.query.filter_by(
        student_id=current_user.id,
        video_id=lesson.id,
        payment_status="Completed"
    ).first()


    return render_template(
        "student_lesson.html",
        lesson=lesson,
        purchased=(purchase is not None),
        config=current_app.config
    )



@student.route("/payment-success/<int:lesson_id>")
@login_required
def payment_success(lesson_id):

    from ..models import Video


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