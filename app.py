from flask import Flask, render_template, request, redirect
import json
from datetime import datetime

app = Flask(__name__)

DATA_FILE = "data.json"

def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

@app.route("/")
def index():
    data = load_data()
    total_income = sum(t["amount"] for t in data if t["type"] == "income")
    total_expense = sum(t["amount"] for t in data if t["type"] == "expense")
    balance = total_income - total_expense
    return render_template("index.html", transactions=data, income=total_income, expense=total_expense, balance=balance)

@app.route("/add", methods=["GET", "POST"])
def add_transaction():
    if request.method == "POST":
        t_type = request.form["type"]
        amount = float(request.form["amount"])
        category = request.form["category"]
        date = request.form["date"] or str(datetime.today().date())

        transaction = {
            "type": t_type,
            "amount": amount,
            "category": category,
            "date": date
        }

        data = load_data()
        data.append(transaction)
        save_data(data)
        return redirect("/")

    return render_template("add.html")

if __name__ == "__main__":
    app.run(debug=True)
