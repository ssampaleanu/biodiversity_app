import datetime as dt
import numpy as np
import pandas as pd

from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Database Setup
#################################################
from flask_sqlalchemy import SQLAlchemy
# The database URI
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///belly_button_biodiversity.sqlite"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


engine = create_engine("sqlite:///belly_button_biodiversity.sqlite")
inspector = inspect(engine)

db = SQLAlchemy(app)

@app.route("/")
def home():
    """Render Home Page."""
    return render_template("index.html")

@app.route("/names")
def names():
    columns = inspector.get_columns("samples")

    samples = []

    for column in columns:
        samples.append(column['name'])

    return jsonify(samples[1:])

@app.route("/otu")
def otu():
    otu_pairs = engine.execute('SELECT lowest_taxonomic_unit_found FROM otu').fetchall()

    otu_desc = []

    for pair in otu_pairs:
        otu_desc.append(pair[0])

    return jsonify(otu_desc)

@app.route("/metadata/<sample>")
def sample_meta(sample):
    search_id = sample[3:]

    result = engine.execute(f'SELECT age, bbtype, ethnicity, gender, location, sampleid FROM samples_metadata WHERE sampleid = "{search_id}"').fetchall()
    result = result[0]

    sample_dict = {
        'AGE':result[0],
        'BB TYPE':result[1],
        'ETHNICITY':result[2],
        'GENDER':result[3],
        'LOCATION':result[4],
        'SAMPLE ID':result[5]
    }

    return jsonify(sample_dict)

@app.route("/wfreq/<sample>")
def wfreq(sample):
    search_id = sample[3:]

    result = engine.execute(f'SELECT wfreq FROM samples_metadata WHERE sampleid = "{search_id}"').fetchall()
    result = result [0]

    return str(result[0])

@app.route('/samples/<sample>')
def life_forms(sample):
    otu_ids = []
    sample_values = []
    results = engine.execute(f'SELECT otu_id, {sample} FROM samples WHERE {sample} > 0 ORDER BY {sample} DESC').fetchall()
    for result in results:
        otu_ids.append(result[0])
        sample_values.append(result[1])

    return_dict = {'otu_ids':otu_ids, 'sample_values':sample_values}

    return jsonify(return_dict)


if __name__ == "__main__":
    app.run(debug=True)