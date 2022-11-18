
from flask_restful import Resource,fields,marshal_with,reqparse
from application.database import db
from application.models import Logger,User,Tracker
from application.validation import NotFoundError,BusinessValidationError

user_output_fields={
    'user_id':fields.Integer,
    "Name":fields.String,
    "email":fields.String,
    "password":fields.String,
    "SecretKey":fields.String
}

tracker_output_fields={
    'user_id':fields.Integer,
    'Tracker_Id':fields.Integer,
    "Name":fields.String,
    "Description":fields.String,
    "Seetings":fields.String,
    "Tracker_Type":fields.String
}

logger_output_fields={
    'Logger_id':fields.Integer,
    'Tracker_Id':fields.Integer,
    "Value":fields.String,
    "Note":fields.String,
    "Time_Stamp":fields.String
}

create_user_parser=reqparse.RequestParser()
create_user_parser.add_argument('user_id')
create_user_parser.add_argument('Password')
create_user_parser.add_argument('Email')
create_user_parser.add_argument('SecretKey')
create_user_parser.add_argument('Name')

update_user_parser=reqparse.RequestParser()
update_user_parser.add_argument('user_id')
update_user_parser.add_argument('Password')
update_user_parser.add_argument('Email')
update_user_parser.add_argument('SecretKey')
update_user_parser.add_argument('Name')

create_tracker_parser=reqparse.RequestParser()
create_tracker_parser.add_argument('tracker_id')
create_tracker_parser.add_argument('user_id')
create_tracker_parser.add_argument('Name')
create_tracker_parser.add_argument('Tracker_Type')
create_tracker_parser.add_argument('Seetings')
create_tracker_parser.add_argument('Description')

update_tracker_parser=reqparse.RequestParser()
update_tracker_parser.add_argument('tracker_id')
update_tracker_parser.add_argument('user_id')
update_tracker_parser.add_argument('Name')
update_tracker_parser.add_argument('Tracker_Type')
update_tracker_parser.add_argument('Seetings')
update_tracker_parser.add_argument('Description')

create_logger_parser=reqparse.RequestParser()
create_logger_parser.add_argument('Logger_Id')
create_logger_parser.add_argument('Tracker_Id')
create_logger_parser.add_argument('Note')
create_logger_parser.add_argument('Value')
create_logger_parser.add_argument('Time_Stamp')

update_logger_parser=reqparse.RequestParser()
update_logger_parser.add_argument('Logger_Id')
update_logger_parser.add_argument('Tracker_Id')
update_logger_parser.add_argument('Note')
update_logger_parser.add_argument('Value')
update_logger_parser.add_argument('Time_Stamp')

class UserAPI(Resource):
    @marshal_with(user_output_fields)
    def get(self,user_id,password):
        print('Hello')
        id=int(user_id)
        user=db.session.query(User).filter(User.user_id==id,User.password==password).first()
        print(user)
        if user:
            return user
        else:
            raise NotFoundError(status_code=404)

    @marshal_with(user_output_fields)
    def put(self,user_id,password):
        id=int(user_id)
        args=update_user_parser.parse_args()
        passw=args.get('Password',None)
        em=args.get("Email",None)
        key=args.get('SecretKey',None)
        nam=args.get('Name',None)
        user=db.session.query(User).filter(User.user_id==id,User.password==password).first()
        print(user)
        if user:
            user.Name=nam
            user.email=em
            user.SecretKey=key
            user.Password=passw
            db.session.commit()
            return user
        else:
            raise NotFoundError(status_code=404)

    def delete(self,user_id,password):
        id=int(user_id)
        user=db.session.query(User).filter(User.user_id==id,User.password==password).first()
        print(user)
        if user:
            db.session.delete(user)
            db.session.commit()
            return {},201
        else:
            raise NotFoundError(status_code=404)
    def post(self):
        args=create_user_parser.parse_args()
        user_id=args.get("user_id",None)
        password=args.get('Password',None)
        em=args.get("Email",None)
        key=args.get('SecretKey',None)
        nam=args.get('Name',None)
        if user_id is None or password is None:
            raise BusinessValidationError(status_code=400,error_code="BE1001",error_message="user_id or password is required")
        else:
            pass
        user=db.session.query(User).filter(User.user_id==int(user_id)).first()
        if user:
            raise BusinessValidationError(status_code=400,error_code="BE1002",error_message="duplicate user_id")
        new_user=User(user_id=int(user_id),password=password,Name=nam,SecretKey=key,email=em)
        db.session.add(new_user)
        db.session.commit()
        return {},201

