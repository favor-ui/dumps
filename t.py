


class all_file(Resource):  

    def get(self):
        # mongo_data1 = mongo.db.chosen_Test
        # mongo_data = mongo.db.chosen_facility
        mongo_data_p = mongo2.db.formal
        # mongo_data_d = mongo2.db.dependents
        # mongo_data = mongo2.db.facility_selection_Test

        allRecords = mongo_data_p.find()

        # allRecords = mongo_data_d.find()

        output = []

        list_records = list(allRecords)
        # print(list_records)

        for record in list_records:
            record["_id"] = str(record["_id"])
            output.append(record)


        p = pd.dataframe("output")

        p.to_excel("principals.xlsx", index = False)

        # d = pd.dataframe("output")

        # d.to_excel("dependents.xlsx", index = False)

        return {"data":output, "Status" : True}, 201
        
        
        

api.add_resource(all_file, '/to_file')


# class Get_all_principals(Resource):  
#     # @require_appkey
#     def get(self):
#         # mongo_data1 = mongo.db.chosen_Test
#         # mongo_data = mongo.db.chosen_facility
#         # mongo_data = mongo2.db.checkFacility_Test
#         # mongo_data = mongo2.db.facility_selection_Test
#         mongo_data = mongo2.db.formal

#         parser = reqparse.RequestParser(bundle_errors= True)
        
#         parser.add_argument("limit", type=int)
#         parser.add_argument("skip", type=int)
#         data = parser.parse_args()
        
#         array = mongo_data.find().limit(data["limit"]).skip(data["skip"])
#         records = list(array)
#         output = []

#         for record in records:
#             record["_id"] = str(record["_id"])
#             output.append(record)
#             total_enrollments = len(output)

#         if len(output) != 0:
#             return {"data" : output, "count":total_enrollments, "Status" : True}, 201
#         else:
#              return {"Message":"No records found", "Status":False }, 404

api.add_resource(Get_all_principals, '/all_principals')