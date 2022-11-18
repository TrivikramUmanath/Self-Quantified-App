from asyncio.log import logger
from email.mime import message


from flask import Flask, redirect, request
from flask import render_template
from flask import current_app as app
from application.models import User,Tracker,Logger
from .database import db
import datetime
import matplotlib.pyplot as plt
from pytz import timezone
import numpy as np
import pandas as pd

dur=["0:00","0:30","1:00","1:30","2:00","2:30","3:00","3:30","4:00","4:30","5:00","5:30","6:00","6:30","7:00","7:30","8:00","8:30","9:00","9:30","10:30","11"]


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "GET":   
        message = " "
    elif request.method == "POST":
          userName=request.form.get("uname")
          passw=request.form.get("psw")
          users=None
          users=User.query.filter_by(Name = userName,password=passw).first()
          if users:
              id=users.user_id
              temp="/Dashboard/"+str(id)
              return redirect(temp)
          else:
              message = "Incorrect UserName or Password"
    return render_template("Login.html",display_message=message)

@app.route("/Forgot_Password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "GET":   
        message = " "
    elif request.method == "POST":
          userName=request.form.get("uname")
          key=request.form.get("key")
          users=None
          users=User.query.filter_by(Name = userName,SecretKey=key).first()
          if users:
              message="Your password is "+str(users.password)
          else:
              message = "Incorrect UserName or COlour"
    return render_template("Forgot_Password.html",display_message=message)

@app.route("/Create",methods=["GET","POST"])
def create():
    if request.method == "GET":
        flag=1
    elif request.method == "POST":
        userName = request.form.get('userid')
        name = request.form.get('name')
        Password = request.form.get('password')
        Email = request.form.get('email')
        ke=request.form.get('key')
        if userName == '':
            return redirect('/')
        else:
            new_user=User(user_id=userName,password=Password,email=Email,Name=name,SecretKey=ke)
            db.session.add(new_user)
            db.session.commit()
        return redirect('/')
    return render_template('Create.html')

@app.route("/Dashboard/<string:id>",methods=["GET","POST"])
def log(id):
    if request.method == "GET" or request.method=="POST":
        intId=int(id)
        track=db.session.query(Tracker).filter(Tracker.user_id==intId)
        name=db.session.query(User).filter(User.user_id==intId).first()
        return render_template("Dashboards.html",trackers=track,id=intId,n=name.Name)
    return render_template('Dashboards.html',id=intId)

@app.route("/Dashboard/<string:ida>/<string:tracker_id>",methods=["GET","POST"])
def view_log(ida,tracker_id):
    if request.method == "GET":     
        a=int(ida)
        b=int(tracker_id)
        log=db.session.query(Logger).filter(Logger.Tracker_Id==b)
    return render_template('view_log.html',lg=log,id1=a,id2=b)

@app.route("/Dashboard/<string:id1>/<string:id2>/AddLogs",methods=["GET","POST"])
def logger(id1,id2):
    if request.method == "POST":
        q=int(id1)
        b=int(id2)     
        timeDuration=request.form.get('timeDuration')
        value=request.form.get('value')
        note=request.form.get('note')
        timeStamp=datetime.datetime.now(timezone("Asia/Kolkata")).strftime('%d-%m-%Y %H:%M:%S.%f')
        new_Log=Logger(Time_Stamp=timeStamp,Value=value,Note=note,Tracker_Id=int(id2))
        db.session.add(new_Log)
        db.session.commit()
        return redirect('/Dashboard/'+str(q)+'/'+str(b))
    else:
        tr= db.session.query(Tracker).filter(Tracker.Tracker_Id==int(id2)).first()
        setti=[]
        if tr.Tracker_Type == "Categorical":
            setti=tr.Seetings.split(',')
            print(setti)

    return render_template('add_log.html',id=int(id1),values=setti,dur=dur)

@app.route("/Dashboard/<string:id1>/<string:id2>/Visualize",methods=["GET","POST"])
def plt_data(id1,id2):
    print(id1)
    print(id2)
    trace=db.session.query(Tracker).filter(Tracker.Tracker_Id==int(id2)).first()
    Activity=trace.Name
    print(Activity)
    lg=db.session.query(Logger).filter(Logger.Tracker_Id==int(id2)).first()
    log=db.session.query(Logger).filter(Logger.Tracker_Id==int(id2)).all()
    x_data=[]
    y_data=[]
    df=pd.DataFrame(columns=[['Input','Output']])
    if log:
        if trace.Tracker_Type == "Numerical":
            data=[]
            for l in log:
                x_data.append(datetime.datetime.strptime(l.Time_Stamp,'%d-%m-%Y %H:%M:%S.%f'))
                y_data.append(float(l.Value))
            df = pd.DataFrame({
                 'Input' : x_data,'Output' : y_data})

            df=df.sort_values(by="Input",kind = "mergesort")
            print(df)
            fig = plt.figure(figsize = (10, 5))
            plt.figure()
            plt.plot(df['Input'],df['Output'])
            plt.title(str(Activity)+' Trend')
            plt.gcf().autofmt_xdate()
            plt.xlabel('Time Stamp')
            plt.ylabel('Value')
            plt.savefig('static/output.png')
        else:
            freq=dict()
            for l in log:
                y_data.append(l.Value)
            x_data=trace.Seetings.split(',')
            freq={}
            for i in x_data:
                freq[i]=0
            for j in y_data:
                for i in freq:
                    if i ==j:
                        freq[i]=freq[i]+1
            courses = list(freq.keys())
            values = list(freq.values())
            print(freq)
            print(courses)
            print(values)
            fig = plt.figure(figsize = (10, 5))
    
            # creating the bar plot
            plt.bar(courses, values, color ='blue',
            width = 0.4)
            plt.title(str(Activity)+' Trend')
            plt.xlabel('Values')
            plt.ylabel('Frequency')
            plt.savefig('static/output.png')
        return render_template('plot_data.html',lg=log,A=Activity,id=int(id1))
    else:
        r=int(id1)
        message="No Data Logged for the Tracker"
        intId=int(id1)
        print(message)
        trace=db.session.query(Tracker).filter(Tracker.user_id==int(id1)).all()
        name=db.session.query(User).filter(User.user_id==intId).first()
        return render_template("Dashboards.html",trackers=trace,id=intId,n=name.Name,m=message)
        

@app.route("/Dashboard/<string:id1>/<string:id2>/Edit",methods=["GET","POST"])
def edit_tracker(id1,id2):
    r=int(id1)
    if request.method == "POST":
        Name=request.form.get('name')
        desciption=request.form.get('description')
        trace=db.session.query(Tracker).filter(Tracker.Tracker_Id==int(id2)).update({Tracker.Name:Name,Tracker.Description:desciption}, synchronize_session = False)
        db.session.commit()
        return redirect('/Dashboard/'+str(r))
    return render_template('edit_tracker.html',id=r)

@app.route("/Dashboard/<string:id1>/<string:id2>/Delete",methods=["GET","POST"])
def delete_tracker(id1,id2):
    id=int(id1)
    id3=int(id2)
    trace=Tracker.query.filter_by(Tracker_Id = id3).first()
    if trace:
        log=Logger.query.filter_by(Tracker_Id = int(id3)).first()
        if log:
            Logger.query.filter_by(Tracker_Id = int(id3)).delete()
        Tracker.query.filter_by(Tracker_Id = id3).delete()
    db.session.commit()
    r=int(id1)
    return redirect('/Dashboard/'+str(r))


@app.route("/Dashboard/<string:id1>/<string:id2>/<string:id3>/Edit",methods=["GET","POST"])
def edit_logs(id1,id2,id3):
    r=int(id1)
    b=int(id2)
    if request.method == "POST":
        time=request.form.get('Time_Stamp')
        value=request.form.get('value')
        note=request.form.get('note')
        lg=db.session.query(Logger).filter(Logger.Logger_Id==int(id3)).update({Logger.Note:note,Logger.Value:value,Logger.Time_Stamp:time}, synchronize_session = False)
        db.session.commit()
        return redirect('/Dashboard/'+str(r)+'/'+str(b))
    return render_template('edit_log.html',id1=r,id2=b)

@app.route("/Dashboard/<string:id1>/<string:id2>/<string:id3>/Delete",methods=["GET","POST"])
def delete_logs(id1,id2,id3):
    Logger.query.filter_by(Logger_Id = int(id3)).delete()
    db.session.commit()
    r=int(id1)
    b=int(id2)
    return redirect('/Dashboard/'+str(r)+'/'+str(b))

@app.route("/Dashboard/<string:id>/addTracker",methods=["GET","POST"])
def tracker(id):
    r=int(id)
    if request.method == "POST":
        print('inside tracker')
        name=request.form.get('name')
        description=request.form.get('description')
        seetings=request.form.get('seetings')
        type=request.form.get('tracker_type')
        new_tracker=Tracker(Name=name,Seetings=seetings,Tracker_Type=type,Description=description,user_id = r)
        db.session.add(new_tracker)
        db.session.commit()
        return redirect('/Dashboard/'+str(r))
    return render_template('add_tracker.html',id=r)
        


    