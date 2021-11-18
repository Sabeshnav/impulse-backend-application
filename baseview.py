import json, string, random
from database import Database
from django.http import HttpResponse, JsonResponse
from mysql.connector import errorcode

"""
 --- Every Basic functions are defined here
"""


def jsonLoader(field, value):
    res = {}
    for i in range(0, len(field)):
        temp = "{\"" + str(field[i]) + "\" : \"" + str(value[i]) + "\"}"
        temp = json.loads(temp)
        res.update(temp)
    print(res)
    return res


def bodyParser(request):
    data = request.body.decode('utf-8')
    data = json.loads(data)
    return data


def randomToken():
    token = "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return token


class Baseview():
    dbs = Database()

    # ---------------------------------------------------CRUD---------------------------------------------------------

    def insert(self, table, columns, values):
        cnx = self.dbs.getConnection()
        cursor = self.dbs.getCursor(cnx=cnx)
        query = ("INSERT INTO " + table + " " + columns + " VALUES " + values)
        print(query)
        cursor.execute(query)
        emp = cursor.lastrowid
        cnx.commit()
        cursor.close()
        cnx.close()
        return HttpResponse(emp, status=200)

    def retrieve(self, columns, table, conditions):
        cnx = self.dbs.getConnection()
        cursor = self.dbs.getCursor(cnx=cnx)
        query = ("SELECT " + columns + " FROM " + table + " WHERE " + conditions)
        print(query)
        cursor.execute(query)
        res = cursor.fetchall()
        cnx.commit()
        cursor.close()
        cnx.close()
        print(res)
        return res

    def retrieve_all(self, table):
        cnx = self.dbs.getConnection()
        cursor = self.dbs.getCursor(cnx=cnx)
        query = ("SELECT * FROM " + table)
        print(query)
        cursor.execute(query)
        res = cursor.fetchall()
        cnx.commit()
        cursor.close()
        cnx.close()
        print(res)
        return res

    def update(self, values, table, condition):
        cnx = self.dbs.getConnection()
        cursor = self.dbs.getCursor(cnx=cnx)
        query = ("UPDATE " + table + " SET " + values + " WHERE " + condition)
        print(query)
        cursor.execute(query)
        cnx.commit()
        cursor.close()
        cnx.close()
        return "done"

    def delete_row(self, table, condition):
        cnx = self.dbs.getConnection()
        cursor = self.dbs.getCursor(cnx=cnx)
        query = ("DELETE FROM " + table + " WHERE " + condition)
        print(query)
        cursor.execute(query)
        cnx.commit()
        cursor.close()
        cnx.close()
        return "done"

    def json_update(self, table, column, value, condition):
        cnx = self.dbs.getConnection()
        cursor = self.dbs.getCursor(cnx=cnx)
        search_query = ("SELECT " + column + " FROM " + table + " WHERE " + condition)
        print(search_query)
        cursor.execute(search_query)
        res = cursor.fetchall()
        res = res[0][0]
        res = json.loads(str(res))
        print(res)
        lis = res[column]
        if lis:
            lis = lis + "," + value
            update_query = ("UPDATE " + table + " SET " + column + " = JSON_SET(" + column + ", '$." + column + "', " + "'" + lis + "') WHERE " + condition)
        else:
            lis = value
            update_query = ("UPDATE " + table + " SET " + column + " = JSON_SET(" + column + ", '$." + column + "', " + "'" + lis + "') WHERE " + condition)
        cursor.execute(update_query)
        cnx.commit()
        cursor.close()
        cnx.close()
        return "done"

    def json_edit(self, table, column, value, condition):
        cnx = self.dbs.getConnection()
        cursor = self.dbs.getCursor(cnx=cnx)
        search_query = ("SELECT " + column + " FROM " + table + " WHERE " + condition)
        print(search_query)
        cursor.execute(search_query)
        res = cursor.fetchall()
        res = res[0][0]
        res = json.loads(str(res))
        print(res)
        lis = res[column]
        if lis:
            lis = value
            update_query = ("UPDATE " + table + " SET " + column + " = JSON_SET(" + column + ", '$." + column + "', " + "'" + lis + "') WHERE " + condition)
        else:
            lis = value
            update_query = ("UPDATE " + table + " SET " + column + " = JSON_SET(" + column + ", '$." + column + "', " + "'" + lis + "') WHERE " + condition)
        cursor.execute(update_query)
        cnx.commit()
        cursor.close()
        cnx.close()
        return "done"

    def is_exists(self, table, column, condition):
        cnx = self.dbs.getConnection()
        cursor = self.dbs.getCursor(cnx=cnx)
        query = ("SELECT " + column + " FROM " + table + " WHERE " + condition)
        print(query)
        cursor.execute(query)
        res = cursor.fetchall()
        cnx.commit()
        cursor.close()
        cnx.close()
        if res:
            return True
        else:
            return False



