from django.http import HttpResponse, JsonResponse
from baseview import Baseview, bodyParser, jsonLoader
from django.views import View
import smtplib
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
        print(details)
        if details:
            if password == str(details[0][3]):
                return HttpResponse(str(details[0][7]), status=200)
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
        category = request.headers['category']
        file_name = filename
        if self.retrieve("*", "teacher", "(token = \"" + token + "\")"):
            file = self.retrieve("*", "general_doc", "(name = \"" + file_name + "\" AND category = " + str(category) + ")")
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
        category = data['category']
        if self.retrieve("*", "teacher", "(token = \"" + token + "\")"):
            return self.insert("general_post", "(teacher_id, img_urls, doc_url, message, date_time, category)", "(\"" + str(teacher_id) + "\", '{\"img_urls\": \"" + img_urls + "\"}', '{\"doc_url\": \"" + doc_url + "\"}', '{\"message\": \"" + message + "\"}', now(), \"  " + str(category) + " \")")
        else:
            return HttpResponse("Un-authenticated user!", status=403)

    # save a doc name
    def put(self, request, filename):
        token = request.headers['token']
        category = request.headers['category']
        if self.retrieve("*", "teacher", "(token = \"" + token + "\")"):
            return self.insert("general_doc", "(name, category)", "(\"" + filename + "\", \"  " + str(category) + " \")")
        else:
            return HttpResponse("Un-authenticated user!", status=403)

    # get posts
    def get(self, request, filename):
        token = request.headers['token']
        messages = []
        img_urls = []
        doc_url = []
        date_times = []
        modes = []
        if self.retrieve("*", "teacher", "(token = \"" + token + "\")"):
            content = self.retrieve_all("general_post ORDER BY id DESC")
            for i in content:
                o = {}
                o = json.loads(str(i[5]))
                print(o)
                o = str(o["message"])
                messages.append(o)
                o = i[3]
                o = json.loads(str(i[3]))
                check_img = o["img_urls"]
                img_urls.append(check_img)
                o = i[4]
                o = json.loads(str(i[4]))
                doc_url.append(o["doc_url"])
                check_doc = o["doc_url"]
                date_times.append(str(i[2]))
                if check_img == "" and check_doc == "":
                    modes.append(0)
                else:
                    if check_img == "" and not check_doc == "":
                        modes.append(2)
                    if check_doc == "" and not check_img == "":
                        modes.append(1)
                    if not check_doc == "" and not check_img == "":
                        modes.append(3)
            result = {"messages": messages, "img_urls": img_urls, "doc_urls": doc_url, "date_times": date_times, "modes": modes}
            return JsonResponse(result, status=200)
        else:
            return HttpResponse("un-authenticated", status=403)


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
                teacher_id) + "\",\"" + class_id + "\", '{\"doc_url\": \"" + doc_url + "\"}', '{\"message\": \"" + message + "\"}', now(), 0)")
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
        print(request.body)
        data = bodyParser(request)

        question = data['question']
        choice_count = data['choice_count']
        negative_marks = data['negative_marks']
        choices = data['choices']
        choices = str(choices)
        choices = choices.replace("[", "")
        choices = choices.replace("]", "")
        choices = choices.split(",")
        test_id = data['test_id']
        correct_choice = data['correct_choice']
        marks = data['marks']
        reasoning = data['reasoning']
        question_id = self.insert("mcq_question", "(question, choice_count, marks, reasoning, choice_ids, negative_marks)", "('{\"question\": \"" + question + "\"}', \"" + str(choice_count) + "\", \"" + str(marks) + "\", \"" + str(reasoning) + "\", '{\"choice_ids\": \"\"}', \"" + str(negative_marks) +"\")")
        question_id = str(question_id.getvalue())
        question_id = question_id.split("'")
        question_id = question_id[1]
        self.json_update("test", "question_ids", str(question_id), "(id = \"" + test_id + "\")")
        print("baga")
        for i in range(0, 4):
            if i == 0:
                ans = 1
            else:
                ans = 0
            choice = choices[i]
            choice_id = self.insert("mcq_choice", "(choice, correct, question_id)", "('{\"choice\": \"" + choice + "\"}', \"" + str(ans) + "\", \"" + str(question_id) + "\")")
            choice_id = str(choice_id.getvalue())
            choice_id = choice_id.split("'")
            choice_id = choice_id[1]
            self.json_update("mcq_question", "choice_ids", str(choice_id), "(id=" + str(question_id) + ")")
        return HttpResponse("added", status=200)

    # get a test details
    def get(self, request):
        test_id = request.headers['testid']
        data = self.retrieve("*", "test", "(id=\"" + str(test_id) + "\")")
        print(str(data[0]))
        if data:
            data = data[0]
            question_ids = data[5]
            question_ids = json.loads(str(question_ids))
            res = {"id": data[0], "name": data[1], "question_ids": str(question_ids['question_ids'])}
            return JsonResponse(res, status=200)
        else:
            return HttpResponse("Test doesn't exist!", status=403)


