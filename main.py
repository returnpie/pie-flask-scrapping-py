from flask import Flask, render_template, request, redirect, send_file
from scrapper import get_jobs
from exporter import save_to_file

app = Flask("scrapper")

db = {}


@app.route("/")
def home():
    return render_template("searchform.html")


@app.route("/report")
def report():
    word = request.args.get('word')
    if (word):
        word = word.lower()
        existing_jobs = db.get(word)
        if existing_jobs:
            jobs = existing_jobs
        else:
            jobs = get_jobs(word)
            db[word] = jobs
    else:
        return redirect("/")
    return render_template("report.html", searchingBy=word, resultsNumber=len(jobs), jobs=jobs)


@app.route("/export")
def export():
    try:
        word = request.args.get("word")
        if not word:
            raise Exception()
        word = word.lower()
        jobs = db.get(word)
        if not jobs:
            raise Exception()
        save_to_file(jobs)
        return send_file("jobs.csv")

    except:
        return redirect("/")


app.run()
