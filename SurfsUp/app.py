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

# Database Setup

engine = create_engine("sqlite:////Users/NicoleAnderson/Dropbox/My Mac (Nicole’s MacBook Air)/Documents/GitHub/sqlalchemy-challenge/SurfsUp/Resources/hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

# Flask Setup

app = Flask(__name__)

# Flask Routes

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    
    session = Session(engine)

    last_date = session.query(measurement.date).order_by(measurement.date.desc()).first()   
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    year_prcp = session.query(measurement.date, measurement.prcp).\
    filter(measurement.date >= year_ago, measurement.prcp != None).\
    order_by(measurement.date).all()

    return jsonify(dict(year_prcp))


@app.route("/api/v1.0/stations")
def station():
  
    session = Session(engine)

    session.query(measurement.station).distinct().count()

    most_active_stations = session.query(measurement.station,func.count(measurement.station)).\
                               group_by(measurement.station).\
                               order_by(func.count(measurement.station).desc()).all()

    return jsonify(dict(most_active_stations))

@app.route("/api/v1.0/tobs")
def tobs():
   
    session = Session(engine)
 
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    year_temp = session.query(measurement.tobs).\
        filter(measurement.date >= year_ago, measurement.station == 'USC00519281').\
        order_by(measurement.tobs).all()
    
    temps = []
    for temp in temps:
        temp_dict = {}
        temp_dict["tobs"] = temp.tobs
        temps.append(temp_dict)

    return jsonify(dict(year_temp))

def start_temps(start_date):
    
    return session.query(func.min(measurement.tobs), \
                        func.max(measurement.tobs), \
                        func.avg(measurement.tobs)).\
                        filter(measurement.date >= start_date).all()

@app.route("/api/v1.0/<start>")

def start_date(start):
    start_temp = start_temps(start)
    t_temp= list(np.ravel(start_temp))

    t_min = t_temp[0]
    t_max = t_temp[1]
    t_avg = t_temp[2]
    t_dict = {'Minimum Temperature': t_min, 'Maximum Temperature': t_max, 'Average Temperature': t_avg}

    return jsonify(t_dict)

def temps(start_date, end_date):

    return session.query(func.min(measurement.tobs), \
                         func.max(measurement.tobs), \
                         func.avg(measurement.tobs)).\
                         filter(measurement.date >= start_date).\
                         filter(measurement.date <= end_date).all()

@app.route("/api/v1.0/<start>/<end>")

def start_end_date(start, end):
    
    calc_temp = temps(start, end)
    ta_temp= list(np.ravel(calc_temp))

    tmin = ta_temp[0]
    tmax = ta_temp[1]
    temp_avg = ta_temp[2]
    temp_dict = { 'Minimum Temperature': tmin, 'Maximum Temperature': tmax, 'Average Temperature': temp_avg}

    return jsonify(temp_dict)

if __name__ == '__main__':
    app.run(debug=True)