class MCQQuestion(Baseview, View):

    # get a question
    def get(self, request):
        question_id = request.headers['qid']
        data = self.retrieve("*", "mcq_question", "(id=\"" + str(question_id) + "\")")
        print(str(data[0]))
        if data:
            data = data[0]
            question = data[1]
            question = json.loads(str(question))
            choice_ids = data[3]
            choice_ids = json.loads(str(choice_ids))
            marks = data[4]
            negative_marks = data[6]
            marks = str(marks)
            negative_marks = str(negative_marks)
            bad_char = ['D','e','c','i','m','a','l','(','\'',')']
            for i in bad_char:
                marks.replace(i, '')
            res = {"id": data[0], "question": str(question['question']), "choice_count" : data[2], "choice_ids" : str(choice_ids['choice_ids']), "marks" : marks, "reasoning" : str(data[5]), "negative_marks" : negative_marks}
            print(str(res))
            return JsonResponse(res, status=200)
        else:
            return HttpResponse("Question doesn't exist!", status=403)

    # edit a question
    def post(self, request):
        data = bodyParser(request)
        choice_edited = data['choice_edited']
        if choice_edited == 0:
            question_id = data['question_id']
            question = data['question']
            marks = data['marks']
            reasoning = data['reasoning']
            test_id = data['test_id']
            negative_marks = data['negative_marks']
            print("question : "+question)
            print("marks : " + str(marks))
            print("reasoning : " + str(reasoning))
            print("negative_marks : " + str(negative_marks))
            print("question id : " + str(question_id))
            self.json_edit("mcq_question", "question", str(question), "(id=" + str(question_id) + ")")
            return HttpResponse(self.update("marks = \"" + str(marks) + "\",  negative_marks = \"" + str(negative_marks) + "\",  reasoning = \"" + str(reasoning) + "\"", "mcq_question", "(id = \"" + str(question_id) + "\")"))
        if choice_edited == 1:
            data = bodyParser(request)
            question = data['question']
            choice_count = data['choice_count']
            negative_marks = data['negative_marks']
            choices = data['choices']
            question_id = data['question_id']
            test_id = data['test_id']
            correct_choice = data['correct_choice']
            marks = data['marks']
            reasoning = data['reasoning']
            self.json_edit("mcq_question", "choice_ids", "", "(id=" + str(question_id) + ")")
            self.json_edit("mcq_question", "question", str(question), "(id=" + str(question_id) + ")")
            for i in range(0, choice_count):
                if i == correct_choice:
                    ans = 1
                else:
                     ans = 0
                choice = choices[str(i)]
                choice_id = self.insert("mcq_choice", "(choice, correct, question_id)",
                                        "('{\"choice\": \"" + choice + "\"}', \"" + str(ans) + "\", \"" + str(
                                            question_id) + "\")")
                choice_id = str(choice_id.getvalue())
                choice_id = choice_id.split("'")
                choice_id = choice_id[1]
                self.json_update("mcq_question", "choice_ids", str(choice_id), "(id=" + str(question_id) + ")")
            return HttpResponse(self.update("marks = \"" + str(marks) + "\",  negative_marks = \"" + str(negative_marks) + "\",  reasoning = \"" + str(reasoning) + "\"", "mcq_question", "(id = \"" + str(question_id) + "\")"))


class Choice(Baseview, View):

    # get a choice
    def get(self, request):
        choice_id = request.headers['cid']
        data = self.retrieve("*", "mcq_choice", "(id=\"" + str(choice_id) + "\")")
        print(str(data[0]))
        if data:
            data = data[0]
            choice = data[1]
            choice = json.loads(str(choice))
            res = {"id": data[0], "choice": str(choice['choice']), "correct": data[2], "question_id": data[3]}
            print(str(res))
            return JsonResponse(res, status=200)
        else:
            return HttpResponse("Choice doesn't exist!", status=403)


class MakeLive(Baseview, View):

    # make mcq test live
    def post(self, request):
        data = bodyParser(request)
        test_id = data['test_id']
        # test_duration = data['test_duration']
        # self.update("time = \"" + str(test_duration) + "\"", "test", "(id = \"" + str(test_id) + "\")")
        return HttpResponse(self.update("live = \"1\"", "test", "(id = \"" + str(test_id) + "\")"), status=200)


class TakeDown(Baseview, View):

    # take down an mcq test live
    def post(self, request):
        data = bodyParser(request)
        test_id = data['test_id']
        return HttpResponse(self.update("live = \"0\"", "test", "(id = \"" + str(test_id) + "\")"), status=200)


