import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#connect to database
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True) 

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station



app = Flask(__name__) #what is the purpose of this line?

############### HOME WELCOME ###############
@app.route('/')
def home():
    """List all available api routes."""
    #print(prec_dict)
    return (
        f"Welcome to the climate API:<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/measurement/ <br/>"
        f"/api/v1.0/start <br/>"
        f"/api/v1.0/start/end <br/>"
        f"/api/v1.0/precipitation/ <br/>"
        f"/api/v1.0/station"
        
    )
############### PRECIPITATION API ###############
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    prior_year = dt.date(2017,8,23) - dt.timedelta(days=365)

    """Return a list of all """
    # Query all passengers
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prior_year).all()
    
    session.close

    precip = {date: prcp for date, prcp in results}
    return jsonify(precip)

############### MEASUREMENT API ###############
@app.route("/api/v1.0/measurement")
def measurement():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    prior_year = dt.date(2017,8,23) - dt.timedelta(days=365)

    """Return a list of all """
    # Query all passengers
    results = session.query(Measurement.id, Measurement.station, Measurement.date, Measurement.prcp, Measurement.tobs).\
        filter(Measurement.date >= prior_year).all()
   
    session.close

    all_data = list(np.ravel(results))
    return jsonify(all_data)

############### STATION API ###############
@app.route("/api/v1.0/station")
def station():
    # Create our session (link) from Python to the DB
    session = Session(engine)
   
    """Return a list of all """
    # Query all stations
    results = session.query(Station.id, Station.name, Station.latitude, Station.longitude, Station.elevation).all()
    		
    session.close

    all_data = list(np.ravel(results))
    return jsonify(all_data)

if __name__ == '__main__':
    app.run(debug=True)
 