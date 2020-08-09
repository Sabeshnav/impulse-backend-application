from django.urls import path
from .views import Mentor, Student, Teacher, ClassRoom, ClassStudentList, ClassTeacherList, Subject, Category, TeacherSubjectList, GetAllTeacher, AddTeacherClass
urlpatterns = [
    path('mentor/', Mentor.as_view()),
    path('student/<username>', Student.as_view()),
    path('teacher/<teacher_id>', Teacher.as_view()),
    path('teacher/add/', AddTeacherClass.as_view()),
    path('class/<class_id>', ClassRoom.as_view()),
    path('student/list/', ClassStudentList.as_view()),
    path('teacher/list/', ClassTeacherList.as_view()),
    path('subject/', Subject.as_view()),
    path('category', Category.as_view()),
    path('subject/list/', TeacherSubjectList.as_view()),
    path('getall/teacher/', GetAllTeacher.as_view())
]