class TrackerAPI(Resource):
    @marshal_with(tracker_output_fields)
    def get(self,user_id,password,Tracker_Id):
        id=int(user_id)
        id2=int(Tracker_Id)
        user=db.session.query(User).filter(User.user_id==id,User.password==password).first()
        if user:
            tracker=db.session.query(Tracker).filter(Tracker.user_id==id,Tracker.Tracker_Id==id2).first()
            if tracker:
                return tracker
            else:
                raise NotFoundError(status_code=404)
        else:
            raise NotFoundError(status_code=404)

    def put(self,user_id,password,Tracker_Id):
        id=int(user_id)
        id2=int(Tracker_Id)
        args=create_tracker_parser.parse_args()
        Name=args.get('Name',None)
        Descr=args.get("Description",None)
        Seet=args.get('Seetings',None)    
        Track_Type=args.get('Tracker_Type',None)

        user=db.session.query(User).filter(User.user_id==id,User.password==password).first()
        print(user)
        if user:
            tracker=db.session.query(Tracker).filter(Tracker.user_id==id,Tracker.Tracker_Id==id2).first()
            if tracker:
                tracker.Name=Name
                tracker.Description=Descr
                tracker.Seetings=Seet
                tracker.Tracker_Type=Track_Type
                db.session.commit()
                return {},201
            else:
                raise NotFoundError(status_code=404)         
        else:
            raise NotFoundError(status_code=404)

    def delete(self,user_id,password,Tracker_Id):
        id=int(user_id)
        id2=int(Tracker_Id)
        user=db.session.query(User).filter(User.user_id==id,User.password==password).first()
        print(user)
        if user:
            tracker=db.session.query(Tracker).filter(Tracker.user_id==id,Tracker.Tracker_Id==id2).first()
            if tracker:
                db.session.delete(tracker)
                db.session.commit()
                return {},201
            else:
                raise NotFoundError(status_code=404)

        else:
            raise NotFoundError(status_code=404)

    def post(self,user_id,password):
        id=int(user_id)
        print('tri')
        args=create_tracker_parser.parse_args()
        id2=args.get('Tracker_Id',None)
        Descr=args.get("Description",None)
        Seet=args.get('Seetings',None)    
        Nam=args.get('Name',None)
        Track_Type=args.get('Tracker_Type',None)
        user=db.session.query(User).filter(User.user_id==id,User.password==password).first()
        if user:
            new_tracker=Tracker(Tracker_Id=id2,Description=Descr,Seetings=Seet,Tracker_Type=Track_Type,Name=Nam,user_id=id)
            db.session.add(new_tracker)
            db.session.commit()
            return {},201
        if user_id is None or password is None:
            raise BusinessValidationError(status_code=400,error_code="BE1001",error_message="user_id or password is required")
        else:
            pass
        user=db.session.query(User).filter(User.user_id==int(user_id)).first()
        if user:
            raise BusinessValidationError(status_code=400,error_code="BE1002",error_message="duplicate user_id")


