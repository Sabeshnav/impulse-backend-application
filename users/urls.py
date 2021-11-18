from django.urls import path
from .views import UserDetails, Signup, GeneralPosts, EnterClasroom, FeedMyClassContentInitial, MyTests, MySubjectiveTests, MCQTestAttend, MyMarks, MySubjectiveSubmission
urlpatterns = [
    path('enter/class/', EnterClasroom.as_view()),
    path('signup/', Signup.as_view()),
    path('gen_post/<category>', GeneralPosts.as_view()),
    path('<user_id>/get/', UserDetails.as_view()),
    path('class/content/', FeedMyClassContentInitial.as_view()),
    path('class/test/mcq/', MyTests.as_view()),
    path('class/test/subjective/', MySubjectiveTests.as_view()),
    path('test/attend/mcq/', MCQTestAttend.as_view()),
    path('test/my/marks/', MyMarks.as_view()),
    path('test/attend/subjective/<filename>/<test_id>/', MySubjectiveSubmission.as_view())
]
