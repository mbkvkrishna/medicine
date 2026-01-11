from flask import Flask, render_template, request
from data import medicine_data
from difflib import get_close_matches

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    suggestion = ""
    error = ""

    if request.method == "POST":
        age = int(request.form["age"])
        gender = request.form["gender"]
        disease = request.form["disease"].lower().strip()

        if disease not in medicine_data:
            match = get_close_matches(disease, medicine_data.keys(), 1, 0.6)
            if match:
                suggestion = match[0]
                disease = match[0]
            else:
                error = "No matching disease found"
                return render_template("index.html", error=error)

        data = medicine_data[disease]

        if age < 12:
            group = "child"
        elif age > 60:
            group = "senior"
        else:
            group = "adult"

        precautions = list(data["precautions"])
        if gender == "female":
            precautions.append("Consult a doctor if pregnant or breastfeeding")

        result = {
            "name": disease.title(),
            "description": data["description"],
            "medicines": data[group],
            "precautions": precautions,
            "stores": data["stores"]
        }

    return render_template("index.html", result=result, suggestion=suggestion, error=error)

if __name__ == "__main__":
    app.run()