"""
# generic APIs are defined here.

# ----------------------------------------------------auth APIs----------------------------------------------------

    def createUser(self, username, email, password, resource):


    def signIn(self,username,resource):
        db = self.getConnection()
        user_details = db[resource].find_one({"username":username})
        user_id = user_details["_id"]
        return HttpResponse(str(user_id),status=200)

# ----------------------------------------------content APIs----------------------------------------------------

    def insert(self, user_id, support_id, data, supportResource, resource):
        db = self.getConnection()
        support_id = convertToObjectId(support_id)
        date = str(datetime.now().date())
        time = str(datetime.now().time())
        user_details = db["auth_user"].find_one({"_id": convertToObjectId(user_id)})
        data.update({"inserted_date": date, "inserted_time": time, str(supportResource)+"_id": str(support_id), "username": user_details["username"]})
        obj_id = db[resource].insert_one(data).inserted_id
        if supportResource:
            resource_id = str(resource)+"_id"
            parent_doc = db[supportResource].find_one({"_id": support_id})
            try:
                resource_object = parent_doc[resource_id]
            except:
                parent_doc.update({resource_id: ""})
                resource_object = parent_doc[resource_id]
            resource_object = resource_object+str(obj_id)+","
            db[supportResource].update_one({"_id": support_id},{"$set": {resource_id: resource_object}})
        if resource not in ["question", "poll", "choice"]:
            resource_id = str(resource)+"_id"
            user_id = convertToObjectId(user_id)
            user_det = db["auth_user"].find_one({"_id": user_id})
            temp_string = user_det[resource_id]
            temp_string = temp_string + str(obj_id) + ","
            db["auth_user"].update_one({"_id": user_id}, {"$set": {resource_id: temp_string}})
            responses = db[supportResource].find_one({"_id": convertToObjectId(support_id)})
            responses = responses["responses"] + 1
            db[supportResource].update_one({"_id": convertToObjectId(support_id)}, {"$set": {"responses": responses}})
        if resource == 'poll':
            return str(obj_id)
        else:
            return HttpResponse(str(obj_id), status=200)

    def poll_retrieve(self, auth_user_id, resource):
        db = self.getConnection()
        if db["auth_user"].find_one({"_id": convertToObjectId(auth_user_id)}):
            result = list(db[resource].find().sort([('_id', pymongo.DESCENDING), 15]))
            return HttpResponse(str(result), status=200)
        else:
            return HttpResponse("invalid user ID", status=400)

    def retrieve(self, auth_user_id, support_id, resource, supportResource):
        db = self.getConnection()
        if db["auth_user"].find_one({"_id": convertToObjectId(auth_user_id)}):
            resource_id = resource+"_id"
            resource_ids = db[supportResource].find_one({"_id": convertToObjectId(support_id)})
            resource_ids = resource_ids[resource_id]
            resource_ids = resource_ids.split(',')
            result = []
            for i in resource_ids:
                if i:
                    result.append(db[resource].find_one({"_id": convertToObjectId(i)}))
            return HttpResponse(str(result), status=200)
        else:
            return HttpResponse("invalid user ID", status=400)

    def vote(self, auth_user_id, resource_id, resource):
        db = self.getConnection()
        if db["auth_user"].find_one({"_id": convertToObjectId(auth_user_id)}):
            value = db[resource].find_one({"_id": convertToObjectId(resource_id)})
            value = value["value"] + 1
            db[resource].update_one({"_id": convertToObjectId(resource_id)}, {"$set": {"value": value}})
            value = db[resource].find_one({"_id": convertToObjectId(resource_id)})
            value = value["value"]
            return HttpResponse(value, status=200)
        else:
            return HttpResponse("invalid user ID", status=400)

    def retrieve_user_content(self, auth_user_id, resource):
        db = self.getConnection()
        if db["auth_user"].find_one({"_id": convertToObjectId(auth_user_id)}):
            obj = db["auth_user"].find_one({"_id": convertToObjectId(auth_user_id)})
            resource_id = resource+"_id"
            result = []
            for i in obj[resource_id]:
                result.append(db[resource].find_one({"_id": convertToObjectId(i)}))
            return HttpResponse(str(result),status=200)
        else:
            return HttpResponse("invalid user ID", status=400)

    def follow(self, auth_user_id, follow_id, resource):
        db = self.getConnection()
        if db["auth_user"].find_one({"_id": convertToObjectId(auth_user_id)}):
            obj = db[resource].find_one({"_id": convertToObjectId(follow_id)})
            followers = obj["followers"] + 1
            db[resource].update_one({"_id": convertToObjectId(follow_id)}, {"$set": {"followers": followers}})
            value = db[resource].find_one({"_id": convertToObjectId(follow_id)})
            value = value["followers"]
            obj = db["auth_user"].find_one({"_id": convertToObjectId(auth_user_id)})
            obj = obj[str(resource)+"_id"]
            obj = obj+str(follow_id)+","
            db["auth_user"].update_one({"_id": convertToObjectId(auth_user_id)}, {"$set": {str(resource)+"_id": obj}})
            return HttpResponse(value, status=200)
        else:
            return HttpResponse("invalid user ID", status=400)

    def check_existence(self, auth_user_id, resource_id, resource):
        db = self.getConnection()
        if db["auth_user"].find_one({"_id": convertToObjectId(auth_user_id)}):
            obj = db["auth_user"].find_one({"_id": convertToObjectId(auth_user_id)})
            obj = obj[str(resource)+"_id"]
            if resource_id in obj:
                return HttpResponse(1, status=200)
            else:
                return HttpResponse(0, status=200)

    def question_feed_retrieve(self,auth_user_id,last_question_id,resource):
        db = self.getConnection()
        if db["auth_user"].find_one({"_id": convertToObjectId(auth_user_id)}):
            if last_question_id is None:
                print("none")
                result = list(db[resource].find().sort([('_id', pymongo.DESCENDING), ]).limit(15))
                return HttpResponse(str(result), status=200)
            else:
                print("is")
                result = list(db[resource].find({"_id":{"$lt":convertToObjectId(last_question_id)}}).sort([('_id', pymongo.DESCENDING), ]).limit(15))
                return HttpResponse(str(result), status=200)
        else:
            return HttpResponse("invalid user ID", status=400)
"""
