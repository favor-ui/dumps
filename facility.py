from flask import Flask, jsonify, request, make_response
from flask_restful import Resource, Api, reqparse
from flask_pymongo import PyMongo
import os, sys
import requests, json
from functools import wraps
from config import Config
import pandas as pd


app = Flask(__name__)

app.config.from_object(Config)

mongo = PyMongo(app)

# app.config['MONGO2_DBNAME'] = 'dbname_two'
# mongo2 = PyMongo(app, config_prefix='MONGO2')

# mongo2 = PyMongo(app, os.environ.get('MONGO_URI_1'))

mongo2 = PyMongo(app, uri = "mongodb+srv://idl:idl123@idl.hgmwm.mongodb.net/Enrollment?retryWrites=true&w=majority")

api = Api(app)


# Base URL
@app.route('/')
def index():
    return {"Message": "It's working", "Status" : True}, 200

class Upload(Resource):
    parser = reqparse.RequestParser()

    # parser.add_argument('Phone_Number', type=str,required=True)
    # parser.add_argument('Submission_ID',type=str,required=True)
    # parser.add_argument('Facility_Code',type=str,required=True)  
    
    def post(self):
        mongo_data = mongo.db.facility_details
        # mongo_data1 = mongo.db.Test
        # convert data to a dateframe, then to dictionary
        excel_data_df = pd.read_excel('facility_details_july6.xlsx', sheet_name = "All",  dtype = str)
        all_records = excel_data_df.to_dict('records')

        mongo_data.insert_many(all_records)

        return {"Message": "Data uploaded successfully ", "Status": True}, 200

api.add_resource(Upload, '/upload/facilities')

class Add_Staff(Resource):
    mongo_data = mongo.db.facility_details
    
    parser = reqparse.RequestParser()

    parser.add_argument('OIC_NUMBER', type=str,required=True,help="Officer in Charge's Number must be 11 digits and cannot be left blank")
    parser.add_argument('STAFF_NUMBER',type=str,required=True,help="customer_phone must be 11 digits and cannot be left blank")

    def put(self):
        mongo_data = mongo.db.facility_details
        data = Add_Staff.parser.parse_args()
        
        if data['OIC_NUMBER'] == data['STAFF_NUMBER']:
            return {"Error!!!": "Same Contact details!","Status": False}, 404
        
        checkoic = mongo_data.find_one({"OIC_NUMBER": data['OIC_NUMBER']})
        if not checkoic:
            return {"Message":  "UnAuthorised", "Status" : False}, 404

        for q in mongo_data.distinct("OIC_NUMBER"):
            if q == data["STAFF_NUMBER"]:
                return {"Message":  "UnAuthorised", "Status" : False}, 404

        checkstaff = mongo_data.find_one({"STAFF_NUMBER.{}".format(data['STAFF_NUMBER']):True})
        if checkstaff:
            return {"Message":"Staff already added", "Status": False }, 404

        if checkoic:
            myquery ={"OIC_NUMBER": data["OIC_NUMBER"]}
            newentry = [{"$set":{"STAFF_NUMBER":{data["STAFF_NUMBER"]: True}}}]
            mongo_data.update_one(myquery,newentry)

            return {"Message":"Your Number %s has been successfully added" %data["STAFF_NUMBER"], "Status" : True}, 201
        else:
            return {"Message":"This number is Unauthorized", "Status": False}, 404
        
api.add_resource(Add_Staff, '/staff/add')

