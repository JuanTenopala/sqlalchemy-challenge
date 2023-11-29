# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/Hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

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
    return (
        f"Hawaii Climate API<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Query precipitation from last 12 months
    year_date = '2016-08-23'
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= year_date).all()
    # Convert the query results to a dictionary
    precipitation_data = {date: prcp for date, prcp in results}
    return jsonify(precipitation_data)

@app.route("/api/v1.0/stations")
def stations():
    # Query all stations
    results = session.query(Station.station, Station.name).all()
    # Convert the query results to a list of dictionaries
    stations_list = []
    for station, name in results:
        stations_dict = {}
        stations_dict["Station ID"] = station
        stations_dict["Name"] = name
        stations_list.append(stations_dict)
    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs():
    # Query observations
    year_date = '2016-08-23'
    most_active = "USC00519281"
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == most_active).filter(Measurement.date >= year_date).all()
    # Convert the query results to a list of dictionaries
    tobs_data = []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict["Date"] = date
        tobs_dict["Temperature"] = tobs
        tobs_data.append(tobs_dict)
    return jsonify(tobs_data)

@app.route("/api/v1.0/<start>")
def stats_start(start):
    # calculate the summary statistics
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobos)).filter(Measurement.date >= start).all()
    # Convert the query results to a list of dictionaries
    start_stats = []
    for min_start, avg_start, max_start in results:
        start_dict = {}
        start_dict["min_start"] = min_start
        start_dict["avg_start"] = avg_start
        start_dict["max_start"] = max_start
        start_stats.append(start_dict)
    return jsonify(start_stats)

@app.route("/api/v1.0/<start>/<end>")
def stats_year(start, end):
    # calculate the summary statistics of the year
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobos)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    # Convert the query results to a list of dictionaries
    year_stats = []
    for min_year, avg_year, max_year in results:
        year_dict = {}
        year_dict["min_start"] = min_year
        year_dict["avg_start"] = avg_year
        year_dict["max_start"] = max_year
        year_stats.append(year_dict)
    return jsonify(year_stats)

if __name__ == '__main__':
    app.run(debug=True)