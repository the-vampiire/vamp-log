from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime as dt
from private import DB_URI

# Server Configuration
app = Flask(__name__)
app.config['DEBUG'] = True

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Models
db = SQLAlchemy(app)

class DailyLog(db.Model):
  __tablename__ = "daily_logs"

  id = db.Column(db.Integer, primary_key = True, nullable = False)
  accomplishment = db.Column(db.String(140), nullable = False)
  challenge = db.Column(db.String(140), nullable = False)
  recognition = db.Column(db.Text, nullable = True)
  notes = db.Column(db.Text, nullable = True)
  created_at = db.Column(db.String(25), nullable = False, default = dt.now().strftime('%B %d, %Y'))

  """
  one-to-many relationship with Paths
  
  flask sqlalchemy: http://flask-sqlalchemy.pocoo.org/2.3/models/#one-to-many-relationships
  mysql: https://code.tutsplus.com/articles/sql-for-beginners-part-3-database-relationships--net-8561
  stack overflow: https://stackoverflow.com/questions/25375179/one-to-many-flask-sqlalchemy?rq=1
  """
  paths = db.relationship("Path", backref = "DailyLog", lazy = "joined")

class Path(db.Model):
  __tablename__ = 'paths'

  id = db.Column(db.Integer, primary_key = True, nullable = False)
  daily_log_id = db.Column(db.Integer, db.ForeignKey('daily_logs.id'), nullable = False)
  reference_url = db.Column(db.Text, nullable = False)

# Database helpers
def create_daily_log(paths, **values):
  new_daily_log = DailyLog(**values) # create log by "spreading" the keyword argument values
  paths = [Path(reference_url = path, daily_log_id = new_daily_log.id) for path in paths]

  new_daily_log.paths.extend(paths) # associate the new_daily_log to the paths
  db.session.add(new_daily_log) # stage the new_daily_log
  db.session.add_all(paths) # stage the paths
  db.session.commit() # save to the database
  return { "daily_log": new_daily_log, "paths": paths }


# Route helpers
def make_progress(form_data):
  accomplishment = form_data['accomplishment']
  challenge = form_data['challenge']
  recognition = form_data['recognition']
  notes = form_data['notes']

  # https://stackoverflow.com/questions/24808660/sending-a-form-array-to-flask
  paths = form_data.getlist('paths') 

  return create_daily_log(paths, accomplishment = accomplishment, challenge = challenge, recognition = recognition, notes = notes)


# Routes
@app.route("/", methods = ["GET", "POST"])
def index():
  # handle POST update - http://flask.pocoo.org/docs/0.12/quickstart/#variable-rules
  if request.method == "POST":
    db_response = make_progress(request.form)
    return render_template("index.html", daily_log = db_response["daily_log"], paths = db_response["paths"])
  elif request.method == "GET":
    return render_template("index.html")

if __name__ == "__main__":
  app.run(port = 3000)


  