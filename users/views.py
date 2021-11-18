from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.http import HttpResponse, JsonResponse
from baseview import Baseview, bodyParser, jsonLoader
from django.views import View
from tableDetails import Tables
import json
from django.contrib.auth.models import User

table = "users"


class EnterClasroom(Baseview, View):

    # enter a classroom
    def post(self, request):
        data = bodyParser(request)
        password = data["password"]
        user_id = data["user_id"]
        class_id = data['class_id']
        ud = self.retrieve("*", "users", "(id=\""+ str(user_id) +"\")")
        if str(class_id) == str(ud[0][3]) and str(password) == str(ud[0][4]):
            return HttpResponse(str(ud[0][5]), status=200)
        else:
            if str(password) != str(ud[0][4]) and str(class_id) == str(ud[0][3]):
                return HttpResponse("incorrect", status=401)
            else:
                return HttpResponse("error", status=400)


class Signup(View, Baseview, Tables):

    def post(self, request):
        data = bodyParser(request)
        username = data["username"]
        email = data["email"]
        if self.retrieve("username", "users", "(username=\""+username+"\")"):
            return HttpResponse("OOPS!! Username already taken!!", status=400)
        else:
            return HttpResponse(self.insert("users", "(username, email)", "(\""+username+"\", \""+email+"\")"), status=200)


class UserDetails(View, Baseview, Tables):

    def get(self, request, user_id):
        res = self.retrieve("*", table, "(id=" + user_id + ")")
        if res:
            class_id = res[0][3]
            if class_id is not None:
                class_details = self.retrieve("*", "class", "(id=" + str(class_id) + ")")
                class_name = class_details[0][1]
                field = ["username", "email", "class_id", "class_name"]
                value = [res[0][1], res[0][2], class_id, class_name]
                print(value)
                res = jsonLoader(field, value)
                return JsonResponse(res, status=200)
            else:
                field = ["username", "email"]
                value = [res[0][1], res[0][2]]
                print(value)
                res = jsonLoader(field, value)
                return JsonResponse(res, status=201)
        else:
            return HttpResponse("error!!", status=400)


class GeneralPosts(View, Baseview):

    # get posts
    def get(self, request, category):
        messages = []
        img_urls = []
        doc_url = []
        date_times = []
        modes = []
        content = self.retrieve_all("general_post WHERE (category = " + str(category) + ")ORDER BY id DESC")
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
        result = {"messages": messages, "img_urls": img_urls, "doc_urls": doc_url, "date_times": date_times,
                  "modes": modes}
        return JsonResponse(result, status=200)


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
        if self.retrieve("*", "users", "(token = \"" + token + "\")"):
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
        if self.retrieve("*", "users", "(token = \"" + token + "\")"):
            test_details = self.retrieve("*", "test", "(class_id = \""+ class_id + "\" AND live = 1)")
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


class MySubjectiveTests(Baseview, View):

    # get the list of My subjective tests
    def get(self, request):
        token = request.headers['token']
        class_id = request.headers['classid']
        ids = []
        names = []
        messages = []
        lives = []
        doc_urls = []
        if self.retrieve("*", "users", "(token = \"" + token + "\")"):
            details = self.retrieve("*", "users", "(token = \"" + token + "\")")
            test_details = self.retrieve("*", "subjective_test", "(class_id = \""+ class_id + "\" AND live = 1)")
            test_details = test_details
            for i in test_details:
                ids.append(str(i[0]))
                names.append(str(i[1]))
                o = i[8]
                print("tamil"+o)
                o = json.loads(o)
                o = o["message"]
                messages.append(o)
                o = i[5]
                print("engg" + o)
                o = json.loads(o)
                o = o["doc_url"]
                doc_urls.append(o)
                lives.append(str(i[7]))
            print(ids)
            print(names)
            print(messages)
            print(lives)
            print(doc_urls)
            result = {"test_ids": ids, "names": names, "messages": messages, "lives": lives, "doc_urls": doc_urls}
            return JsonResponse(result, status=200)
        else:
            return HttpResponse("un authenticated user", status=403)


