from flask import Flask, render_template, request, redirect, session, jsonify
import sqlite3


app = Flask(__name__)

app.secret_key = "fd-khan-secret-key"


# =====================
# TIME SLOTS
# =====================

TIME_SLOTS = [

    "08:00", "08:30",
    "09:00", "09:30",
    "10:00", "10:30",
    "11:00", "11:30",
    "12:00", "12:30",
    "13:00", "13:30",
    "14:00", "14:30",
    "15:00", "15:30",
    "16:00", "16:30"

]


# =====================
# DATABASE
# =====================

def get_db():

    conn = sqlite3.connect("fdkhan.db")

    conn.row_factory = sqlite3.Row

    return conn



def init_db():

    conn = get_db()


    conn.execute("""
    CREATE TABLE IF NOT EXISTS bookings(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        name TEXT,

        email TEXT,

        grade TEXT,

        subject TEXT,

        date TEXT,

        time TEXT,

        message TEXT,

        status TEXT DEFAULT 'Pending'

    )
    """)



    conn.execute("""
    CREATE TABLE IF NOT EXISTS blocked_slots(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        date TEXT,

        time TEXT

    )
    """)


    conn.commit()

    conn.close()



init_db()



# =====================
# PAGES
# =====================


@app.route("/")
def home():

    return render_template("index.html")



@app.route("/about")
def about():

    return render_template("about.html")



@app.route("/services")
def services():

    return render_template("services.html")



@app.route("/store")
def store():

    return render_template("store.html")



@app.route("/booking")
def booking():

    return render_template(
        "booking.html"
    )



# =====================
# GET AVAILABLE TIMES
# =====================


@app.route("/get_available_slots")
def get_available_slots():


    date = request.args.get("date")


    conn = get_db()



    blocked = conn.execute(

        """
        SELECT time
        FROM blocked_slots
        WHERE date=?
        """,

        (date,)

    ).fetchall()



    booked = conn.execute(

        """
        SELECT time
        FROM bookings
        WHERE date=?
        """,

        (date,)

    ).fetchall()



    conn.close()



    blocked_times = [

        x["time"]

        for x in blocked

    ]



    booked_times = [

        x["time"]

        for x in booked

    ]



    available = []



    for slot in TIME_SLOTS:


        if (

            slot not in blocked_times

            and

            slot not in booked_times

        ):

            available.append(slot)



    return jsonify(available)





# =====================
# SUBMIT BOOKING
# =====================


@app.route("/submit_booking", methods=["POST"])

def submit_booking():


    date = request.form["date"]

    time = request.form["time"]



    conn = get_db()



    check = conn.execute(

        """
        SELECT *
        FROM bookings
        WHERE date=?
        AND time=?
        """,

        (date,time)

    ).fetchone()



    if check:


        conn.close()


        return """

        <h2>This slot is already booked</h2>

        <a href="/booking">Back</a>

        """




    blocked = conn.execute(

        """
        SELECT *
        FROM blocked_slots
        WHERE date=?
        AND time=?
        """,

        (date,time)

    ).fetchone()




    if blocked:


        conn.close()


        return """

        <h2>This slot is unavailable</h2>

        <a href="/booking">Back</a>

        """




    conn.execute(

        """
        INSERT INTO bookings

        (

        name,

        email,

        grade,

        subject,

        date,

        time,

        message

        )

        VALUES (?,?,?,?,?,?,?)

        """,

        (

        request.form["name"],

        request.form["email"],

        request.form["grade"],

        request.form["subject"],

        date,

        time,

        request.form["message"]

        )

    )



    conn.commit()

    conn.close()



    return redirect("/booking")





# =====================
# ADMIN LOGIN
# =====================


@app.route("/admin", methods=["GET","POST"])

def admin():


    if request.method == "POST":


        username = request.form["username"]

        password = request.form["password"]



        if username == "admin" and password == "1234":


            session["logged_in"] = True


            return redirect("/dashboard")



    return render_template("admin_login.html")






# =====================
# DASHBOARD
# =====================


@app.route("/dashboard")

def dashboard():


    if not session.get("logged_in"):

        return redirect("/admin")



    conn = get_db()



    bookings = conn.execute(

        """

        SELECT *

        FROM bookings

        ORDER BY date,time

        """

    ).fetchall()



    blocked_slots = conn.execute(

        """

        SELECT *

        FROM blocked_slots

        ORDER BY date,time

        """

    ).fetchall()



    conn.close()



    return render_template(

        "admin_dashboard.html",

        bookings=bookings,

        blocked_slots=blocked_slots,

        time_slots=TIME_SLOTS

    )





# =====================
# CONFIRM
# =====================


@app.route("/confirm_booking/<int:id>")

def confirm_booking(id):


    if not session.get("logged_in"):

        return redirect("/admin")



    conn = get_db()



    conn.execute(

        """

        UPDATE bookings

        SET status='Confirmed'

        WHERE id=?

        """,

        (id,)

    )



    conn.commit()

    conn.close()



    return redirect("/dashboard")





# =====================
# DELETE
# =====================


@app.route("/delete_booking/<int:id>")

def delete_booking(id):


    if not session.get("logged_in"):

        return redirect("/admin")



    conn = get_db()



    conn.execute(

        "DELETE FROM bookings WHERE id=?",

        (id,)

    )



    conn.commit()

    conn.close()



    return redirect("/dashboard")






# =====================
# BLOCK SLOT
# =====================


@app.route("/block_slot", methods=["POST"])

def block_slot():


    if not session.get("logged_in"):

        return redirect("/admin")



    conn = get_db()



    date = request.form["date"]



    if "full_day" in request.form:


        for slot in TIME_SLOTS:


            conn.execute(

                """

                INSERT INTO blocked_slots(date,time)

                VALUES (?,?)

                """,

                (date,slot)

            )



    else:


        conn.execute(

            """

            INSERT INTO blocked_slots(date,time)

            VALUES (?,?)

            """,

            (

            date,

            request.form["time"]

            )

        )



    conn.commit()

    conn.close()



    return redirect("/dashboard")






# =====================
# UNBLOCK
# =====================


@app.route("/unblock_slot/<int:id>")

def unblock_slot(id):


    if not session.get("logged_in"):

        return redirect("/admin")



    conn = get_db()



    conn.execute(

        "DELETE FROM blocked_slots WHERE id=?",

        (id,)

    )



    conn.commit()

    conn.close()



    return redirect("/dashboard")





# =====================
# LOGOUT
# =====================


@app.route("/logout")

def logout():


    session.clear()


    return redirect("/admin")





if __name__ == "__main__":

    app.run(debug=True)