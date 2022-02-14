from facility import *
import requests

from datetime import datetime, date, timedelta

def cur_date():
    ti_me = datetime.now()
    c_time = ti_me.strftime("%Y:%m:%d %X")

    return c_time

time = cur_date()

# Facility Selection API in use with USSD
class AddUser_Facility(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('phone_number', type=str,required=True)
    parser.add_argument('submission_id',type=str,required=True)
    parser.add_argument('facility_code',type=str,required=True)
    
    def put(self):
        mongo_data = mongo2.db.formal
        
        # mongo_data = mongo2.db.facility_selection_Test


        data = AddUser_Facility.parser.parse_args()
        ph = data["phone_number"]
        
        findbeneficiary = mongo_data.find_one({"phone_number": ph, "submission_id":data["submission_id"]})

        if not findbeneficiary:
            return {"message":  "Beneficiary does not exist", "Status" : False}, 404
       
        checkbeneficiary = mongo_data.find({"phone_number": ph, "submission_id":data["submission_id"]})

        array = list(checkbeneficiary)
        # print(array)
        for entry in array:
            if entry["facility_name"].lower() != "nan":
                return {"message":"You have chosen a facility already you cannot change or add another", "Status": False }, 404
            
            else:
                excel_data_df = pd.read_csv("in_use.csv", dtype = str)
                # facilities = excel_data_df.to_dict('records')
                
                
                found = excel_data_df[excel_data_df["facility_code"]== data["facility_code"]]
                details = (found.values)

                if len(details) == 0:
                    return {"message": "Facility does not exist or has reach maximum, Please choose another facility", "Status" : False}, 404
                # print(details == [])
                
                else:
                    fn = details[0][0].strip()
                    wd = details[0][1].strip()
                    lga = details[0][2].strip()
                    fc = details[0][3].strip()  
                    myquery ={"phone_number": ph, "submission_id":data["submission_id"]}
                    newentry = {"$set":{"facility_code":data["facility_code"],"facility_name":fn, "printed":"False","phc_ward":wd, "phc_lga":lga, "Date":time}}
                    mongo_data.update_one(myquery,newentry)
                    return {"message":"Your facility choice has been updated", "Status" : True}, 201
        
api.add_resource(AddUser_Facility, '/updated')

# Change Hospital from Plateau Hospital to any other Hospital
class Change_from_Plateau(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('enrollment_id',type=str,required=True)
    parser.add_argument('facility_code',type=str,required=True)
    
    def put(self):
        mongo_data = mongo2.db.formal

        # mongo_data = mongo2.db.facility_selection_Test

        data = Change_from_Plateau.parser.parse_args()
        
        findbeneficiary = mongo_data.find_one({"enrollment_id":data["enrollment_id"]})
       
        if not findbeneficiary:
            return {"message":  "Beneficiary does not exist", "Status" : False}, 404
        
        
        checkbeneficiary = mongo_data.find({"enrollment_id":data["enrollment_id"]})

        array = list(checkbeneficiary)
        # print(array)
        for entry in array:
            if entry["facility_name"] != "Plateau State Specialist Hospital, Jos":
            # if entry["facility_code"] != "706512":
                return {"message":"You have chosen a facility already you cannot change or add another", "Status": False }, 404
            
            else:
                excel_data_df = pd.read_csv("in_use.csv", dtype = str)
                # facilities = excel_data_df.to_dict('records')
                
                
                found = excel_data_df[excel_data_df["facility_code"]== data["facility_code"]]
                details = (found.values)

                if len(details) == 0:
                    return {"message": "Facility does not exist or has reach maximum, Please choose another facility", "Status" : False}, 404
                # print(details == [])
                
                else:
                    fn = details[0][0].strip()
                    wd = details[0][1].strip()
                    lga = details[0][2].strip()
                    fc = details[0][3].strip()  
                    myquery ={"enrollment_id":data["enrollment_id"]}
                    newentry = {"$set":{"facility_code":data["facility_code"],"facility_name":fn, "phc_ward":wd, "phc_lga":lga}}
                    mongo_data.update_one(myquery,newentry)
                    return {"message":"Your facility choice has been updated", "Status" : True}, 201
        
api.add_resource(Change_from_Plateau, '/from_plateau')


class Alter_Facility(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('phone_number', type=str,required=True)
    parser.add_argument('submission_id',type=str,required=True)
    parser.add_argument('facility_code',type=str,required=True)
    
    def put(self):
        mongo_data = mongo2.db.formal
        # mongo_data = mongo2.db.facility_selection_Test

        data = Alter_Facility.parser.parse_args()
        ph = data["phone_number"]

        findbeneficiary = mongo_data.find_one({"phone_number": ph, "submission_id":data["submission_id"]})

        if not findbeneficiary:
            return {"message":  "Beneficiary does not exist", "Status" : False}, 404
       
        
        excel_data_df = pd.read_csv("in_use.csv", dtype = str)

        # excel_data_df = pd.read_excel("facility_details_july6.xlsx",sheet_name="full", dtype = str)
        # facilities = excel_data_df.to_dict('records')
        
        
        found = excel_data_df[excel_data_df["facility_code"]== data["facility_code"]]
        details = (found.values)

        if len(details) == 0:
            return {"message": "Facility does not exist or has reach maximum, Please choose another facility", "Status" : False}, 404
        # print(details == [])
        
        else:
            fn = details[0][0].strip()
            wd = details[0][1].strip()
            lga = details[0][2].strip()
            fc = details[0][3].strip()  
            myquery ={"phone_number": ph, "submission_id":data["submission_id"]}
            newentry = {"$set":{"facility_code":data["facility_code"],"facility_name":fn,"phc_ward":wd, "phc_lga":lga}}
            mongo_data.update_one(myquery,newentry)
            return {"message":"Your facility choice has been updated", "Status" : True}, 201
        
api.add_resource(Alter_Facility, '/alter')


class Change_SubID(Resource):
   
    parser = reqparse.RequestParser()

    parser.add_argument('phone_number', type=str,required=True)
    parser.add_argument('submission_id',type=str,required=True)
    parser.add_argument('new_sub_id',type=str,required=True)

    def put(self):
        mongo_data = mongo2.db.formal
        # mongo_data = mongo2.db.facility_selection_Test

        data = Change_SubID.parser.parse_args()
        ph = data["phone_number"]
        sid = data["submission_id"]
        nsid = data["new_sub_id"]

        findbeneficiary = mongo_data.find_one({"phone_number": ph, "submission_id":sid})

        if not findbeneficiary:
            return {"message":  "Beneficiary does not exist", "Status" : False}, 404
        
        myquery ={"phone_number": ph, "submission_id":sid}
        newentry = {"$set":{"submission_id":nsid}}
        mongo_data.update_one(myquery,newentry)
        return {"message":"Your Submission ID has been updated", "Status" : True}, 201
        
api.add_resource(Change_SubID, '/change_sid')



class Change_Phone_number(Resource):
   
    parser = reqparse.RequestParser()

    parser.add_argument('phone_number', type=str,required=True)
    parser.add_argument('submission_id',type=str,required=True)
    parser.add_argument('new_phone_number',type=str,required=True)

    def put(self):
        mongo_data = mongo2.db.formal
        # mongo_data = mongo2.db.facility_selection_Test

        data = Change_Phone_number.parser.parse_args()
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
        
api.add_resource(Change_Phone_number, '/correct_phone')

class Change_name(Resource):
   
    parser = reqparse.RequestParser()

    parser.add_argument('phone_number', type=str,required=True)
    parser.add_argument('submission_id',type=str,required=True)
    parser.add_argument('new_submission_id',type=str,required=True)
    parser.add_argument('new_name',type=str,required=True)
    parser.add_argument('date_of_birth',type=str,required=True)
    parser.add_argument('gender',type=str,required=True)

    def put(self):
        mongo_data = mongo2.db.formal
        # mongo_data = mongo2.db.facility_selection_Test

        data = Change_name.parser.parse_args()
        ph = data["phone_number"]
        sid = data["submission_id"]
        nsid = data["new_submission_id"]
        nname = data["new_name"]
        dob = data["date_of_birth"]
        sex = data["gender"]

        findbeneficiary = mongo_data.find_one({"phone_number": ph, "submission_id":sid})

        if not findbeneficiary:
            return {"message":  "Beneficiary does not exist", "Status" : False}, 404
        
        myquery ={"phone_number": ph, "submission_id":sid}
        newentry = {"$set":{"name":nname,"date_of_birth":dob,"submission_id":nsid,"gender":sex}}
        mongo_data.update_one(myquery,newentry)
        return {"message":"Your record has been updated successfully", "Status" : True}, 201
        
api.add_resource(Change_name, '/change_name')

class Revert_EID(Resource):
   
    parser = reqparse.RequestParser()

    parser.add_argument('phone_number', type=str,required=True)
    parser.add_argument('submission_id',type=str,required=True)
    parser.add_argument('new_enrollment_id',type=str,required=True)

    def put(self):
        mongo_data = mongo2.db.formal
        # mongo_data = mongo2.db.facility_selection_Test

        data = Revert_EID.parser.parse_args()
        ph = data["phone_number"]
        sid = data["submission_id"]
        n_eid = data["new_enrollment_id"]

        findbeneficiary = mongo_data.find_one({"phone_number": ph, "submission_id":sid})

        if not findbeneficiary:
            return {"message":  "Beneficiary does not exist", "Status" : False}, 404
        
        myquery ={"phone_number": ph, "submission_id":sid}
        newentry = {"$set":{"enrollment_id":n_eid}}
        mongo_data.update_one(myquery,newentry)
        return {"message":"Your Enrollment ID has been updated", "Status" : True}, 201
        
api.add_resource(Revert_EID, '/revert_enrID')

class Get_Prin_by_enrID(Resource):  
    
    # @require_appkey
    def get(self):
        # mongo_data1 = mongo.db.chosen_Test
        # mongo_data = mongo.db.chosen_facility
        mongo_data = mongo2.db.formal
        # mongo_data = mongo2.db.facility_selection_Test
        parser = reqparse.RequestParser()
        parser.add_argument("enrollment_id", type=str,required=True,help="Enrollment ID must be 10 digits and cannot be left blank")
   
        data = parser.parse_args()

        eid = data["enrollment_id"]
        allRecords = mongo_data.find({"enrollment_id":eid})

        output = []
        list_records = list(allRecords)
        # print(list_records)

        for record in list_records:
            record["_id"] = str(record["_id"])
            output.append(record)

        if len(output) != 0:
            return {"data" : output,"Status" : True}, 201
        else:
             return {"Message":"No records found", "Status":False }, 404

api.add_resource(Get_Prin_by_enrID, '/prin_enrID')

class Get_prin_by_subid(Resource):  
    parser = reqparse.RequestParser()
    parser.add_argument("submission_id", type=str,required=True,help="submission id must be more than 3 digits and cannot be left blank")
   
    # @require_appkey
    def get(self):
        # mongo_data1 = mongo.db.chosen_Test
        # mongo_data = mongo.db.chosen_facility
        mongo_data = mongo2.db.formal
        # mongo_data = mongo2.db.facility_selection_Test
        
        data = Get_prin_by_subid.parser.parse_args()
    
        sid = data["submission_id"]
        allRecords = mongo_data.find({"submission_id":sid})

        output = []
        list_records = list(allRecords)
        # print(list_records)

        for record in list_records:
            record["_id"] = str(record["_id"])
            output.append(record)

        if len(output) != 0:
            return {"data" : output, "Status" : True}, 201
        else:
             return {"message":"No records found", "Status":False }, 404

api.add_resource(Get_prin_by_subid, '/prin_subid')


class Get_all_principals(Resource):  
    # @require_appkey
    def get(self):
        # mongo_data1 = mongo.db.chosen_Test
        # mongo_data = mongo.db.chosen_facility
        # mongo_data = mongo2.db.checkFacility_Test
        # mongo_data = mongo2.db.facility_selection_Test
        mongo_data = mongo2.db.formal

        parser = reqparse.RequestParser(bundle_errors= True)
        
        parser.add_argument("limit", type=int)
        parser.add_argument("skip", type=int)
        data = parser.parse_args()
        
        array = mongo_data.find().limit(data["limit"]).skip(data["skip"])
        records = list(array)
        output = []

        for record in records:
            record["_id"] = str(record["_id"])
            output.append(record)
            total_enrollments = len(output)

        if len(output) != 0:
            return {"data" : output, "count":total_enrollments, "Status" : True}, 201
        else:
             return {"Message":"No records found", "Status":False }, 404

api.add_resource(Get_all_principals, '/all_principals')


class Get_prin_by_phone(Resource):  
    parser = reqparse.RequestParser()
    parser.add_argument("phone_number", type=str,required=True,help="Phone Number must be 11 digits and cannot be left blank")
    
    # @require_appkey
    def get(self):
        # mongo_data1 = mongo.db.chosen_Test
        # mongo_data = mongo.db.chosen_facility
        mongo_data = mongo2.db.formal
        # mongo_data = mongo2.db.facility_selection_Test
        
        data = Get_prin_by_phone.parser.parse_args()
    
        if len(data["phone_number"]) != 11 or len(''.join(i for i in data["phone_number"] if i.isdigit())) != 11:
            return {"Error": "Phone number must be 11 digits","Status": False}, 404

        ph = data["phone_number"]
        allRecords = mongo_data.find({"phone_number":ph})

        output = []
        list_records = list(allRecords)
        # print(list_records)

        for record in list_records:
            record["_id"] = str(record["_id"])
            output.append(record)

        if len(output) != 0:
            return {"data" : output,"Status" : True}, 201
        else:
             return {"Message":"No records found", "Status":False }, 404

api.add_resource(Get_prin_by_phone, '/prin_phone')


class Get_Deps_enrid(Resource):  
    parser = reqparse.RequestParser()
    parser.add_argument("principal's_enrid", type=str,required=True,help="Phone number must be 11 digits and cannot be empty")
   
    # @require_appkey
    def get(self):
        # mongo_data1 = mongo.db.chosen_Test
        # mongo_data = mongo.db.chosen_facility
        mongo_data = mongo2.db.dependents
        # mongo_data = mongo2.db.facility_selection_Test
        
        data = Get_Deps_enrid.parser.parse_args()
    
        enrid = data["principal's_enrid"]
        allRecords = mongo_data.find({"principals_enrid":enrid})

        output = []
        list_records = list(allRecords)
        # print(list_records)

        for record in list_records:
            record["_id"] = str(record["_id"])
            output.append(record)

        if len(output) != 0:
            return {"data" : output, "Status" : True}, 201
        else:
             return {"message":"No records found", "Status":False }, 404

api.add_resource(Get_Deps_enrid, '/dep_enrid')

class Get_dep_subid(Resource):  
    parser = reqparse.RequestParser()
    parser.add_argument("submission_id", type=str,required=True,help="submission id must be more than 3 digits and cannot be left blank")
   
    # @require_appkey
    def get(self):
        # mongo_data1 = mongo.db.chosen_Test
        # mongo_data = mongo.db.chosen_facility
        mongo_data = mongo2.db.dependents
        # mongo_data = mongo2.db.facility_selection_Test
        
        data = Get_dep_subid.parser.parse_args()
    
        sid = data["submission_id"]

        allRecords = mongo_data.find({"principal_s_submission_id":sid})

        output = []
        list_records = list(allRecords)
        # print(list_records)

        for record in list_records:
            record["_id"] = str(record["_id"])
            output.append(record)

        if len(output) != 0:
            return {"data" : output, "Status" : True}, 201
        else:
             return {"message":"No records found", "Status":False }, 404

api.add_resource(Get_dep_subid, '/dep_subid')

class Remove_Dups(Resource):
    
    parser = reqparse.RequestParser()

    parser.add_argument('submission_id', type=str,required=True,help="Submission ID cannot be left blank")
    parser.add_argument('blood_group',type=str,required=True,help="Blood Group cannot be left blank")
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
        
        mongoA = mongo2.db.Achieve
        mongo_data = mongo2.db.formal
        
        data = Remove_Dups.parser.parse_args()

        query = {"submission_id": data["submission_id"],"blood_group":data["blood_group"]}
        
        myquery = mongo_data.find(query)

        if myquery:
        
            removestaff = {"$unset":{"blood_group":data["blood_group"]}}
            
            mongoA.insert(query)

            mongo_data.update_one(query,removestaff) 

            return {"Message":"Successful", "Status": True},200      
        else:
            return {"Message":"No record found","Status": False}, 404

        
api.add_resource(Remove_Dups, '/del_dups')

class claimsForm(Resource):    
    def post(self):
        mongo_data1 = mongo.db.claims_form
        # mongo_data = mongo.db.claims_Test

        # claims form
        parser = reqparse.RequestParser()

        parser.add_argument('Health_Facility_Code', type=str,required=True)
        parser.add_argument('OIC_Name',type=str,required=True)
        parser.add_argument('Facility_Telephone',type=str,required=True)
        parser.add_argument('Referral_Date', type=str)       
        parser.add_argument('Beneficiary’s_ID',type=str,required=True)
        parser.add_argument('Daignosis',type=str,required=True)
        parser.add_argument('Services_Rendered', type=str,required=True)
        parser.add_argument('Encounter_Code',type=str,required=True)
        parser.add_argument('Cost',type=str,required=True)
        
        data = parser.parse_args()

        if len(data["Facility_Telephone"]) != 11 or len(''.join(i for i in data["Facility_Telephone"] if i.isdigit())) != 11:
            return {"Error": "Facility_Telephone number must be 11 digits","Status": False}, 404
        
        elif len(data["OIC_Name"]) < 2 or len(''.join(i for i in data["OIC_Name"] if i)) < 2:
            return {"Error": "OIC_Name cannot not be less than 2 characters long be 11 digits","Status": False}, 404

        elif len(data['OIC_Name']) > 100 or len(''.join(i for i in data['OIC_Name'] if i )) > 100:
            return {"Error": "OIC Name  cannot be more than one hundred characters long","Status": False}, 404

        elif len(data["Health_Facility_Code"]) != 6 or len(''.join(i for i in data["Health_Facility_Code"] if i.isdigit())) != 6:
            return {"Error": "Health_Facility_Code must be 6 digits","Status": False}, 404

        elif len(data["Beneficiary’s_ID"]) != 9 or len(''.join(i for i in data["Beneficiary’s_ID"] if i.isdigit())) != 9:
            return {"Error": "Beneficiary’s_ID must be 9 digits","Status": False}, 404

        else:

            post_claim = {
                'Health_Facility_Code':data['Health_Facility_Code'],'OIC_Name':data['OIC_Name'],'Facility_Telephone':data['Facility_Telephone'],'Referral_Date':data['Referral_Date'],'Beneficiary’s_ID':data['Beneficiary’s_ID'],'Daignosis':data['Daignosis'],'Services_Rendered':data['Services_Rendered'],'Encounter_Code':data['Encounter_Code'],'Cost':data['Cost']
                }

            mongo_data1.insert(post_claim)

            return {"message": "Data uploaded successfully ", "Status": True}, 200
        
   
    # @require_appkey
    def get(self):
        
        mongo_data1 = mongo.db.claims_form
        # mongo_data = mongo.db.claims_Test

        parser = reqparse.RequestParser(bundle_errors= True)

        parser.add_argument('Health_Facility_Code', type=str,required=True)
        
        data = parser.parse_args()

        if len(data["Health_Facility_Code"]) != 6 or len(''.join(i for i in data["Health_Facility_Code"] if i.isdigit())) != 6:
            return {"Error": "Health_Facility_Code must be 6 digits","Status": False}, 404
        
        output = []

        # myquery = {'OIC_NUMBER':data['OIC_NUMBER']}
        for q in mongo_data1.find({'Health_Facility_Code':data['Health_Facility_Code']}):
            if q:
                q["_id"] = str(q["_id"])
            
                output.append(q)
            else:
                output = "No results"
        
        return {"Claims Details " :  output, "Status": True },200

api.add_resource(claimsForm, '/secondary_claims')


class GetallClaims(Resource):  
    # @require_appkey
    def get(self):
        mongo_data1 = mongo.db.claims_form
        # mongo_data = mongo.db.claims_Test

        parser = reqparse.RequestParser(bundle_errors= True)
        
        parser.add_argument("limit", type=int)
        parser.add_argument("skip", type=int)
        data = parser.parse_args()
        
        records = mongo_data1.find().limit(data["limit"]).skip(data["skip"])
        output = []
        for record in records:
            record["_id"] = str(record["_id"])
            output.append(record)

        if len(output) != 0:
            return {"data" : output, "Status" : True}, 201
        else:
             return {"message":"No records found", "Status":False }, 404

api.add_resource(GetallClaims, '/getall_claims')


class Get_toFile(Resource):  
    # @require_appkey
    def get(self):
        mongo_data = mongo2.db.formal
        # mongo_data = mongo2.db.formal_old
        # mongo_data = mongo2.db.dependents
        # mongo_data = mongo2.db.dependents_old
        records = mongo_data.find()
        output = []
        for record in records:
            record["_id"] = str(record["_id"])
            output.append(record)

        df = pd.DataFrame(output)
        df.to_excel("principals.xlsx", index = False)
        # df.to_excel("principals_old.xlsx", index = False)
        # df.to_excel("dependents.xlsx", index = False)
        # df.to_excel("dependents_o
        ld.xlsx", index = False)

        if len(output) != 0:
            return {"data" : "Done", "Status" : True}, 201
        else:
            return {"Message":"No records found", "Status":False }, 404

api.add_resource(Get_toFile, '/to_file')