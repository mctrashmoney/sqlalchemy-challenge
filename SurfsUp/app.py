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
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect an existing database into a new model
Base = automap_base()
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

@app.route('/')
def homepage():
    """List all available API routes"""
    return (
        f"Available routes:<br/>"
        f"<b>/api/v1.0/precipitation</b> - Last 12 months of precipitation data<br/>"
        f"<b>/api/v1.0/stations</b> - List of weather stations<br/>"
        f"<b>/api/v1.0/tobs</b> - Temperature observations for the most active station (last 12 months)<br/>"
        f"<b>/api/v1.0/&lt;start&gt;</b> - Min, Avg, Max temperature from start date onwards (YYYY-MM-DD)<br/>"
        f"<b>/api/v1.0/&lt;start&gt;/&lt;end&gt;</b> - Min, Avg, Max temperature for a given date range (YYYY-MM-DD/YYYY-MM-DD)<br/>"
    )

@app.route('/api/v1.0/precipitation')
def precipitation():
    """Retrieve last 12 months of precipitation data"""
    session = Session(engine)

    recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    recent_date = dt.datetime.strptime(recent_date, "%Y-%m-%d").date()
    twelve_months_ago = recent_date - relativedelta(months=12)

    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= twelve_months_ago).order_by(Measurement.date).all()
    session.close()

    return jsonify({date: prcp for date, prcp in results})

@app.route('/api/v1.0/stations')
def stations():
    """Return list of stations"""
    session = Session(engine)
    results = session.query(Station.station).all()
    session.close()

    return jsonify([station[0] for station in results])

@app.route('/api/v1.0/tobs')
def tobs():
    """Retrieve temperature observations of the most active station for the last 12 months"""
    session = Session(engine)

    active_station = session.query(Measurement.station)\
        .group_by(Measurement.station)\
        .order_by(func.count(Measurement.station).desc()).first()[0]

    recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    recent_date = dt.datetime.strptime(recent_date, "%Y-%m-%d").date()
    twelve_months_ago = recent_date - relativedelta(months=12)

    results = session.query(Measurement.date, Measurement.tobs)\
        .filter(Measurement.station == active_station, Measurement.date >= twelve_months_ago)\
        .order_by(Measurement.date).all()
    
    session.close()

    return jsonify([{"Date": date, "Temperature": temp} for date, temp in results])

@app.route('/api/v1.0/<start>')
def start_date(start):
    """Return TMIN, TAVG, and TMAX for all dates >= start date"""
    session = Session(engine)

    start = dt.datetime.strptime(start, "%Y-%m-%d").date()

    results = session.query(
        func.min(Measurement.tobs),
        func.avg(Measurement.tobs),
        func.max(Measurement.tobs)
    ).filter(Measurement.date >= start).all()

    session.close()

    return jsonify({
        "Min Temp": results[0][0],
        "Avg Temp": round(results[0][1], 2),
        "Max Temp": results[0][2]
    })

@app.route('/api/v1.0/<start>/<end>')
def start_end_date(start, end):
    """Return TMIN, TAVG, and TMAX for dates between start and end (inclusive)"""
    session = Session(engine)

    start = dt.datetime.strptime(start, "%Y-%m-%d").date()
    end = dt.datetime.strptime(end, "%Y-%m-%d").date()

    results = session.query(
        func.min(Measurement.tobs),
        func.avg(Measurement.tobs),
        func.max(Measurement.tobs)
    ).filter(Measurement.date >= start, Measurement.date <= end).all()

    session.close()

    return jsonify({
        "Min Temp": results[0][0],
        "Avg Temp": round(results[0][1], 2),
        "Max Temp": results[0][2]
    })

if __name__ == '__main__':
    app.run(debug=True)
