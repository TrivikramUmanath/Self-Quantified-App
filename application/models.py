from .database import db

class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    Name = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)
    SecretKey=db.Column(db.String)

class Tracker(db.Model):
    __tablename__ = "Tracker"
    user_id = db.Column(db.Integer,db.ForeignKey("user.user_id",ondelete="CASCADE"), nullable=False)
    Tracker_Id  = db.Column(db.Integer, primary_key=True, nullable=False,autoincrement=True)
    Tracker_Type = db.Column(db.String)
    Name = db.Column(db.String)
    Description = db.Column(db.String)
    Seetings = db.Column(db.String)
 

class Logger(db.Model):
    __tablename__ = 'Logger'
    Tracker_Id = db.Column(db.Integer,db.ForeignKey("Tracker.Tracker_Id",ondelete="CASCADE"), nullable=False)
    Logger_Id = db.Column(db.Integer, primary_key=True,nullable=False)
    Value = db.Column(db.String,nullable=False)
    Note = db.Column(db.String,nullable=False)
    Time_Stamp = db.Column(db.String)


