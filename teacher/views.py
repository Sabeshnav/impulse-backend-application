from django.http import HttpResponse, JsonResponse
from baseview import Baseview, bodyParser, jsonLoader
from django.views import View
import json
from tableDetails import Tables

table = 'teacher'


class Login(Baseview, View):

    # logs a teacher into the class
    def post(self, request):
        data = bodyParser(request)
        username = data['username']
        password = data['password']
        details = self.retrieve("*", "teacher", "(name = \"" + username + "\")")
        if details:
            if password == str(details[0][7]):
                return HttpResponse(str(details[0][8]), status=200)
            else:
                return HttpResponse("Incorrect password!", status=401)
        else:
            return HttpResponse("Teacher with the given username has not been added!!", status=403)


class DailyTest(Baseview, View):

    # create a test
    def post(self, request, teacher_id):
        token = request.headers['token']
        data = bodyParser(request)
        test_name = data['test_name']
        description = data['description']
        if self.retrieve("*", "teacher", "(token = \"" + token + "\")"):
            test_id = self.insert("daily_test", "(name, description, teacher_id, live)",
                                  "(\"" + test_name + "\", '{\"description\": \"" + description + "\"}', " + teacher_id + ", \"0\")")
            return HttpResponse(test_id, status=200)
        else:
            return HttpResponse("Un-authenticated user!", status=403)

    # put questions
    def put(self, request, teacher_id):
        test_id = request.headers['testid']
        data = bodyParser(request)
        question = data['question']
        choices = data['choices']
        choice_count = data['choice_count']
        correct_choice = data['correct_choice']
        max_marks = data['max_marks']
        self.insert("daily_question", "(test_id, question, choice_count, choices, correct, max_marks)",
                    "(\"" + str(test_id) + "\", '{\"question\": \"" + str(question) + "\"}', " + str(choice_count) + ", '{\"choices\": " + str(choices) + "}' , " + str(correct_choice) + ", \"" + str(max_marks) + "\")")
        return HttpResponse("done", status=200)


class WeeklyTest(Baseview, View):

    # create a test
    def post(self, request, teacher_id):
        token = request.headers['token']
        data = bodyParser(request)
        test_name = data['test_name']
        description = data['description']
        if self.retrieve("*", "teacher", "(token = \"" + token + "\")"):
            test_id = self.insert("weekly_test", "(name, description, teacher_id, live)",
                                  "(\"" + test_name + "\", '{\"description\": \"" + description + "\"}', " + teacher_id + ", \"0\")")
            return HttpResponse(test_id, status=200)
        else:
            return HttpResponse("Un-authenticated user!", status=403)

    # put questions
    def put(self, request, teacher_id):
        test_id = request.headers['testid']
        data = bodyParser(request)
        question = data['question']
        choices = data['choices']
        choice_count = data['choice_count']
        correct_choice = data['correct_choice']
        max_marks = data['max_marks']
        self.insert("weekly_question", "(test_id, question, choice_count, choices, correct, max_marks)",
                    "(\"" + str(test_id) + "\", '{\"question\": \"" + str(question) + "\"}', " + str(choice_count) + ", '{\"choices\": " + str(choices) + "}' , " + str(correct_choice) + ", \"" + str(max_marks) + "\")")
        return HttpResponse("done", status=200)


class MonthlyTest(Baseview, View):

    # create a test
    def post(self, request, teacher_id):
        token = request.headers['token']
        data = bodyParser(request)
        test_name = data['test_name']
        description = data['description']
        if self.retrieve("*", "teacher", "(token = \"" + token + "\")"):
            test_id = self.insert("monthly_test", "(name, description, teacher_id, live)",
                                  "(\"" + test_name + "\", '{\"description\": \"" + description + "\"}', " + teacher_id + ", \"0\")")
            return HttpResponse(test_id, status=200)
        else:
            return HttpResponse("Un-authenticated user!", status=403)

    # put questions
    def put(self, request, teacher_id):
        test_id = request.headers['testid']
        data = bodyParser(request)
        question = data['question']
        choices = data['choices']
        choice_count = data['choice_count']
        correct_choice = data['correct_choice']
        max_marks = data['max_marks']
        self.insert("monthly_question", "(test_id, question, choice_count, choices, correct, max_marks)",
                    "(\"" + str(test_id) + "\", '{\"question\": \"" + str(question) + "\"}', " + str(choice_count) + ", '{\"choices\": " + str(choices) + "}' , " + str(correct_choice) + ", \"" + str(max_marks) + "\")")
        return HttpResponse("done", status=200)


