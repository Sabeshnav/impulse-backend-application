from django.http import HttpResponse, JsonResponse
from baseview import Baseview, bodyParser, randomToken
from django.views import View
from tableDetails import Tables
import json


class Mentor(View, Baseview, Tables):

    # make an existing teacher mentor
    def post(self, request):
        data = bodyParser(request)
        teacher_id = data["teacher_id"]
        class_id = data["class_id"]
        class_id = str(class_id)
        teacher_id = str(teacher_id)
        temp = self.retrieve("mentor", "class", "(id = " + class_id + ")")
        if temp[0][0]:
            self.update("mentor = " + teacher_id, "class", "(id = " + class_id + ")")
        else:
            self.update("mentor = " + teacher_id, "class", "(id = " + class_id + ")")
        return HttpResponse("done")


class Student(View, Baseview, Tables):

    # add an existing user to a class
    def post(self, request, username):
        data = bodyParser(request)
        username = data["username"]
        user_id = data["user_id"]
        password = data["password"]
        class_id = data["class_id"]
        checker = self.retrieve("students", "class", "(id = " + str(class_id) + ")")
        checker = checker[0][0]
        checker = json.loads(str(checker))
        checker = str(checker["students"])
        checker = checker.split(",")
        token = randomToken()
        print(str(checker))
        check = 0
        for i in checker:
            if str(user_id) == str(i):
                check = 1
                break
        self.json_update("class", "students", str(user_id), "(id = \"" + str(class_id) + "\")")
        if check == 0:
            return HttpResponse(self.update(
                "class_id = \"" + str(class_id) + "\", password = \"" + str(password) + "\", token = \"" + str(token) + "\"",
                "users", "(username = \"" + username + "\")"), status=200)
        else:
            return HttpResponse("Student already added to the class!", status=409)

    # get an user
    def get(self, request, username):
        data = self.retrieve("*", "users", "(username=\"" + username + "\")")
        if data:
            data = data[0]
            res = {"id": data[0], "username": data[1], "email": data[2]}
            return JsonResponse(res, status=200)
        else:
            return HttpResponse("User doesn't exist!", status=403)

    # remove a student from a class
    def delete(self, request, username):
        user_id = request.headers['userid']
        return HttpResponse(self.update("class_id = NULL, password = NULL, token = NULL", "users", "(id = \"" + user_id + "\")"))


class Teacher(View, Baseview, Tables):

    # add a teacher
    def post(self, request, teacher_id):
        data = bodyParser(request)
        username = data["username"]
        password = data["password"]
        phone = data["phone"]
        email = data["email"]
        if self.retrieve("*", "teacher", "(name = \"" + username + "\")"):
            return HttpResponse("Teacher already exists!!", status=403)
        else:
            flag = True
            token = ""
            while flag:
                token = randomToken()
                if self.retrieve("*", "teacher", "(token=\"" + token + "\")"):
                    flag = True
                else:
                    flag = False
            self.insert("teacher", "(name, phone, email, subject_ids, class_ids, password, token)",
                        "(\"" + username + "\", \"" + phone + "\", \"" + email + "\", '{\"subject_ids\": \"\"}', '{\"class_ids\": \"\"}', \"" + password + "\", \"" + token + "\")")
            return HttpResponse("done", status=200)

    # get a teacher
    def get(self, request, teacher_id):
        data = self.retrieve("*", "teacher", "(id=\"" + teacher_id + "\")")
        if data:
            data = data[0]
            res = {"id": data[0], "name": data[1], "phone": data[2], "email": data[3]}
            return JsonResponse(res)
        else:
            return HttpResponse("Teacher doesn't exist!", status=403)

    # remove a teacher
    def delete(self, request, teacher_id):
        return HttpResponse(self.delete_row("teacher", "(id = " + teacher_id + ")"))


class ClassRoom(View, Baseview, Tables):

    # create a class
    def post(self, request, class_id):
        data = bodyParser(request)
        class_name = data["class_name"]
        #mentor = data["mentor"]
        if self.is_exists("class", "*", "(name = \""+class_name+"\")"):
            return HttpResponse("Class name already exists!", status=403)
        else:
            return HttpResponse(self.insert("class", "(name, mentor, teachers, students)", "(\"" + class_name + "\", 1 , '{\"teachers\": \"\"}', '{\"students\": \"\"}')"), status=200)

    # get the list of all classes
    def get(self, request, class_id):
        res = self.retrieve_all("class")
        class_ids = []
        class_names = []
        mentors = []
        teachers = []
        students = []
        for row in res:
            class_ids.append(row[0])
            class_names.append(row[1])
            mentors.append(row[4])
            teachers.append(row[2])
            students.append(row[3])
        result = {"class_ids": class_ids, "class_names": class_names, "mentors": mentors, "teachers": teachers, "students": students}
        print(str(result)+"asasas")
        return JsonResponse(result, status=200)

    # delete a class
    def delete(self, request, class_id):
        return HttpResponse(self.delete_row("class", "(id = " + class_id + ")"),status=200)


class ClassStudentList(View, Baseview, Tables):

    # get the list of students of a class
    def get(self, request):
        class_id = request.headers['class']
        res = self.retrieve("*", "users", "(class_id = " + class_id + ")")
        if res:
            user_ids = []
            usernames = []
            emails = []
            for row in res:
                user_ids.append(row[0])
                usernames.append(row[1])
                emails.append(row[2])
            result = {"user_ids": user_ids, "usernames": usernames, "emails": emails}
            print(str(result))
            return JsonResponse(result, status=200)
        else:
            return HttpResponse("This class has no students!!", status=404)


