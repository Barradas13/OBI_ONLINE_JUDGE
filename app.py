from flask import Flask, render_template, jsonify
import json, os

app = Flask(__name__)

@app.route("/")
def index():
    files = os.listdir("problems")
    problems = [f.replace(".json", "") for f in files]
    return render_template("templates/base.html", problems=problems)

@app.route("/problem/<pid>")
def problem(pid):
    with open(f"problems/{pid}.json") as f:
        data = json.load(f)
    return render_template("templates/problem.html", problem=data)

if __name__ == "__main__":
    app.run(debug=True)
