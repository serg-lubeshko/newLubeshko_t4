from django.urls import path

from app.views.course_view import CourseList, DetailCourse, AddTeacher, AddStudent
from app.views.homework_view import HomeworkToLecture
from app.views.lecture_view import LectureToCourse, LectureRUD, LectureList
from app.views.mark_message_view import ProfessorWatchHomework, ProfessorMarkDetail, StudentLookHisSolution
from app.views.person_view import UserRegister, ListPerson
from app.views.solution_view import SolutionToHomework

urlpatterns = [
    #Для удобства Login и Logout использовал Джанговский
    path('a-create-person/', UserRegister.as_view()),
    path('a-list-person/', ListPerson.as_view()),

    path('b-course-watch-and-add/all', CourseList.as_view()),
    path('b-course/detail/<int:pk>', DetailCourse.as_view()),
    path('b-course/add-professor/<int:course_id>', AddTeacher.as_view()),
    path('b-course/add_del-student/<int:course_id>', AddStudent.as_view()),

    path('bc-lecture-list/', LectureList.as_view()),
    path('c-lecture-add/<int:course_id>', LectureToCourse.as_view()),
    path('c-lecture-rud/<int:id>', LectureRUD.as_view()),

    path('d-add-homework/', HomeworkToLecture.as_view()),

    path('e-student-watch-task-and-add-solution/', SolutionToHomework.as_view()),

    path('professor-watch-homework-add-mark-message/', ProfessorWatchHomework.as_view()),
    path('professor-update-mark/<int:solution_id>', ProfessorMarkDetail.as_view()),
    # path('professor-update-mark/<int:solution_id>', ProfessorChangeMark.as_view()),

    path('student-look-check-solutions/', StudentLookHisSolution.as_view()),
    # path('student-look-check-chatted/<int:solution_id>', StudentLookHisSolution.as_view()),

]