class ClassTeacherList(View, Baseview, Tables):

    # get the list of teachers of a class
    def get(self, request):
        class_id = request.headers['class']
        res = self.retrieve("teachers", "class", "(id = " + class_id + ")")
        res = res[0][0]
        print(str(res))
        res = json.loads(res)
        print(res["teachers"])
        res = res["teachers"]
        if res:
            res = res.split(",")
            print(res)
            l = ""
            for i in res:
                l = l + str(i) + ","
            l = l[:-1]
            l = "(" + l + ")"
            res = self.retrieve("*", "teacher", "id IN " + l)
            print(str(res))
            teacher_ids = []
            teachers = []
            phones = []
            emails = []
            for row in res:
                teacher_ids.append(row[0])
                teachers.append(row[1])
                phones.append(row[2])
                emails.append(row[3])
            result = {"teacher_ids": teacher_ids, "teachers": teachers, "phones": phones, "emails": emails}
            print(str(result))
            return JsonResponse(result, status=200)
        else:
            return HttpResponse("This class has no teachers!!", status=404)


class Subject(View, Baseview, Tables):

    # create a subject
    def post(self, request):
        data = bodyParser(request)
        subject_name = data["subject_name"]
        code = data["code"]
        category = data["category"]
        if self.is_exists("subject", "*", "(name = \"" + subject_name + "\")"):
            return HttpResponse("Subject already exists!", status=403)
        else:
            return HttpResponse(self.insert("subject", "(name, code, category)", "(\"" + subject_name + "\", \"" + str(code) + "\", " + str(category) + ")"))

    # get the list of all subjects
    def get(self, request):
        res = self.retrieve_all("subject")
        subject_ids = []
        names = []
        codes = []
        categories = []
        for row in res:
            subject_ids.append(row[0])
            names.append(row[1])
            codes.append(row[2])
            categories.append(row[3])
        result = {"subject_ids": subject_ids, "names": names, "codes": codes, "categories": categories}
        print(str(result))
        return JsonResponse(result, status=200)


class Category(View, Baseview, Tables):

    # create a category
    def post(self, request):
        data = bodyParser(request)
        name = data["name"]
        if self.is_exists("category", "*", "(name = \"" + name + "\")"):
            return HttpResponse("Category already exists!", status=403)
        else:
            return HttpResponse(self.insert("category", "(name)", "(\"" + name + "\")"))

    # get the list of all categories
    def get(self, request):
        res = self.retrieve_all("category")
        ids = []
        names = []
        categories = []
        for row in res:
            ids.append(row[0])
            names.append(row[1])
        result = {"category_ids": ids, "names": names}
        return JsonResponse(result, status=200)


class TeacherSubjectList(View, Baseview, Tables):

    # get the list of subjects of a teacher
    def get(self, request):
        teacher_id = request.headers['id']
        res = self.retrieve("subjects_ids", "teacher", "(id = " + teacher_id + ")")
        res = res[0][0]
        print(str(res))
        res = json.loads(res)
        print(res["subject_ids"])
        res = res["subject_ids"]
        res = res.split(",")
        print(res)
        l = ""
        for i in res:
            l = l + str(i) + ","
        l = l[:-1]
        l = "(" + l + ")"
        print(l)
        res = self.retrieve("*", "subject", "id IN " + l)
        print(str(res))
        subject_ids = []
        subject_names = []
        codes = []
        categories = []
        for row in res:
            subject_ids.append(row[0])
            subject_names.append(row[1])
            codes.append(row[2])
            categories.append(row[3])
        result = {"subject_ids": subject_ids, "subject_names": subject_names, "codes": codes, "categories": categories}
        print(str(result))
        return JsonResponse(result, status=200)


class GetAllTeacher(View, Baseview, Tables):

    # get the list of all teachers
    def get(self, request):
        res = self.retrieve_all("teacher")
        ids = []
        names = []
        emails = []
        phones = []
        for row in res:
            ids.append(row[0])
            names.append(row[1])
            phones.append(row[3])
            emails.append(row[5])
        result = {"teacher_ids": ids, "names": names, "emails": emails, "phones": phones}
        print(str(result))
        return JsonResponse(result, status=200)


class AddTeacherClass(View, Baseview, Tables):

    # add teacher to a class
    def post(self, request):
        data = bodyParser(request)
        class_id = data["class_id"]
        teacher_id = data["teacher_id"]
        checker = self.retrieve("teachers", "class", "(id = " + str(class_id) + ")")
        checker = checker[0][0]
        checker = json.loads(str(checker))
        checker = str(checker["teachers"])
        checker = checker.split(",")
        flag = 0
        for i in checker:
            if str(teacher_id) == str(i):
                flag = 1
                break
        print(flag)
        if flag == 0:
            self.json_update("teacher", "class_ids", str(class_id), "(id=" + str(teacher_id) + ")")
            return HttpResponse(self.json_update("class", "teachers", str(teacher_id), "(id=" + str(class_id) + ")"), status=200)
        else:
            return HttpResponse("Teacher already added to the class!", status=409)