class SubmitDailyTest(Baseview, View):

    # submit the test
    def post(self, request):
        data = bodyParser(request)
        token = request.headers['token']
        test_id = data['test_id']
        if self.retrieve("*", "teacher", "(token = \"" + token + "\")"):
            return HttpResponse(self.update("date_time = now(), live = 1", "daily_test", "(id = \"" + test_id + "\")"), status=200)
        else:
            return HttpResponse("Un-authenticated user!", status=403)


class SubmitWeeklyTest(Baseview, View):

    # submit the test
    def post(self, request):
        data = bodyParser(request)
        token = request.headers['token']
        test_id = data['test_id']
        if self.retrieve("*", "teacher", "(token = \"" + token + "\")"):
            return HttpResponse(self.update("date_time = now(), live = 1", "weekly_test", "(id = \"" + test_id + "\")"), status=200)
        else:
            return HttpResponse("Un-authenticated user!", status=403)


class SubmitMonthlyTest(Baseview, View):

    # submit the test
    def post(self, request):
        data = bodyParser(request)
        token = request.headers['token']
        test_id = data['test_id']
        if self.retrieve("*", "teacher", "(token = \"" + token + "\")"):
            return HttpResponse(self.update("date_time = now(), live = 1", "monthly_test", "(id = \"" + test_id + "\")"), status=200)
        else:
            return HttpResponse("Un-authenticated user!", status=403)


class GeneralPost(Baseview, View):

    # check existence of doc
    def get(self, request, filename):
        token = request.headers['token']
        file_name = filename
        if self.retrieve("*", "teacher", "(token = \"" + token + "\")"):
            file = self.retrieve("*", "general_doc", "(name = \"" + file_name + "\")")
            if file:
                return HttpResponse("File already exists!!", status=403)
            else:
                return HttpResponse("Success!!", status=200)
        else:
            return HttpResponse("Un-authenticated user!", status=405)

    # post a general post
    def post(self, request, filename):
        data = bodyParser(request)
        token = data['token']
        teacher_id = data['teacher_id']
        img_urls = data['img_urls']
        doc_url = data['doc_url']
        message = data['message']
        if self.retrieve("*", "teacher", "(token = \"" + token + "\")"):
            return self.insert("general_post", "(teacher_id, img_urls, doc_url, message, date_time)", "(\"" + str(teacher_id) + "\", '{\"img_urls\": \"" + img_urls + "\"}', '{\"doc_url\": \"" + doc_url + "\"}', '{\"message\": \"" + message + "\"}', now())")
        else:
            return HttpResponse("Un-authenticated user!", status=403)

    # save a doc name
    def put(self, request, filename):
        token = request.headers['token']
        if self.retrieve("*", "teacher", "(token = \"" + token + "\")"):
            return self.insert("general_doc", "(name)", "(\"" + filename + "\")")
        else:
            return HttpResponse("Un-authenticated user!", status=403)


class MyClasses(Baseview, View):

    # get the list of MyClasses
    def get(self, request):
        token = request.headers['token']
        if self.retrieve("*", "teacher", "(token = \"" + token + "\")"):
            details = self.retrieve("*", "teacher", "(token = \"" + token + "\")")
            class_ids = str(details[0][5])
            class_ids = json.loads(class_ids)
            class_ids = class_ids['class_ids']
            class_ids = class_ids.split(",")
            print("idddd "+str(class_ids))
            class_names = []
            for i in class_ids:
                class_names.append(self.retrieve("name", "class", "(id = \"" + str(i) + "\")")[0][0])
            print("nammme"+str(class_names))
            result = {"class_ids": class_ids, "class_names": class_names}
            return JsonResponse(result, status=200)
        else:
            return HttpResponse("un-authenticated", status=403)


class SubjectList(View, Baseview, Tables):

    # get the list of subjects
    def get(self, request):
        token = request.headers['token']
        res = self.retrieve("subjects_ids", "teacher", "(token = \"" + token + "\")")
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


