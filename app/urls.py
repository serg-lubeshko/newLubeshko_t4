from django.urls import path

from app.views.course_view import CourseList, DetailCourse, AddTeacher, AddStudent
from app.views.person_view import UserRegister

urlpatterns = [

    path('create-person/', UserRegister.as_view()),

    path('course/all', CourseList.as_view()),
    path('course/detail/<int:pk>', DetailCourse.as_view()),
    path('course/add-professor/<int:course_id>', AddTeacher.as_view()),
    path('course/add-student/<int:course_id>', AddStudent.as_view()),

]