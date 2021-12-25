from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, generics
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from app.conf.permission import IsRegisteredPersonCourse, IsProffesorToLecture
from app.models import Course, Lecture
from app.serializers.serializers_lecture import LectureSerializer, CourseLectureSerializer


class LectureList(generics.ListAPIView):
    """  Список курса с лекциями """

    permission_classes = [IsAuthenticated]
    serializer_class = CourseLectureSerializer
    queryset = Course.objects.all()

    def get_queryset(self):
        if self.request.user.status in ('p'):
            return Course.objects.filter(teacher=self.request.user.pk)
        elif self.request.user.status in ('s'):
            return Course.objects.filter(student=self.request.user.pk)


class LectureToCourse(GenericAPIView):
    """ Лекции к курсу может добавить профессор."""

    permission_classes = [IsAuthenticated, IsRegisteredPersonCourse]
    serializer_class = LectureSerializer
    parser_classes = (FormParser, MultiPartParser)

    def get(self, request, course_id):
        if request.user.status in ('p'):
            quer = Course.objects.filter(teacher=request.user.pk).get(id=course_id)
            serializer = CourseLectureSerializer(quer)
            return Response(serializer.data)
        elif request.user.status in ('s'):
            quer = Course.objects.filter(student=request.user.pk).get(id=course_id)
            serializer = CourseLectureSerializer(quer)
            return Response(serializer.data)

    def post(self, request, course_id):
        serializer = LectureSerializer(data=self.request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(course_id=course_id, professor_id=self.request.user.id)  # ПООООМЕНЯТЬ ID
            return Response(serializer.data, status=status.HTTP_200_OK)


class LectureRUD(generics.RetrieveUpdateDestroyAPIView):
    """ Обновление, удаление лекции. Может только автор лекции """

    permission_classes = [IsAuthenticated, IsProffesorToLecture]
    serializer_class = LectureSerializer
    queryset = Lecture.objects.all()
    lookup_field = "id"  # id лекции
