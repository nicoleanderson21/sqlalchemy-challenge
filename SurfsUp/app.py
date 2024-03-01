# Import the dependencies.

from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/station"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )


@app.route("/api/v1.0/precipitation")
def names():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    last_date = session.query(measurement.date).order_by(measurement.date.desc()).first()   
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    year_prcp = session.query(measurement.date, measurement.prcp).\
    filter(measurement.date >= year_ago, measurement.prcp != None).\
    order_by(measurement.date).all()

    return jsonify(dict(year_prcp))


@app.route("/api/v1.0/stations")
def passengers():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    session.query(measurement.station).distinct().count()

    most_active_stations = session.query(measurement.station,func.count(measurement.station)).\
                               group_by(measurement.station).\
                               order_by(func.count(measurement.station).desc()).all()

    return jsonify(dict(most_active_stations))

@app.route("/api/v1.0/tobs")
def names():
    # Create our session (link) from Python to the DB
    session = Session(engine)
 
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    year_temp = session.query(measurement.tobs).\
        filter(measurement.date >= year_ago, measurement.station == 'USC00519281').\
        order_by(measurement.tobs).all()
    
    temps = []
    for temp in temps:
        temp_dict = {}
        temp_dict["tobs"] = temp.tobs
        temp_dict["age"] = age
        temp_dict["sex"] = sex
        temps.append(passenger_dict)

    return jsonify(dict(year_prcp))

@app.route("/api/v1.0/<start>")
def names():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    last_date = session.query(measurement.date).order_by(measurement.date.desc()).first()   
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    year_prcp = session.query(measurement.date, measurement.prcp).\
    filter(measurement.date >= year_ago, measurement.prcp != None).\
    order_by(measurement.date).all()

    return jsonify(dict(year_prcp))

@app.route("/api/v1.0/<start>/<end>")
def names():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    last_date = session.query(measurement.date).order_by(measurement.date.desc()).first()   
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    year_prcp = session.query(measurement.date, measurement.prcp).\
    filter(measurement.date >= year_ago, measurement.prcp != None).\
    order_by(measurement.date).all()

    return jsonify(dict(year_prcp))

if __name__ == '__main__':
    app.run(debug=True)