class ClassContents(Baseview, View):

    # adds a content
    def post(self, request, filename, class_id, subject_id):
        data = bodyParser(request)
        token = data['token']
        subject_id = data['subject_id']
        class_id = data['class_id']
        doc_url = data['doc_url']
        message = data['message']
        teacher = self.retrieve("*", "teacher", "(token = \"" + token + "\")")
        teacher_id = teacher[0][0]
        if teacher:
            return self.insert("class_content", "(teacher_id, class_id, doc_url, message, date_time, subject_id)", "(\"" + str(
                teacher_id) + "\",\"" + class_id + "\", '{\"doc_url\": \"" + doc_url + "\"}', '{\"message\": \"" + message + "\"}', now(), \"" + subject_id + "\")")
        else:
            return HttpResponse("un-authenticated", status=403)

    # check existence of doc
    def get(self, request, filename, class_id, subject_id):
        token = request.headers['token']
        if self.retrieve("*", "teacher", "(token = \"" + token + "\")"):
            file = self.retrieve("*", "class_doc", "(name = \"" + filename + "\" AND class_id = \""+ class_id + "\" AND subject_id = \"" + subject_id + "\")")
            if file:
                return HttpResponse("File already exists!!", status=403)
            else:
                return HttpResponse("Success!!", status=200)
        else:
            return HttpResponse("Un-authenticated user!", status=405)

    # save a doc name
    def put(self, request, filename, class_id, subject_id):
        token = request.headers['token']
        if self.retrieve("*", "teacher", "(token = \"" + token + "\")"):
            return self.insert("class_doc", "(name, class_id, subject_id)", "(\"" + filename + "\", \""+ class_id + "\", \"" + subject_id + "\")")
        else:
            return HttpResponse("Un-authenticated user!", status=403)


class MCQTest(Baseview, View):

    # start a test
    def post(self, request):
        data = bodyParser(request)
        token = data['token']
        test_name = data['test_name']
        class_id = data['class_id']
        subject_id = data['subject_id']
        teacher = self.retrieve("*", "teacher", "(token = \"" + token + "\")")
        if teacher:
            teacher_id = teacher[0][0]
            return self.insert("test", "(name, teacher_id, class_id, subject_id, question_ids, live)", "(\"" + str(test_name) + "\", \"" + str(teacher_id) + "\", \"" + str(class_id) + "\", \"" + str(subject_id) + "\", '{\"question_ids\": \"\"}', \"0\")")
        else:
            return HttpResponse("un-authenticated user", status=403)

    # put questions to test
    def put(self, request):
        data = bodyParser(request)
        question = data['question']
        choice_count = data['choice_count']
        choices = data['choices']
        test_id = data['test_id']
        correct_choice = data['correct_choice']
        marks = data['marks']
        reasoning = data['reasoning']
        question_id = self.insert("mcq_question", "(question, choice_count, marks, reasoning, choice_ids)", "('{\"question\": \"" + question + "\"}', \"" + str(choice_count) + "\", \"" + str(marks) + "\", \"" + str(reasoning) + "\", '{\"choice_ids\": \"\"}')")
        question_id = str(question_id.getvalue())
        question_id = question_id.split("'")
        question_id = question_id[1]
        self.json_update("test", "question_ids", str(question_id), "(id = \"" + test_id + "\")")
        for i in range(0, choice_count):
            if i == correct_choice:
                ans = 1
            else:
                ans = 0
            choice = choices[str(i)]
            choice_id = self.insert("mcq_choice", "(choice, correct, question_id)", "('{\"choice\": \"" + choice + "\"}', \"" + str(ans) + "\", \"" + str(question_id) + "\")")
            choice_id = str(choice_id.getvalue())
            choice_id = choice_id.split("'")
            choice_id = choice_id[1]
            self.json_update("mcq_question", "choice_ids", str(choice_id), "(id=" + str(question_id) + ")")
        return HttpResponse("added", status=200)


class MakeLive(Baseview, View):

    # make mcq test live
    def post(self, request):
        data = bodyParser(request)
        test_id = data['test_id']
        return HttpResponse(self.update("live = \"1\"", "test", "(id = \"" + str(test_id) + "\")"), status=200)

