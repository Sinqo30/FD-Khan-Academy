from flask import Flask, render_template, request, redirect, session
import sqlite3


app = Flask(__name__)

app.secret_key = "fd-khan-secret-key"



# =====================
# DATABASE
# =====================


def get_db():

    conn = sqlite3.connect("fdkhan.db")

    conn.row_factory = sqlite3.Row

    return conn





def init_db():

    conn=get_db()



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


    conn=get_db()


    blocked_slots = conn.execute(
        "SELECT * FROM blocked_slots"
    ).fetchall()



    conn.close()



    return render_template(
        "booking.html",
        blocked_slots=blocked_slots
    )







# =====================
# SUBMIT BOOKING
# =====================



@app.route("/submit_booking", methods=["POST"])

def submit_booking():


    date=request.form["date"]

    time=request.form["time"]



    conn=get_db()





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
        <h2>Slot unavailable</h2>
        <a href="/booking">Back</a>
        """







    booked = conn.execute(

    """

    SELECT *

    FROM bookings

    WHERE date=?

    AND time=?

    """,

    (date,time)

    ).fetchone()






    if booked:


        conn.close()



        return """
        <h2>This time has already been booked</h2>
        <a href="/booking">Choose another time</a>
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
# ADMIN
# =====================



@app.route("/admin", methods=["GET","POST"])

def admin():


    if request.method=="POST":



        if request.form["username"]=="admin" and request.form["password"]=="1234":


            session["logged_in"]=True


            return redirect("/dashboard")




    return render_template("admin_login.html")








@app.route("/dashboard")

def dashboard():


    if not session.get("logged_in"):

        return redirect("/admin")



    conn=get_db()



    bookings=conn.execute(

    """

    SELECT *

    FROM bookings

    ORDER BY date,time

    """

    ).fetchall()





    blocked_slots=conn.execute(

    "SELECT * FROM blocked_slots"

    ).fetchall()




    conn.close()



    return render_template(

    "admin_dashboard.html",

    bookings=bookings,

    blocked_slots=blocked_slots

    )








@app.route("/confirm_booking/<int:id>")

def confirm_booking(id):


    if not session.get("logged_in"):

        return redirect("/admin")



    conn=get_db()



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








@app.route("/delete_booking/<int:id>")

def delete_booking(id):


    if not session.get("logged_in"):

        return redirect("/admin")



    conn=get_db()



    conn.execute(

    "DELETE FROM bookings WHERE id=?",

    (id,)

    )



    conn.commit()

    conn.close()



    return redirect("/dashboard")








@app.route("/block_slot",methods=["POST"])

def block_slot():


    if not session.get("logged_in"):

        return redirect("/admin")



    conn=get_db()



    conn.execute(

    """

    INSERT INTO blocked_slots(date,time)

    VALUES (?,?)

    """,

    (

    request.form["date"],

    request.form["time"]

    )

    )



    conn.commit()

    conn.close()



    return redirect("/dashboard")








@app.route("/logout")

def logout():


    session.clear()


    return redirect("/admin")







if __name__=="__main__":

    app.run(debug=True)