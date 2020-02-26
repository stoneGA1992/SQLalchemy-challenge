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
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to the table
Measurement = Base.classes.measurement
Station = Base.classes.station
date = dt.datetime(2016, 8, 22)
start_date = dt.datetime(2011, 2, 28)
end_date = dt.datetime(2012, 3, 5)

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
        f"/api/v1.0/stations"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Returns precipitation"""
    # Query
    results = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date > date).order_by(Measurement.date).all()

    session.close()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))

    return jsonify(all_names)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Returns stations"""
    # Query
    results2 = session.query(Measurement.station, func.count(Measurement.station)).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()


    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results2))

    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Returns tobs"""
    # Query
    results3 = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date > date).order_by(Measurement.date).all()


    session.close()

    # Convert list of tuples into normal list
    all_tobs = list(np.ravel(results3))

    return jsonify(all_tobs)


if __name__ == '__main__':
    app.run(debug=True)


@app.route("/api/v1.0/<start>")
def start(start_date):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Returns start"""
    # Query
    results4 = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()


    session.close()

    # Convert list of tuples into normal list
    all_start = list(np.ravel(results4))

    return jsonify(all_start)


@app.route("/api/v1.0//<start>/<end>")
def start_end():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Returns start"""
    # Query
    results5 = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()


    session.close()

    # Convert list of tuples into normal list
    all_start_end = list(np.ravel(results5))

    return jsonify(all_start_end)




if __name__ == '__main__':
    app.run(debug=True)