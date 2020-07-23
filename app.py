# import dependencies
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

######################################################
# Database Setup
######################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect an existing database 
Base = automap_base()
# Reflect tables
Base.prepare(engine, reflect=True)

# Save reference to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station

######################################################
# Flask Setup
######################################################
app = Flask(__name__)

######################################################
# Flask Routes
######################################################

# Define what to do when user hits the index route
@app.route("/")
def home():
    """List all available api routes."""
    return(
        f"Welcome to Hawaii Climate Page<br/> "
        f"Available Routes:<br/>"
        f"<br/>"  
        f"/api/v1.0/precipitation<br/>"
        f"<br/>"
        f"/api/v1.0/stations<br/>"
        f"<br/>"
        f"/api/v1.0/tobs<br/>"
        f"<br/>"
        f"/api/v1.0/<start><br/>"
        "<br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

#####################################################
# Precipitation
#####################################################

# create precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the prcp data as json with date as key"""
    #creation our session link from Python to the DB
    session = Session(engine)

    # Query all date and precipitation values
    prcp_data = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all precipitation
    precipitation = []
    for date, prcp in prcp_data:
        prcp_dict = {}
        prcp_dict[date] = prcp 
        precipitation.append(prcp_dict)

    return jsonify(precipitation)

######################################################
# Stations
######################################################

# create stations route    
@app.route("/api/v1.0/stations")
def stations():
    """Return the prcp data as json with date as key"""
    #creation our session link from Python to the DB
    session = Session(engine)

    # Query all stations
    station_names =session.query(Station.name).all()

    session.close()

    # Convert list of tuples into normal list
    station_list = list(np.ravel(station_names))


    return jsonify(station_list)

######################################################
# Temp Obs
######################################################

# create temperature observation route
@app.route("/api/v1.0/tobs")
def tobs():
    #creation our session link from Python to the DB
    session = Session(engine)

    #set the latest date
    start_date = datetime.date(2016, 8, 23)

    # Query all date and tobs values
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= start_date).\
        filter(Measurement.station == 'USC00519281').all()

    session.close()

######################################################
# Could not figure out the last two. Ran out of time :(
######################################################

######################################################
# Run the app
######################################################
if __name__ == "__main__":
    app.run(debug=True)

