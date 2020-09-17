from django.urls import path
from .views import MakeLiveSubjective, DeleteSubjectiveTest, TakeDownSubjective, TeacherDetails, DailyTest, WeeklyTest, SubmissionsMCQ, MonthlyTest, SubmitDailyTest, MySubjectiveTests, Login, GeneralPost, TakeDown, SubjectivePost, MyClasses, FeedMyClassContentAppend, SubjectiveTest, FeedMyClassContentInitial, SubjectList, MyTests, ClassContents, Choice, MCQTest, MakeLive, MCQQuestion
urlpatterns = [
    path('test/daily/<teacher_id>', DailyTest.as_view()),
    path('test/weekly/<teacher_id>', WeeklyTest.as_view()),
    path('test/monthly/<teacher_id>', MonthlyTest.as_view()),
    path('test/my/subjective/delete/', DeleteSubjectiveTest.as_view()),
    path('test/daily/submit/', SubmitDailyTest.as_view()),
    path('login/', Login.as_view()),
    path('gen_post/<filename>', GeneralPost.as_view()),
    path('my_classes/', MyClasses.as_view()),
    path('my_subjects/', SubjectList.as_view()),
    path('content/post/<filename>/<class_id>/<subject_id>', ClassContents.as_view()),
    path('test/', MCQTest.as_view()),
    path('make/live/', MakeLive.as_view()),
    path('take/down/', TakeDown.as_view()),
    path('make/live/subjective/', MakeLiveSubjective.as_view()),
    path('take/down/subjective/', TakeDownSubjective.as_view()),
    path('test/question/', MCQQuestion.as_view()),
    path('test/choice/', Choice.as_view()),
    path('test/my/', MyTests.as_view()),
    path('feed/class/content/initial/', FeedMyClassContentInitial.as_view()),
    path('feed/class/content/append/', FeedMyClassContentAppend.as_view()),
    path('test/subjective/<filename>/<class_id>/<subject_id>', SubjectiveTest.as_view()),
    path('subjective_post/<filename>/<class_id>/<subject_id>', SubjectivePost.as_view()),
    path('test/subjective/feed/', MySubjectiveTests.as_view()),
    path('marks/mcq/', SubmissionsMCQ.as_view()),
    path('details/', TeacherDetails.as_view())
]
