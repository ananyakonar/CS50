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

    # validate screen_name
    screen_nm = request.args.get("screen_name", "").lstrip("@")
    if not screen_nm:
        return redirect(url_for("index"))

    # absolute paths to lists
    positive_value = os.path.join(sys.path[0], "positive-words.txt")
    negative_value = os.path.join(sys.path[0], "negative-words.txt")

    # instantiate analyzer
    analyzer = Analyzer(positive_value, negative_value)
    
    # get screen_name's most recent 100 tweets
    tweets = helpers.get_user_timeline(screen_nm, 100)
    
    # return to index if screen_name doesn't exist
    if tweets == None:
        return redirect(url_for("index"))
        
    # create positive, negative and neutral count
    positive, negative, neutral = 0, 0, 0
    
    # analyze each tweet & increase corresponding sentimen count
    for tweet in tweets:
        score_value = analyzer.analyze(tweet)
        if score_value > 0.0:
            positive += 1
        elif score_value < 0.0:
            negative += 1
        else:
            neutral += 1

    # generate chart
    chart = helpers.chart(positive, negative, neutral)

    # render results
    return render_template("search.html", chart=chart, screen_nm=screen_nm)
