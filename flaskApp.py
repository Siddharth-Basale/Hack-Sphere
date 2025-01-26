from flask import Flask, render_template, request, jsonify
import csv
import os
import random

app = Flask(__name__)

CSV_FILE = "invoice_data.csv"
FINAL_CSV_FILE = "final.csv"

# Ensure CSV exists
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Company", "Invoice", "Status"])


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/get_invoices", methods=["GET"])
def get_invoices():
    if not os.path.exists(CSV_FILE):
        return jsonify([])

    with open(CSV_FILE, "r") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        data = [row for row in reader]

    return jsonify(data)


@app.route("/update_invoice", methods=["POST"])
def update_invoice():
    data = request.json
    company = data["company"]
    invoice = data["invoice"]

    # Randomly select a status
    status = random.choice(["Valid", "Invalid"])

    with open(CSV_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([company, invoice, status])

    return jsonify({"success": True})


@app.route("/edit_invoice", methods=["POST"])
def edit_invoice():
    data = request.json
    original_invoice = data["original_invoice"]
    updated_invoice = data["updated_invoice"]

    rows = []
    with open(CSV_FILE, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if row[1] == original_invoice:
                row[1] = updated_invoice
                row[2] = "Valid" if len(updated_invoice.strip()) >= 5 else "Invalid"
            rows.append(row)

    with open(CSV_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(rows)

    return jsonify({"success": True})


@app.route("/finalize_invoice", methods=["POST"])
def finalize_invoice():
    data = request.json
    invoice_to_finalize = data["invoice"]

    rows = []
    finalized_row = None
    with open(CSV_FILE, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if row[1] == invoice_to_finalize and row[2] == "Valid":
                finalized_row = row
            else:
                rows.append(row)

    with open(CSV_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(rows)

    if finalized_row:
        with open(FINAL_CSV_FILE, "a", newline="") as file:
            writer = csv.writer(file)
            if os.path.getsize(FINAL_CSV_FILE) == 0:
                writer.writerow(["Company", "Invoice", "Status"])
            writer.writerow(finalized_row)

    return jsonify({"success": True})


if __name__ == "__main__":
    app.run(debug=True)
