# Import the dependencies.
import numpy as np
from numpy import mean
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

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
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of dates and percipitation"""
    # Perform a query to retrieve the data and precipitation scores
    results = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= dt.date(2016, 8, 23)).all()

    session.close()

    # Create a dictionary using date as the key and prcp as the value from the row data and append to a list of all_percipitation
    all_percipitation = []
    for date, prcp in results:
        percipitation_dict = {}
        percipitation_dict[date] = prcp
        all_percipitation.append(percipitation_dict)

    return jsonify(all_percipitation)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of stations from the dataset"""
    # Query all stations
    results = session.query(Station.station).all()

    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of temperature observations"""
    # Using the most active station id
    # Query the last 12 months of temperature observation data for this station
    # Perform a query to retrieve the tobs
    results = session.query(Measurement.tobs).\
    filter(Measurement.date >= dt.date(2016, 8, 23)).\
    filter(Measurement.station == 'USC00519281').all()
    
    session.close()

    # Convert list of tuples into normal list
    all_tobs = list(np.ravel(results))

    return jsonify(all_tobs)


@app.route("/api/v1.0/<start>")
def start(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of min, max, avg temperature observations"""
    # Using the start date, calculate the lowest, highest, and average temperature.
    tobs = session.query(Measurement.tobs).filter(Measurement.date >= dt.date(start)).all()
    list_tobs = []
    tobs_min = list_tobs.append(min(tobs))
    tobs_max = list_tobs.append(max(tobs))
    tobs_avg = list_tobs.append(mean(tobs))
    
    session.close()

    # Convert list of tuples into normal list
    sm_tobs = list(np.ravel(list_tobs))

    return jsonify(sm_tobs)

@app.route("/api/v1.0/<start>/<end>")
def start(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of min, max, avg temperature observations"""
    # Using the start and end date, calculate the lowest, highest, and average temperature.
    tobs = session.query(Measurement.tobs).filter(Measurement.date >= dt.date(start)).\
    filter(Measurement.date <= dt.date(end)).all()
    list_tobs = []
    tobs_min = list_tobs.append(min(tobs))
    tobs_max = list_tobs.append(max(tobs))
    tobs_avg = list_tobs.append(mean(tobs))
    
    session.close()

    # Convert list of tuples into normal list
    sm_tobs = list(np.ravel(list_tobs))

    return jsonify(sm_tobs)

if __name__ == '__main__':
    app.run(debug=True)



