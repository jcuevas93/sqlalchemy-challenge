# Import the dependencies.
from flask import Flask, jsonify
from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
from datetime import datetime as dt

#################################################
# Database Setup
#################################################
app = Flask(__name__)
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# Reflect an existing database into a new model
Base = automap_base()
# Reflect the tables
Base.prepare(engine, reflect=True)


# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB


#################################################
# Flask Setup
#################################################



#################################################
# Flask Routes
#################################################
@app.route("/")
def home():
    """List all available API routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    """Return a list of precipitation data including the date and prcp"""
    # Query all the precipitation data
    results = session.query(Measurement.date, Measurement.prcp).all()
    session.close()

    # Create a dictionary from the row data and append to a list of all_precipitations
    all_precipitations = {date: prcp for date, prcp in results}
    return jsonify(all_precipitations)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    """Return a JSON list of stations from the dataset."""
    results = session.query(Station.station).all()
    session.close()

    all_stations = [station[0] for station in results]
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    """Return a JSON list of temperature observations (TOBS) for the previous year."""
    # Query the dates and temperature observations of the most active station for the last year of data
    # This is an example, adjust the query according to your actual data and requirements
    most_active_station = 'USC00519281'
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == most_active_station).all()
    session.close()

    tobs_list = [{date: tobs} for date, tobs in results]
    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
def temp_start(start):
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    session.close()

    temps = list(map(lambda x: {"TMIN": x[0], "TAVG": x[1], "TMAX": x[2]}, results))
    return jsonify(temps)

@app.route("/api/v1.0/<start>/<end>")
def temp_start_end(start, end):
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    session.close()

    temps = list(map(lambda x: {"TMIN": x[0], "TAVG": x[1], "TMAX": x[2]}, results))
    return jsonify(temps)

# Define other routes as needed

if __name__ == '__main__':
    app.run(debug=True)