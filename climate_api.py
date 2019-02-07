import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy.pool import QueuePool

from flask import Flask, jsonify

#Setup db
engine = create_engine('sqlite:///Resources/hawaii.sqlite')

Base = automap_base()
Base.prepar(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

#Setup Flask
app = Flask(__name__)

#Setup routes
@app.route('/')
def home():
    return (
        f'Available Routes:<br/>'
        f'/api/v1.0/precipitation<br/>'
        f'/api/v1.0/stations<br/>'
        f'/api/v1.0/tobs</br>'
        f'/api/v1.0/<start><br/>'
        f'/api/v1.0/<start>/<end>'    
    )

@app.route('/api/v1.0/precipitation')
def percipitation():
    
@app.route('/api/v1.0/stations')
def stations():
    
@app.route('/api/v1.0/tobs')
def tobs():
    
@app.route('/api/v1.0/<start>')
def startdate():
    
@app.route('/api/v1.0/<start>/<end>')
def startenddate():

if __name__ == '__main__':
    app.run(debug=True)