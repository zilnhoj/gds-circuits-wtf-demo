import json
import os

from flask import flash, json, make_response, redirect, render_template, request, url_for
from werkzeug.exceptions import NotFound
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import Range1d

from app import app


@app.route("/")
def index():
    components_ls = os.listdir("govuk_components")
    components_ls.sort()
    # create some data
    x1 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    y1 = [0, 8, 2, 4, 6, 9, 5, 6, 25, 28, 4, 7]
    x2 = [2, 5, 7, 15, 18, 19, 25, 28, 9, 10, 4]
    y2 = [2, 4, 6, 9, 15, 18, 0, 8, 2, 25, 28]
    x3 = [0, 1, 0, 8, 2, 4, 6, 9, 7, 8, 9]
    y3 = [0, 8, 4, 6, 9, 15, 18, 19, 19, 25, 28]

    # select the tools you want
    TOOLS = "pan,wheel_zoom,box_zoom,reset,save"

    # the red and blue graphs share this data range
    xr1 = Range1d(start=0, end=30)
    yr1 = Range1d(start=0, end=30)

    # only the green graph uses this data range
    xr2 = Range1d(start=0, end=30)
    yr2 = Range1d(start=0, end=30)

    # build the figures
    p1 = figure(x_range=xr1, y_range=yr1, tools=TOOLS, width=300, height=300)
    p1.scatter(x1, y1, size=12, color="red", alpha=0.5)

    p2 = figure(x_range=xr1, y_range=yr1, tools=TOOLS, width=300, height=300)
    p2.scatter(x2, y2, size=12, color="blue", alpha=0.5)

    p3 = figure(x_range=xr2, y_range=yr2, tools=TOOLS, width=300, height=300)
    p3.scatter(x3, y3, size=12, color="green", alpha=0.5)

    # plots can be a single Bokeh model, a list/tuple, or even a dictionary
    # plots = {'Red': p1, 'Blue': p2, 'Green': p3}
    plots = (p1, p2, p3)

    script, div = components(plots)
    return render_template("index.html", script=script, div=div, components_ls=components_ls)

@app.route("/start", methods=["GET"])
def start():
    return render_template("start.html")

@app.route("/date", methods=["GET", "POST"])
def date():

    if request.method == "POST":
        cir_date = request.form['dob']
        print(f' circuits - {cir_date}')

        # return redirect("choose-circuit.html")
        return redirect(url_for("choose_circuit"), date=cir_date)
    else:
        date = 'none'
    print('outside of validate on submit if statement')
    return render_template("date.html")

@app.route("/choose-circuit", methods=["GET", "POST"])
def choose_circuit():

    if request.method == "POST":
        cir_session = request.form['choose-a-session']
        print(f'value for choose a session {cir_session}')

        return redirect(url_for("review", cir_session=cir_session))
    return render_template("choose-circuit.html")

@app.route("/review", methods=["GET", "POST"])
def review():

    # if request.method == "POST":
    #
    #     return redirect(url_for("start"))
    return render_template("review.html")

@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_server(error):
    return render_template("500.html"), 500

@app.route("/components/<string:component>")
def component(component):
    try:
        with open("govuk_components/{}/fixtures.json".format(component)) as json_file:
            fixtures = json.load(json_file)
    except FileNotFoundError:
        raise NotFound

    return render_template("component.html", fixtures=fixtures)