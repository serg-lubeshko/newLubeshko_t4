from rest_framework import permissions

from app.models import Homework, Lecture, StudCour, TeachCour



class IsProfessorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.status == 'p'

class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user









class IsProffesorOwnerOrReadOnly(permissions.BasePermission):

    def has_object(self, request, view, obj):
        # if request.method in permissions.SAFE_METHODS:
        #     return True
        print(obj, '***********')
        return obj.professor.pk == request.user.pk


class IsRegisteredStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            param = request.parser_context['kwargs'].get('homework_id')
            id_lecture = Homework.objects.get(id=param).lecture_for_homework_id
            id_course = Lecture.objects.get(id=id_lecture).course_id
            user = request.user.pk
            return StudCour.objects.filter(course_id=id_course).filter(student_id=user)
        except Homework.DoesNotExist:
            return False


class IsRegisteredPersonCourse(permissions.BasePermission):
    def has_permission(self, request, view):
        param = request.parser_context['kwargs'].get('course_id')
        status_user = request.user.status
        if status_user in ('s'):
            if request.method in permissions.SAFE_METHODS and StudCour.objects.filter(
                    student_id=request.user.pk).filter(course_id=param):
                return True
        if status_user in ('p',) and TeachCour.objects.filter(teacher_id=request.user.pk).filter(course_id=param):
            return True
        return False


class IsRegisteredPersonHomework(permissions.BasePermission):
    def has_permission(self, request, view):
        param_lecture = request.parser_context['kwargs'].get('lecture_id')
        param = Lecture.objects.get(id=param_lecture).course_id
        status_user = request.user.status
        if status_user in ('s'):
            if request.method in permissions.SAFE_METHODS and StudCour.objects.filter(
                    student_id=request.user.pk).filter(course_id=param):
                return True
        if status_user in ('p',) and TeachCour.objects.filter(teacher_id=request.user.pk).filter(course_id=param):
            return True
        return False


# class IsProfessorOrReadOnlyMark(permissions.BasePermission):
#     def has_permission(self, request, view):
#         print('eddedede')
#         # if request.method in permissions.SAFE_METHODS:
#         #     return True
#         return bool(
#             request.user.status == 'p',
#         )


class IsProfessorOrReadOnlyMark(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.status == 'p'
        try:
            param_solution = request.data['solution_id']
            professor_pk = Homework.objects.get(homework_solution__id=param_solution).professor_id
        except Homework.DoesNotExist:
            return False
        return bool(request.user.status == 'p' and request.user.pk == professor_pk)


class IsProfessorOrReadOnlyMarkDetail(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.status == 'p'
        # param_solution = request.data['solution_id']
        print(request.parser_context['kwargs'])
        try:
            param_solution = request.parser_context['kwargs'].get('solution_id')
            professor_pk = Homework.objects.get(homework_solution__id=param_solution).professor_id
        except Homework.DoesNotExist:
            return False
        return bool(request.user.status == 'p' and request.user.pk == professor_pk)


# class XXXX(permissions.BasePermission):
#
#     def has_object_permission(self, request, view, obj):
#
#         if request.method in permissions.SAFE_METHODS:
#             return True
#
#         return obj.professor.pk == request.user.pk

class IsStudentOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # if request.method in permissions.SAFE_METHODS:
        #     return True
        return request.user.status == 's'
