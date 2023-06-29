# Import the dependencies.

from flask import Flask, jsonify
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model

Base = automap_base()
# reflect the tables
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


# 3. Define what to do when a user hits the index route
@app.route("/")
def home():
    return(
        f"Miranda<br/>"
        f"routes<br/>"
        f"/api/v1.0/precipitation<br/>"
    )

# 4. Define what to do when a user hits the /about route


@app.route("/api/v1.0/precipitation")
def about():
    last_date = session.query(func.max(Measurement.date)).first()
    one_year_ago = dt.datetime.strptime(
        last_date[0], '%Y-%m-%d') - dt.timedelta(days=365)

    # Perform a query to retrieve the data and precipitation scores
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= one_year_ago).all()
    precip = {date: prcp for date, prcp in results}
    print(precip)
    return jsonify(precip)


if __name__ == "__main__":
    app.run(debug=True)
