from flask import Flask, Response, request
import pymongo
import json
from bson.objectid import ObjectId 

app = Flask(__name__)

# connect db
try:
    mongo = pymongo.MongoClient(host="localhost", port=27017)
    db = mongo.todo
    print("INFO - success to connect db")
except:
    print("ERROR - cannot connect to db")

# Create todo
@app.route("/add_todo", methods=["POST"])
def create_todo():
    try:
        # static
        #todo = {"Title":"test", "Due_date":str(datetime.datetime(2022, 9, 30, 0, 0, 0))}
        # dynamic
        todo = {"Title":request.form["Title"], "Due_date":request.form["Due_date"]}
        dbResponse = db.todo.insert_one(todo)
        return Response(response=json.dumps({"message":"Add success!", "id":f"{dbResponse.inserted_id}"}), status=200, mimetype="application/json")
    except Exception as ex:
        print(ex)

# Find all todo
@app.route("/", methods=["GET"])
def find_todo():
    try:
        data = list(db.todo.find())
        for todo in data:
            todo["_id"] = str(todo["_id"])
        return Response(response=json.dumps(data), status=200, mimetype="application/json")
    except Exception as ex:
        print(ex)
        return Response(response=json.dumps({"message":"Cannot find todo!"}), status=500, mimetype="application/json")

# Update todo by id
@app.route("/update_todo/<id>", methods=["PATCH"])
def update_todo(id):
    try:
        dbResponse = db.todo.update_one({"_id":ObjectId(id)},{"$set":{"Title":request.form["Title"],"Due_date":request.form["Due_date"]}})
        if dbResponse.modified_count == 1:
            return Response(response=json.dumps({"message":"Update success!"}), status=200, mimetype="application/json")
        else:
            return Response(response=json.dumps({"message":"Notthing Update!"}), status=200, mimetype="application/json")
    except Exception as ex:
        print(ex)
        return Response(response=json.dumps({"message":"Cannot update todo!"}), status=500, mimetype="application/json")

# Delete todo by id
@app.route("/delete_todo/<id>", methods=["DELETE"])
def delete_todo(id):
    try:
        dbResponse = db.todo.delete_one({"_id":ObjectId(id)})
        if dbResponse.deleted_count == 1:
            return Response(response=json.dumps({"message":"Delete success!", "id":f"{id}"}), status=200, mimetype="application/json")
        else:
            return Response(response=json.dumps({"message":"Todo not found!"}), status=200, mimetype="application/json")
    except Exception as ex:
        print(ex)
        return Response(response=json.dumps({"message":"Cannot delete todo!"}), status=500, mimetype="application/json")

# default path "/"
@app.route("/", methods=["GET"])
def default_path():
    return "CRUD Operation with Flask & MongoDB !!!"

# start server
if __name__ == "__main__":
    app.run(port=5000, debug=True)