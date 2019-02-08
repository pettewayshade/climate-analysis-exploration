import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy.pool import QueuePool

from flask import Flask, jsonify

#Setup db
engine = create_engine('sqlite:///Resources/hawaii.sqlite')

Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

#Setup Flask
app = Flask(__name__)

#Setup routes
@app.route('/')
def home():
    return (
        f'<b>Available Routes:</b><br/>'
        f'<ul>'
        f'<li>/api/v1.0/precipitation</li>'
        f'<li>/api/v1.0/stations</li>'
        f'<li>/api/v1.0/tobs</li>'
        f'<li>/api/v1.0/start<br/>'
        f'-- Note: Start date must be between 2010-01-01 and 2017-08-23<br/>'
        f'<li>/api/v1.0/start/end</li>'
        f'-- Note: Start date cannot be sooner that 2010-01-01 and end date cannot be later than 2017-08-23'
        f'</ul>'
    )

@app.route('/api/v1.0/precipitation')
def percipitation():
    gdate = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    prcp = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= gdate).\
    order_by(Measurement.date).all()
    
    prcp = dict(prcp)
    
    str = 'Perceipation results for previous year:'
    return jsonify(prcp)


@app.route('/api/v1.0/stations')
def stations():
    results = session.query(Station.station).all()
    session.close()
    
    allStations = list(np.ravel(results))
    
    msg = f'List of all stations from the dataset:'
    
    return jsonify(f'{msg} {allStations}')


@app.route('/api/v1.0/tobs')
def tobs():
    gdate = dt.datetime(2017, 8, 18) - dt.timedelta(days=365)
    tobs = session.query(Measurement.tobs).\
        filter(Measurement.date >= gdate).\
        order_by(Measurement.tobs.desc()).\
        group_by(Measurement.tobs).all()
    session.close()
    
    tobs = list(np.ravel(tobs))
    
    msg = f'List of Temperature Obeservations (tobs) for the previous year:'
    
    return jsonify(f'{msg} {tobs}')


@app.route('/api/v1.0/<start>')
def startdate(start):
    if start < '2010-01-01' or start > '2017-08-23': 
        return jsonify({"error": f"Start date: {start} is not within range."}), 404
    
    results = session.query(
             func.min(Measurement.tobs),
             func.max(Measurement.tobs),
             func.avg(Measurement.tobs)).\
             filter(Measurement.date >= start).all()
    session.close()
    
    results = list(np.ravel(results))
    
    item_dict = {
        'Min tob': results[0],
        'Max tob': results[1],
        'Avg tob': results[2]
        }
        
    msg = f'TOB results for dates greater than or equal to {start}:'
    
    return jsonify(f'{msg} {item_dict}')


@app.route('/api/v1.0/<start>/<end>')
def startenddate(start,end):
    if start < '2010-01-01' or end  > '2017-08-23' or start >= end or end <= start: 
        return jsonify({"error": f"Start date: {start} or end date: {end} is not within range."}), 404
    
    results = session.query(
             func.min(Measurement.tobs),
             func.max(Measurement.tobs),
             func.avg(Measurement.tobs)).\
             filter(Measurement.date >= start, Measurement.date <= end).all()
    session.close()
    
    results = list(np.ravel(results))
    
    item_dict = {
        'Min tob': results[0],
        'Max tob': results[1],
        'Avg tob': results[2]
        }
    
    msg = f'TOB results for date range {start} - {end}:'
    
    return jsonify(f'{msg} {item_dict}')


if __name__ == '__main__':
    app.run(debug=True)