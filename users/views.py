from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.http import HttpResponse
from baseview import Baseview, bodyParser, jsonLoader
from django.views import View
from tableDetails import Tables
from django.contrib.auth.models import User

table = "users"


class Register(View, Baseview, Tables):

    def post(self, request):
        data = bodyParser(request)
        username = data["username"]
        email = data["email"]
        class_id = data["class_id"]
        if self.retrieve("username", "users", "(username=\""+username+"\")"):
            return HttpResponse("OOPS!! Username already taken!!", status=400)
        else:
            return HttpResponse(self.insert(table=table,columns=self.tables['users'],values="(\""+username+"\",\""+email+"\","+class_id+")"), status=200)


class UserDeatils(View, Baseview, Tables):

    def get(self,request,user_id):
        res = self.retrieve("*", table, "(id=" + user_id + ")")
        if res:
            field = ["username", "email"]
            value = [res[0][1], res[0][2]]
            print(value)
            res = jsonLoader(field, value)
            return HttpResponse(str(res), status=200)
        else:
            return HttpResponse("error!!", status=400)