# route to Remove staff
class DeleteStaff(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('OIC_NUMBER', type=str,required=True,help="Officer in Charge's Number must be 11 digits and cannot be left blank")
    parser.add_argument('STAFF_NUMBER',type=str,required=True,help="customer_phone must be 11 digits and cannot be left blank")
    # Get achieve
    def get(self):
        mongoA = mongo.db.Achieve
        output = []

        for q in mongoA.find():
            q["_id"] = str(q["_id"])
            output.append(q)
        return {"result": output, "Status" : True}, 200

    # Remove contact
    def put(self):
        mongoA = mongo.db.Achieve
        mongo_data = mongo.db.facility_details
        data = DeleteStaff.parser.parse_args()

        if data['OIC_NUMBER'] == data['STAFF_NUMBER']:
            return {"Error": "Same Contact details!","Status": False}, 404
        
        # stub for the above commented function (checking if agent exists)
        checkoic = mongo_data.find_one({"OIC_NUMBER": data['OIC_NUMBER']})
        if not checkoic:
            return {"Message":"You are Unauthorized","Status": False}, 404

        myquery =mongo_data.find({"OIC_NUMBER": data["OIC_NUMBER"],"STAFF_NUMBER.{}".format(data["STAFF_NUMBER"]): True})
        
        if myquery:
            queryoic = {"OIC_NUMBER": data["OIC_NUMBER"]}

            removestaff = {"$unset":{"STAFF_NUMBER.{}".format(data['STAFF_NUMBER']):True}}
            
            mongoA.insert({"STAFF_NUMBER":{data["STAFF_NUMBER"]: True}})

            mongo_data.update_one(queryoic,removestaff) 

            return {"Message":"Successful", "Status": True},200      
        else:
            return {"Message":"No record found","Status": False}, 404
           
        # return {"message" : "Contact details for Staff %s removed successfully" %data['STAFF_NUMBER']}
        
api.add_resource(DeleteStaff, '/delete')

class Getone(Resource):  
    parser = reqparse.RequestParser()
    parser.add_argument("OIC_NUMBER", type=str,required=True,help="Officer in Charge's must be 11 digits and cannot be left blank")
   
    # @require_appkey
    def get(self):
        data = Getone.parser.parse_args()
        mongo_data = mongo.db.facility_details
        
        if len(data["OIC_NUMBER"]) != 11 or len(''.join(i for i in data["OIC_NUMBER"] if i.isdigit())) != 11:
            return {"Error": "OIC Contact must be 11 digits","Status": False}, 404

        output = []

        # myquery = {'OIC_NUMBER':data['OIC_NUMBER']}
        for q in mongo_data.find({"OIC_NUMBER":data["OIC_NUMBER"]}):
            if q:
                q["_id"] = str(q["_id"])
            
                output.append(q)
            else:
                output = "No results"
        
        return {"facilitdatails " :  output, "Status": True },200

api.add_resource(Getone, '/OIC')

class Change_OIC_Phone_number(Resource):
   
    parser = reqparse.RequestParser()

    parser.add_argument('phone_number', type=str,required=True)
    parser.add_argument('submission_id',type=str,required=True)
    parser.add_argument('new_phone_number',type=str,required=True)

    def put(self):
        mongo_data = mongo2.db.formal
        # mongo_data = mongo2.db.facility_selection_Test

        data = Change_OIC_Phone_number.parser.parse_args()
        ph = data["phone_number"]
        sid = data["submission_id"]
        nph = data["new_phone_number"]

        findbeneficiary = mongo_data.find_one({"phone_number": ph, "submission_id":sid})

        if not findbeneficiary:
            return {"message":  "Beneficiary does not exist", "Status" : False}, 404
        
        myquery ={"phone_number": ph, "submission_id":sid}
        newentry = {"$set":{"phone_number":nph}}
        mongo_data.update_one(myquery,newentry)
        return {"message":"Your Phone Number has been updated successfully", "Status" : True}, 201
        
api.add_resource(Change_OIC_Phone_number, '/correct_oic_phone')

class Get_facility(Resource):  
    parser = reqparse.RequestParser()
    parser.add_argument("facility_code", type=str,required=True,help="Facility Code must be 6 digits and cannot be left blank")
   
    # @require_appkey
    def get(self):
        data = Get_facility.parser.parse_args()
        mongo_data = mongo.db.facility_details
        
        if len(data["facility_code"]) != 6 or len(''.join(i for i in data["facility_code"] if i.isdigit())) != 6:
            return {"Error": "Facility Code must be 6 digits","Status": False}, 404

        output = []

        # myquery = {'OIC_NUMBER':data['OIC_NUMBER']}
        f_c = data["facility_code"]
        for q in mongo_data.find({"facility_code":data["facility_code"]}):
            if q:
                q["_id"] = str(q["_id"])
            
                output.append(q)
            else:
                output = "No results"
        
        return {"facilitdatails " :  output, "Status": True },200

api.add_resource(Get_facility, '/facility')

class Update_Record(Resource):

    parser = reqparse.RequestParser()
   
    parser.add_argument("facility_name", type=str,required=True,help="Facility Name cannot be left blank")
    parser.add_argument("facility_type", type=str,required=True,help="Facility Type be left blank")
    parser.add_argument("services", type=str,required=True,help="Services cannot be left blank")
    parser.add_argument("oic_number", type=str,required=True,help="OIC Number cannot be left blank")
    parser.add_argument("oic_number2", type=str,required=False,help="OIC Number2 can be left blank")
    parser.add_argument("lga", type=str,required=True,help="LGA cannot be left blank")
    parser.add_argument("ward", type=str,required=True,help="Ward cannot be left blank")
    parser.add_argument("facility_code", type=str,required=True,help="Facility Code cannot be left blank")

    def put(self):
        # mongo_data = mongo2.db.facility_selection_Test
        mongo_data = mongo.db.facility_details
        data = Update_Record.parser.parse_args()

        # variables

        fn = data["facility_name"].strip()
        ft = data["facility_type"].strip()
        ser = data["services"].strip()
        oic1 = data["oic_number"].strip()
        oic2 = data["oic_number2"].strip()
        # oic2 = str(int(data[x]["oic_number2"])).,
        wd = data["ward"].strip()
        lg = data["lga"].strip()
        fc = data["facility_code"].strip()

        myquery ={"facility_code": fc}
        newentry = {"$set":{"facility_name": fn,"facility_type":ft, "services":ser,"oic_number":oic1, "oic_number2":oic2, "ward":wd, "lga":lg}}
        
        mongo_data.update_one(myquery,newentry)
            
        return {"message":"Facility Details updated successfully", "Status" : True}, 201

api.add_resource(Update_Record, '/update_facility_details')


class Getall(Resource):  
    # @require_appkey
    def get(self):
        mongo_data = mongo.db.facility_details
        parser = reqparse.RequestParser()
        parser.add_argument("limit", type=int)
        parser.add_argument("skip", type=int)
        data = parser.parse_args()
        
        records = mongo_data.find().limit(data["limit"]).skip(data["skip"])
        output = []
        for record in records:
            record["_id"] = str(record["_id"])
            output.append(record)

        if len(output) != 0:
            return {"data" : output, "Status" : True}, 201
        else:
             return {"Message":"No records found", "Status":False }, 404

api.add_resource(Getall, '/all/facilities')


class Facility_toFile(Resource):  
    # @require_appkey
    def get(self):
        mongo_data = mongo.db.facility_details
        records = mongo_data.find()
        output = []
        for record in records:
            record["_id"] = str(record["_id"])
            output.append(record)

        df = pd.DataFrame(output)
        df.to_excel("all_facilities.xlsx", index = False)

        if len(output) != 0:
            return {"data" : "Done", "Status" : True}, 201
        else:
             return {"Message":"No records found", "Status":False }, 404

api.add_resource(Facility_toFile, '/fc_file')



@app.errorhandler(400)
def bad_request__error(exception):
    return jsonify(
        {
            "Message": "Sorry you entered wrong values kindly check and resend!"
        },
        {
            "status": 400
        }
    )


@app.errorhandler(401)
def internal_error(error):
    return jsonify(
        {
            "Message": "Access denied ! please register and login to generate API KEY"
        },
        {
            "status": 401
        }
    )


@app.errorhandler(404)
def not_found_error(error):
    return jsonify(
        {
            "Message": "Sorry the page your are looking for is not here kindly go back"
        },
        {
            "status": 404
        }
    )


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify(
        {
            "Message": "Sorry the requested method is not allowed kindly check and resend !"
        },
        {
            "status": 405
        }
    )


@app.errorhandler(500)
def internal_server_error(error):
    return jsonify(
        {
            "Message": "Bad request please check your input and resend !"
        },
        {
            "status": 500
        }
    )


@app.errorhandler(501)
def server_not_found_error(error):
    return jsonify(
        {
            "Message": "inter server error"
        },
        {
            "status": 501
        }
    )