class MCQTestAttend(Baseview, View):

    # attend an mcq test
    def get(self, request):
        result = {}
        test_id = request.headers['testid']
        test_details = self.retrieve("*", "test", "(id = \"" + test_id + "\")")
        test_name = str(test_details[0][1])
        question_ids = test_details[0][5]
        question_ids = json.loads(question_ids)
        question_ids = str(question_ids["question_ids"])
        question_ids = list(question_ids.split(","))
        qNumber = 0
        for i in question_ids:
            res = {}
            qNumber = qNumber + 1
            question_id = i
            data = self.retrieve("*", "mcq_question", "(id=\"" + str(question_id) + "\")")
            print(str(data[0]))
            if data:
                data = data[0]
                question = data[4]
                question = json.loads(str(question))
                choice_ids = data[6]
                choice_ids = json.loads(str(choice_ids))
                marks = data[3]
                negative_marks = data[7]
                marks = str(marks)
                negative_marks = str(negative_marks)
                bad_char = ['D', 'e', 'c', 'i', 'm', 'a', 'l', '(', '\'', ')']
                for i in bad_char:
                    marks.replace(i, '')
                choice_ids = str(choice_ids['choice_ids'])
                choice_ids = list(choice_ids.split(","))
                c_number = 1
                print("choiceeee", choice_ids)
                for i in choice_ids:
                    c_name = "c" + str(c_number)
                    v_name = "v"+ str(c_number)
                    c_data = self.retrieve("*", "mcq_choice", "(id=\"" + str(i) + "\")")
                    print(str(c_data[0]))
                    c_data = c_data[0]
                    choice = c_data[1]
                    choice = json.loads(str(choice))
                    res[c_name] = str(choice['choice'])
                    res[v_name] = str(c_data[2])
                    c_number = c_number + 1
                print("original", str(res))
                res.update({"id": data[0], "question": str(question['question']), "choice_count": data[2], "marks": marks, "reasoning": str(data[5]), "negative_marks": negative_marks, "question_number" : str(qNumber)})
                print("duplicate", str(res))
                qn = "q"+str(qNumber)
                result[str(qn)] = res
        result['numbers'] = qNumber
        print(str(result))
        return JsonResponse(result, status=200)


class MyMarks(Baseview, View):

    # put a test's mark
    def post(self, request):
        data = bodyParser(request)
        user_id = data["user_id"]
        test_id = data["test_id"]
        marks = data['marks']
        self.insert("mcq_test_marks", "(test_id, user_id, marks)", "(\"" + test_id + "\", \""+ user_id + "\", \"" + marks + "\")")
        return HttpResponse("done", status=200)

    # get all test marks of a student
    def get(self, request):
        user_id = request.headers["userid"]
        data = self.retrieve("*", "mcq_test_marks", "(user_id=\"" + str(user_id) + "\")")
        data = data
        print("unicorn")
        print(str(data))
        marks = []
        names = []
        result = {}
        for i in data:
            test_details = self.retrieve("name", "test", "(id=\"" + str(i[1]) + "\")")
            names.append(str(test_details[0]))
            marks.append(i[3])
        result["names"] = names
        result["marks"] = marks
        return JsonResponse(result, status=200)


class MySubjectiveSubmission(Baseview, View):

    # check existence of doc
    def get(self, request, filename, test_id):
        token = request.headers['token']
        test_id = request.headers['testid']
        user_details = self.retrieve("*", "users", "(token = \"" + token + "\")")
        if user_details:
            class_id = user_details[0][3]
            file = self.retrieve("*", "subjective_test_submission_doc", "(name = \"" + filename + "\" AND class_id = \""+ class_id + "\" AND test_id = \"" + test_id + "\")")
            if file:
                return HttpResponse("File already exists!!", status=403)
            else:
                return HttpResponse("Success!!", status=200)
        else:
            return HttpResponse("Un-authenticated user!", status=405)

    # save a doc name
    def put(self, request, filename, test_id):
        token = request.headers['token']
        user_details = self.retrieve("*", "users", "(token = \"" + token + "\")")
        if user_details:
            class_id = user_details[0][3]
            return self.insert("subjective_test_submission_doc", "(name, class_id, test_id)", "(\"" + filename + "\", \""+ class_id + "\", \"" + test_id + "\")")
        else:
            return HttpResponse("Un-authenticated user!", status=403)

    # adds a content
    def post(self, request, filename, test_id):
        data = bodyParser(request)
        token = data['token']
        test_id = data['test_id']
        doc_url = data['doc_url']
        user_details = self.retrieve("*", "users", "(token = \"" + token + "\")")
        user_id = user_details[0][0]
        if user_details:
            return self.insert("subjective_submission", "(user_id, test_id, doc_url)", "(\"" + str(
                user_id) + "\",\"" + test_id + "\", '{\"doc_url\": \"" + doc_url + "\"}')")
        else:
            return HttpResponse("un-authenticated", status=403)
