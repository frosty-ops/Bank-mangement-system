from flask import Flask, render_template, request, redirect
from database import get_connection

app = Flask(__name__)


@app.route("/")
def dashboard():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT balance FROM account WHERE id = 1")
    result = cursor.fetchone()

    balance = result[0]

    cursor.close()
    connection.close()

    return render_template("dashboard.html", balance=balance)


@app.route("/deposit", methods=["GET", "POST"])
def deposit():

    if request.method == "POST":

        amount = float(request.form["amount"])

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            "UPDATE account SET balance = balance + %s WHERE id = 1",
            (amount,)
        )

        cursor.execute("SELECT balance FROM account WHERE id = 1")
        new_balance = cursor.fetchone()[0]

        cursor.execute(
            "INSERT INTO transactions (type, amount, balance_after) VALUES (%s, %s, %s)",
            ("Deposit", amount, new_balance)
        )

        connection.commit()

        cursor.close()
        connection.close()

        return redirect("/")

    return render_template("deposit.html")


@app.route("/withdraw", methods=["GET", "POST"])
def withdraw():

    if request.method == "POST":

        amount = float(request.form["amount"])

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT balance FROM account WHERE id = 1")
        balance = cursor.fetchone()[0]

        if amount <= balance:

            cursor.execute(
                "UPDATE account SET balance = balance - %s WHERE id = 1",
                (amount,)
            )

            cursor.execute("SELECT balance FROM account WHERE id = 1")
            new_balance = cursor.fetchone()[0]

            cursor.execute(
                "INSERT INTO transactions (type, amount, balance_after) VALUES (%s, %s, %s)",
                ("Withdraw", amount, new_balance)
                )

            connection.commit()

        cursor.close()
        connection.close()

        return redirect("/")

    return render_template("withdraw.html")
@app.route("/history")
def history():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT type, amount, balance_after, transaction_date
        FROM transactions
        ORDER BY id DESC
    """)

    transactions = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template("history.html", transactions=transactions)


if __name__ == "__main__":
    app.run(debug=True)
