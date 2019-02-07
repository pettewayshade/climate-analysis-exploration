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
        f"Available Routes:<br/>"
        f'/api/v1.0/precipitation<br/>'
        f'/api/v1.0/stations<br/>'
        f'/api/v1.0/tobs</br>'
        f'/api/v1.0/start<br/>'
        f'/api/v1.0/start/end'    
    )

@app.route('/api/v1.0/precipitation')
def percipitation():
    gdate = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    prcp = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= gdate).\
    order_by(Measurement.date).all()
    
    prcp = dict(prcp)
    
    return jsonify(prcp)

@app.route('/api/v1.0/stations')
def stations():
    results = session.query(Station.station).all()
    session.close()
    
    allStations = list(np.ravel(results))
    
    return jsonify(allStations)

@app.route('/api/v1.0/tobs')
def tobs():
    gdate = dt.datetime(2017, 8, 18) - dt.timedelta(days=365)
    tobs = session.query(Measurement.tobs).\
        filter(Measurement.date >= gdate).\
        order_by(Measurement.tobs.desc()).all()
    session.close()
    
    tobs = list(np.ravel(tobs))
    
    msg = f'List of Temperature Obeservations (tobs) for the previous year'
    return jsonify(tobs)

@app.route('/api/v1.0/<start>')
def startdate():
    return f'No info'

@app.route('/api/v1.0/<start>/<end>')
def startenddate():
    return f'No info'

if __name__ == '__main__':
    app.run(debug=True)