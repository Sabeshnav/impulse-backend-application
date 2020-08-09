from django.urls import path
from .views import DailyTest, WeeklyTest, MonthlyTest, SubmitDailyTest, Login, GeneralPost, MyClasses, SubjectList, ClassContents, MCQTest, MakeLive
urlpatterns = [
    path('test/daily/<teacher_id>', DailyTest.as_view()),
    path('test/weekly/<teacher_id>', WeeklyTest.as_view()),
    path('test/monthly/<teacher_id>', MonthlyTest.as_view()),
    path('test/daily/submit/', SubmitDailyTest.as_view()),
    path('login/', Login.as_view()),
    path('gen_post/<filename>', GeneralPost.as_view()),
    path('my_classes/', MyClasses.as_view()),
    path('my_subjects/', SubjectList.as_view()),
    path('content/post/<filename>/<class_id>/<subject_id>', ClassContents.as_view()),
    path('test/', MCQTest.as_view()),
    path('make/live/', MakeLive.as_view())
]
