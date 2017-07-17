from flask import Flask, redirect, render_template, request, url_for

import os
import sys
import helpers
from analyzer import Analyzer

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search")
def search():
    screen_nm = request.args.get("screen_name", "").lstrip("@")
    if not screen_nm:
        return redirect(url_for("index"))
    positive_value = os.path.join(sys.path[0], "positive-words.txt")
    negative_value = os.path.join(sys.path[0], "negative-words.txt")
    analyzer = Analyzer(positive_value, negative_value)
    tweets = helpers.get_user_timeline(screen_nm, 100)
    if tweets == None:
        return redirect(url_for("index"))
    positive, negative, neutral = 0, 0, 0
    for tweet in tweets:
        score_value = analyzer.analyze(tweet)
        if score_value > 0.0:
            positive += 1
        elif score_value < 0.0:
            negative += 1
        else:
            neutral += 1
    chart = helpers.chart(positive, negative, neutral)

    
    return render_template("search.html", chart=chart, screen_nm=screen_nm)