class LoggerAPI(Resource):
    @marshal_with(logger_output_fields)
    def get(self,user_id,password,Tracker_Id,Logger_Id):
        id=int(user_id)
        user=db.session.query(User).filter(User.user_id==id,User.password==password).first()
        if user:
            id2=int(Tracker_Id)
            tracker=db.session.query(Tracker).filter(Tracker.user_id==id,Tracker.Tracker_Id==id2).first()
            if tracker:
                id3=int(Logger_Id)
                logger=db.session.query(Logger).filter(Logger.Logger_Id==id3,Logger.Tracker_Id==id2).first()
                if logger:
                    return logger
                else:
                    raise NotFoundError(status_code=404)
            else:
                raise NotFoundError(status_code=404)        
        else:
            raise NotFoundError(status_code=404)

    def put(self,user_id,password,Tracker_Id,Logger_Id):
        id=int(user_id)
        id1=int(Tracker_Id)
        id2=int(Logger_Id)
        args=update_logger_parser.parse_args()
        timeSt=args.get('Time_Stamp',None)
        val=args.get("Value",None)
        note=args.get('Note',None)    
        user=db.session.query(User).filter(User.user_id==id,User.password==password).first()
        if user:
            tracker=db.session.query(Tracker).filter(Tracker.user_id==id,Tracker.Tracker_Id==id1).first()
            if tracker:
                logger=db.session.query(Logger).filter(Logger.Logger_Id==id2,Logger.Tracker_Id==id1).first()
                if logger:
                    logger.Time_Stamp=timeSt
                    logger.Value=val
                    logger.Note=note
                    db.session.commit()
            return {},201
        else:
            raise NotFoundError(status_code=404)

    def delete(self,user_id,password,Tracker_Id,Logger_Id):
        id=int(user_id)
        user=db.session.query(User).filter(User.user_id==id,User.password==password).first()
        if user:
            id2=int(Tracker_Id)
            tracker=db.session.query(Tracker).filter(Tracker.user_id==id,Tracker.Tracker_Id==id2).first()
            if tracker:
                id3=int(Logger_Id)
                logger=db.session.query(Logger).filter(Logger.Logger_Id==id3,Logger.Tracker_Id==id2).first()
                if logger:
                    db.session.delete(logger)
                    db.session.commit()
                    return {},201
                else:
                    raise NotFoundError(status_code=404)
            else:
                raise NotFoundError(status_code=404)        
        else:
            raise NotFoundError(status_code=404)
            
    def post(self,user_id,password,Tracker_Id):
        id=int(user_id)
        id1=int(Tracker_Id)
        args=create_logger_parser.parse_args()
        Logger_Id=args.get('Logger_Id',None)
        timeSt=args.get('Time_Stamp',None)
        val=args.get("Value",None)
        note=args.get('Note',None)    
        user=db.session.query(User).filter(User.user_id==id,User.password==password).first()
        if user:
            tracker=db.session.query(Tracker).filter(Tracker.user_id==id,Tracker.Tracker_Id==id1).first()
            if tracker:
                new_logger=Logger(Logger_Id=int(Logger_Id),Time_Stamp=timeSt,Value=val,Note=note,Tracker_Id =id1)
                db.session.add(new_logger)
                db.session.commit()
                return {},201
            else:
                raise BusinessValidationError(status_code=400,error_code="BE1003",error_message="Tracker_Id is invalid")
        if user_id is None or password is None:
            raise BusinessValidationError(status_code=400,error_code="BE1001",error_message="user_id or password is required")
        else:
            pass
        user=db.session.query(User).filter(User.user_id==int(user_id)).first()
        if user:
            raise BusinessValidationError(status_code=400,error_code="BE1002",error_message="duplicate user_id")


class SendImage_Logs(Resource):        
    def get(self,user_id,password,Tracker_Id):
        id=int(user_id)
        id1=int(Tracker_Id)
        user=db.session.query(User).filter(User.user_id==id,User.password==password).first()
        if user:
            tracker=db.session.query(Tracker).filter(Tracker.user_id==id,Tracker.Tracker_Id==id1).first()
            print('jh')
            if tracker:
                q='192.168.1.19:8080/Dashboard/'+str(id)+'/'+str(id1)+'/Visualize'
                return {'link':q}
        else:
            return "Image sending failed"

