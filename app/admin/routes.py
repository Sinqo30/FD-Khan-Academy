import os

from werkzeug.utils import secure_filename

from flask import (
    current_app,
    Blueprint,
    render_template,
    redirect,
    url_for,
    request,
    flash
)

from flask_login import login_required, current_user

from ..extensions import db
<<<<<<< HEAD
from ..models import Booking, Course, Video, SiteSetting
=======

from ..models import (
    Booking,
    Course,
    Video,
    BusinessSettings
)
>>>>>>> restore-de6a5d5


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
        return redirect(
            url_for("student.dashboard")
        )

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

        flash(
            "Course added successfully!",
            "success"
        )

        return redirect(
            url_for("admin.courses")
        )

    return render_template(
        "add_course.html"
    )



@admin.route("/courses/edit/<int:course_id>", methods=["GET","POST"])
@login_required
def edit_course(course_id):

    if not current_user.is_admin:
        return redirect(
            url_for("student.dashboard")
        )

    course = Course.query.get_or_404(course_id)


    if request.method == "POST":

        course.title = request.form["title"]

        course.description = request.form["description"]

        course.grade = request.form["grade"]

        course.subject = request.form["subject"]

        course.price = float(
            request.form["price"]
        )


        db.session.commit()


        flash(
            "Course updated!",
            "success"
        )


        return redirect(
            url_for("admin.courses")
        )


    return render_template(
        "edit_course.html",
        course=course
    )



@admin.route("/courses/delete/<int:course_id>")
@login_required
def delete_course(course_id):

    if not current_user.is_admin:
        return redirect(
            url_for("student.dashboard")
        )


    course = Course.query.get_or_404(course_id)


    lessons = Video.query.filter_by(
        course_id=course.id
    ).all()


    for lesson in lessons:
        db.session.delete(lesson)


    db.session.delete(course)

    db.session.commit()


    flash(
        "Course deleted!",
        "success"
    )


    return redirect(
        url_for("admin.courses")
    )



# =========================
# BOOKINGS
# =========================


@admin.route("/booking/<int:booking_id>/approve")
@login_required
def approve_booking(booking_id):

    if not current_user.is_admin:
        return redirect(
            url_for("student.dashboard")
        )


    booking = Booking.query.get_or_404(
        booking_id
    )


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


    booking = Booking.query.get_or_404(
        booking_id
    )


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


    booking = Booking.query.get_or_404(
        booking_id
    )


    db.session.delete(
        booking
    )

    db.session.commit()


    return redirect(
        url_for("admin.dashboard")
    )



# =========================
# LESSONS
# =========================


@admin.route("/lessons/add/<int:course_id>", methods=["GET","POST"])
@login_required
def add_lesson(course_id):

    if not current_user.is_admin:
        return redirect(
            url_for("student.dashboard")
        )


    course = Course.query.get_or_404(
        course_id
    )


    if request.method == "POST":

        video = request.files["video"]


        filename = secure_filename(
            video.filename
        )


        video.save(
            os.path.join(
                current_app.config["UPLOAD_FOLDER"],
                filename
            )
        )


        lesson = Video(

            course_id=course.id,

            title=request.form["title"],

            caption=request.form["caption"],

            video_file=filename,

            price=float(
                request.form["price"]
            ),

            order=int(
                request.form["order"]
            )
        )


        db.session.add(
            lesson
        )

        db.session.commit()


        flash(
            "Lesson uploaded!",
            "success"
        )


        return redirect(
            url_for(
                "admin.manage_lessons",
                course_id=course.id
            )
        )


    return render_template(
        "add_lesson.html",
        course=course
    )



@admin.route("/courses/<int:course_id>/lessons")
@login_required
def manage_lessons(course_id):

    if not current_user.is_admin:
        return redirect(
            url_for("student.dashboard")
        )


    course = Course.query.get_or_404(
        course_id
    )


    lessons = Video.query.filter_by(
        course_id=course.id
    ).order_by(
        Video.order
    ).all()


    return render_template(
        "manage_lessons.html",
        course=course,
        lessons=lessons
    )
<<<<<<< HEAD
@admin.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
=======



@admin.route("/lessons/edit/<int:lesson_id>", methods=["GET","POST"])
@login_required
def edit_lesson(lesson_id):
>>>>>>> restore-de6a5d5

    if not current_user.is_admin:
        return redirect(
            url_for("student.dashboard")
        )

<<<<<<< HEAD
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
=======

    lesson = Video.query.get_or_404(
        lesson_id
    )


    if request.method == "POST":

        lesson.title = request.form["title"]

        lesson.caption = request.form["caption"]

        lesson.price = float(
            request.form["price"]
        )

        lesson.order = int(
            request.form["order"]
        )


        db.session.commit()


        flash(
            "Lesson updated!",
            "success"
        )


        return redirect(
            url_for(
                "admin.manage_lessons",
                course_id=lesson.course_id
            )
        )


    return render_template(
        "edit_lesson.html",
        lesson=lesson
    )



@admin.route("/lessons/delete/<int:lesson_id>")
@login_required
def delete_lesson(lesson_id):

    if not current_user.is_admin:
        return redirect(
            url_for("student.dashboard")
        )


    lesson = Video.query.get_or_404(
        lesson_id
    )


    course_id = lesson.course_id


    db.session.delete(
        lesson
    )


    db.session.commit()


    flash(
        "Lesson deleted!",
        "success"
    )


    return redirect(
        url_for(
            "admin.manage_lessons",
            course_id=course_id
        )
    )



# =========================
# PAYPAL SETTINGS
# =========================


@admin.route("/payment-settings", methods=["GET","POST"])
@login_required
def payment_settings():

    if not current_user.is_admin:
        return "Unauthorized"


    settings = BusinessSettings.query.first()


    if not settings:

        settings = BusinessSettings()

        db.session.add(settings)

        db.session.commit()



    if request.method == "POST":

        settings.paypal_client_id = request.form[
            "paypal_client_id"
        ]

        settings.currency = request.form[
            "currency"
        ]


        db.session.commit()


        flash(
            "Payment settings updated!",
            "success"
        )


    return render_template(
        "admin_payment_settings.html",
        settings=settings
    )
from ..models import User
@admin.route("/users")
@login_required
def users():

    if not current_user.is_admin:
        return redirect(
            url_for("student.dashboard")
        )

    users = User.query.all()

    return render_template(
        "admin_users.html",
        users=users
    )


@admin.route("/users/make-admin/<int:user_id>")
@login_required
def make_admin(user_id):

    if not current_user.is_admin:
        return redirect(
            url_for("student.dashboard")
        )

    user = User.query.get_or_404(user_id)

    user.is_admin = True

    db.session.commit()

    flash(
        "User is now an admin!",
        "success"
    )

    return redirect(
        url_for("admin.users")
    )
@admin.route("/users/remove-admin/<int:user_id>")
@login_required
def remove_admin(user_id):

    if not current_user.is_admin:
        return redirect(
            url_for("student.dashboard")
        )

    user = User.query.get_or_404(user_id)

    # Prevent removing yourself
    if user.id == current_user.id:
        flash(
            "You cannot remove your own admin access.",
            "danger"
        )

        return redirect(
            url_for("admin.users")
        )


    user.is_admin = False

    db.session.commit()


    flash(
        "Admin access removed.",
        "success"
    )


    return redirect(
        url_for("admin.users")
>>>>>>> restore-de6a5d5
    )