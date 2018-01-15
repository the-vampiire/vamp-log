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

  if __name__ == "__main__":
    app.run(port = 3000)


  