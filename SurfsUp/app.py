# Import the dependencies.
import numpy as np
import sqlalchemy
from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base

from flask import Flask, jsonify

from dateutil.relativedelta import relativedelta
import datetime as dt

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///SurfsUp/Resources/hawaii.sqlite")

# Reflect an existing database into a new model
Base = automap_base()
# Reflect the tables
Base.prepare(autoload_with=engine)

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
# Default page to list all available API routes
@app.route('/')
def homepage():
    """List of all available API routes"""
    return (
        f"Available routes:<br/>"
        f"<b>/api/v1.0/precipitation<br/></b>"
        f"<b>/api/v1.0/stations<br/></b>"
        f"<b>/api/v1.0/tobs<br/></b>"
        f"<b>/api/v1.0/start_date</b><br/><i>(Format: YYYY-MM-DD), i.e. 2017-08-23</i><br/>"
        f"<b>/api/v1.0/start_date/end_date</b><br/><i>(Format: YYYY-MM-DD), i.e. 2017-08-23</i><br/>"
    )

# Precipitation route for the last 12 months in the dataset in the API
@app.route('/api/v1.0/precipitation')
def prcp():
    recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    if isinstance(recent_date, str):
        recent_date = dt.datetime.strptime(recent_date, "%Y-%m-%d").date()
    twelve_months_ago = recent_date - relativedelta(months=12)
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= twelve_months_ago).order_by(Measurement.date.desc()).all()
    session.close()

    prcp_list = [{date: prcp} for date, prcp in results]
    return jsonify(prcp_list)

# Stations route for the dataset in the API 
@app.route('/api/v1.0/stations')
def stations():
    results = session.query(Station.station, Station.name).all()
    session.close()
    station_list = [{"Station": station, "Station_Name": name} for station, name in results]
    return jsonify(station_list)

# Temperature Observations route for the last 12 months in the dataset in the API
@app.route('/api/v1.0/tobs')
def tobs():
    recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    if isinstance(recent_date, str):
        recent_date = dt.datetime.strptime(recent_date, "%Y-%m-%d").date()
    twelve_months_ago = recent_date - relativedelta(months=12)
    active_station, _ = session.query(Measurement.station, func.count(Measurement.station)).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).first()
    session.close()
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == active_station).filter(Measurement.date >= twelve_months_ago).order_by(Measurement.date.desc()).all()
    tobs_list = [{"Date": tobs[0], "Temperature": tobs[1]} for tobs in results]
    return jsonify(tobs_list)

# Start date only route for the dataset in the API
@app.route('/api/v1.0/<start_date>')
def start_date_only(start_date):
    start_date = dt.datetime.strptime(start_date, "%Y-%m-%d")
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start_date).all()
    session.close()
    start_date_only_results = [{"Min Temp": results[0][0], "Max Temp": results[0][1], "Avg Temp": results[0][2]}]
    return jsonify(start_date_only_results)

# Start and end date route for the dataset in the API
@app.route('/api/v1.0/<start_date>/<end_date>')
def start_end_date(start_date, end_date):
    start_date = dt.datetime.strptime(start_date, "%Y-%m-%d")
    end_date = dt.datetime.strptime(end_date, "%Y-%m-%d")
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    session.close()
    start_end_date_results = [{"Min Temp": results[0][0], "Max Temp": results[0][1], "Avg Temp": results[0][2]}]
    return jsonify(start_end_date_results)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