class MyTests(Baseview, View):

    # get the list of MyTests
    def get(self, request):
        token = request.headers['token']
        class_id = request.headers['classid']
        # subject_id = request.headers['subjectid']
        ids = []
        names = []
        question_ids = []
        lives = []
        class_ids = []
        subject_ids = []
        if self.retrieve("*", "teacher", "(token = \"" + token + "\")"):
            details = self.retrieve("*", "teacher", "(token = \"" + token + "\")")
            teacher_id = details[0][0]
            test_details = self.retrieve("*", "test", "(class_id = \""+ class_id + "\")")
            test_details = test_details
            for i in test_details:
                ids.append(str(i[0]))
                names.append(str(i[1]))
                o = i[5]
                o = json.loads(o)
                o = o["question_ids"]
                question_ids.append(o)
                lives.append(str(i[6]))
            print(ids)
            print(names)
            print(question_ids)
            print(lives)
            result = {"test_ids": ids, "names": names, "question_ids": question_ids, "lives": lives}
            return JsonResponse(result, status=200)
        else:
            return HttpResponse("un authenticated user", status=403)

    # delete a test
    def post(self, request):
        data = bodyParser(request)
        test_id = data['test_id']
        return HttpResponse(self.delete_row("test", "(id = \"" + test_id + "\")"), status=200)


class FeedMyClassContentInitial(Baseview, View):

    # get initial feed
    def get(self, request):
        print("awkward")
        token = request.headers['token']
        class_id = request.headers['classid']
        ids = []
        messages = []
        urls = []
        date_times = []
        if self.retrieve("*", "teacher", "(token = \"" + token + "\")"):
            contents = self.retrieve("*", "class_content", "(class_id = \"" + class_id + "\") ORDER BY id DESC")
            for i in contents:
                ids.append(str(i[0]))
                o = i[4]
                o = json.loads(o)
                o = o["message"]
                messages.append(o)
                o = i[3]
                o = json.loads(o)
                o = o["doc_url"]
                urls.append(o)
                date_times.append(str(i[5]))
            print("ids" + str(ids) + "messages" + str(messages) + "urls" + str(urls) + "date_times" + str(date_times))
            result = {"ids": ids, "messages": messages, "urls": urls, "date_times": date_times}
            return JsonResponse(result, status=200)
        else:
            return HttpResponse("Choice doesn't exist!", status=403)


class FeedMyClassContentAppend(Baseview, View):

    # get initial feed
    def get(self, request):
        token = request.headers['token']
        last_id = request.headers['lastid']
        class_id = request.headers['classid']
        subject_id = request.headers['subjectid']
        ids = []
        messages = []
        urls = []
        date_times = []
        if self.retrieve("*", "teacher", "(token = \"" + token + "\")"):
            details = self.retrieve("*", "teacher", "(token = \"" + token + "\")")
            teacher_id = details[0][0]
            contents = self.retrieve("*", "class_content", "(teacher_id = \"" + str(
                teacher_id) + "\" AND class_id = \"" + class_id + "\" AND subject_id = \"" + subject_id + "\" AND id < \"" + last_id + "\") ORDER BY id DESC")
            for i in contents:
                ids.append(str(i[0]))
                o = i[4]
                o = json.loads(o)
                o = o["message"]
                messages.append(o)
                o = i[3]
                o = json.loads(o)
                o = o["doc_url"]
                urls.append(o)
                date_times.append(str(i[2]))
            print("ids" + str(ids) + "messages" + str(messages) + "urls" + str(urls) + "date_times" + str(date_times))
            result = {"ids": ids, "messages": messages, "urls": urls, "date_times": date_times}
            return JsonResponse(result, status=200)
        else:
            return HttpResponse("Choice doesn't exist!", status=403)


class SubjectiveTest(Baseview, View):

    # start a test
    def post(self, request, filename, class_id, subject_id):
        data = bodyParser(request)
        token = data['token']
        test_name = data['test_name']
        class_id = data['class_id']
        subject_id = data['subject_id']
        teacher = self.retrieve("*", "teacher", "(token = \"" + token + "\")")
        if teacher:
            teacher_id = teacher[0][0]
            return self.insert("subjective_test", "(name, teacher_id, class_id, subject_id, doc_url, live, message)",
                               "(\"" + str(test_name) + "\", \"" + str(teacher_id) + "\", \"" + str(
                                   class_id) + "\", \"" + str(subject_id) + "\", '{\"doc_url\": \"\"}', \"0\", '{\"message\": \"\"}')")
        else:
            return HttpResponse("un-authenticated user", status=403)

    # check existence of doc
    def get(self, request, filename, class_id, subject_id):
        token = request.headers['token']
        file_name = filename
        if self.retrieve("*", "teacher", "(token = \"" + token + "\")"):
            file = self.retrieve("*", "subjective_doc", "(name = \"" + file_name + "\")")
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
            return self.insert("subjective_doc", "(name, class_id, subject_id)", "(\"" + filename + "\", \""+ class_id + "\", \"" + subject_id + "\")")
        else:
            return HttpResponse("Un-authenticated user!", status=403)


