from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import json
import pandas as pd

app = Flask(__name__)


# CREATE DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///hyperloop-trips.db"
# Optional: But it will silence the deprecation warning in the console.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# db.create_all()

with open("TestData.json") as data_file:
    data = json.load(data_file)


df = pd.DataFrame(data)
engine = create_engine("sqlite:///hyperloop-trips.db")
df.to_sql("Trip", con=engine)


@app.route('/api/<metricName>/')
def show(metricName):
    result = df.loc[:,metricName].to_json(orient='table')
    parsed = json.loads(result)
    return json.dumps(parsed, indent=4)


#print(df)
if __name__ == "__main__":
    app.run()
