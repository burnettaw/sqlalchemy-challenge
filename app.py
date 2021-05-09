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

############### MOST ACTIVE OBSERVATION API ###############
@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    prior_year = dt.date(2017,8,23) - dt.timedelta(days=365)

    """Return a list of all """
    # Query all stations
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == "USC00519281").filter(Measurement.date >= prior_year).all() 
    		
    session.close

    all_data = list(np.ravel(results))
    return jsonify(all_data)

############### OBSERVATION START DATE API ###############
@app.route("/api/v1.0/<start>")
def start_date(start):

    session = Session(engine)
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date == start).all() 
    session.close

    # for result in results:
    #     if result[0] == dt.date(start):
    #         return jsonify(all_data)
    
    all_data = list(np.ravel(results))
    return jsonify(all_data)
    return jsonify({"error": f"Date with  {start} not found."}), 404

############### OBSERVATION START DATE AND END DATE API ###############
@app.route("/api/v1.0/<start>/<end>")
def start_to_end_date(start,end):

    session = Session(engine)
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= start and Measurement.date <= end).all() 
    session.close

    # for result in results:
    #     if result[0] == dt.date(start):
    #         return jsonify(all_data)
    
    all_data = list(np.ravel(results))
    return jsonify(all_data)
    return jsonify({"error": f"Date with  {start} not found."}), 404

if __name__ == '__main__':
    app.run(debug=True)
 