class SubjectivePost(Baseview, View):

    # adds a content
    def post(self, request, filename, class_id, subject_id):
        data = bodyParser(request)
        token = data['token']
        test_id = data['test_id']
        subject_id = data['subject_id']
        class_id = data['class_id']
        doc_url = data['doc_url']
        message = data['message']
        teacher = self.retrieve("*", "teacher", "(token = \"" + token + "\")")
        teacher_id = teacher[0][0]
        if teacher:
            self.json_update("subjective_test", "message", str(message), "(id=" + str(test_id) + ")")
            self.json_update("subjective_test", "doc_url", str(doc_url), "(id=" + str(test_id) + ")")
            self.update("date_time = now()", "subjective_test", "(id=" + str(test_id) + ")")
            return HttpResponse("done", status=200)
        else:
            return HttpResponse("un-authenticated", status=403)


class MySubjectiveTests(Baseview, View):

    # get the list of My subjective tests
    def get(self, request):
        token = request.headers['token']
        class_id = request.headers['classid']
        subject_id = request.headers['subjectid']
        ids = []
        names = []
        messages = []
        lives = []
        class_ids = []
        subject_ids = []
        if self.retrieve("*", "teacher", "(token = \"" + token + "\")"):
            details = self.retrieve("*", "teacher", "(token = \"" + token + "\")")
            teacher_id = details[0][0]
            test_details = self.retrieve("*", "subjective_test", "(teacher_id = \"" + str(teacher_id) + "\" AND class_id = \""+ class_id + "\" AND subject_id = \""+ subject_id + "\")")
            test_details = test_details
            for i in test_details:
                ids.append(str(i[0]))
                names.append(str(i[1]))
                o = i[8]
                print("tamil"+o)
                o = json.loads(o)
                o = o["message"]
                messages.append(o)
                lives.append(str(i[7]))
            print(ids)
            print(names)
            print(messages)
            print(lives)
            result = {"test_ids": ids, "names": names, "messages": messages, "lives": lives}
            return JsonResponse(result, status=200)
        else:
            return HttpResponse("un authenticated user", status=403)

    # delete a test
    def post(self, request):
        data = bodyParser(request)
        test_id = data['test_id']
        return HttpResponse(self.delete_row("test", "(id = \"" + test_id + "\")"), status=200)


class MakeLiveSubjective(Baseview, View):

    # make subjective test live
    def post(self, request):
        data = bodyParser(request)
        test_id = data['test_id']
        return HttpResponse(self.update("live = \"1\"", "subjective_test", "(id = \"" + str(test_id) + "\")"), status=200)


class TakeDownSubjective(Baseview, View):

    # take down an subjective test live
    def post(self, request):
        data = bodyParser(request)
        test_id = data['test_id']
        return HttpResponse(self.update("live = \"0\"", "subjective_test", "(id = \"" + str(test_id) + "\")"), status=200)


class DeleteSubjectiveTest(Baseview, View):

    # delete a test
    def post(self, request):
        data = bodyParser(request)
        test_id = data['test_id']
        return HttpResponse(self.delete_row("subjective_test", "(id = \"" + test_id + "\")"), status=200)


class SubmissionsMCQ(Baseview, View):

    # get the marks of students in a test
    def get(self, request):
        test_id = request.headers['testid']
        print("test"+test_id)
        marks = self.retrieve("*", "mcq_test_marks", "(test_id = \"" + str(test_id) + "\")")
        student_names = []
        student_ids = []
        scores = []
        for i in marks:
            user_id = i[2]
            user_details = self.retrieve("username", "users", "(id = \"" + str(user_id) + "\")")
            username = str(user_details[0][0])
            mark = str(i[3])
            student_names.append(username)
            student_ids.append(user_id)
            scores.append(str(mark))
        print("         "+str(student_names)+"       "+str(student_ids)+"          "+str(scores))
        result = {"names": student_names, "ids": student_ids, "scores": scores}
        return JsonResponse(result, status=200)


class TeacherDetails(View, Baseview):

    def get(self, request):
        token = request.headers['token']
        res = self.retrieve("*", "teacher", "(token = \"" + token + "\")")
        if res:
            name = res[0][1]
            phone = res[0][2]
            email = res[0][3]
            result = {"name": name, "phone": phone, "email": email}
            return JsonResponse(result, status=200)
        else:
            return HttpResponse("error!!", status=400)
