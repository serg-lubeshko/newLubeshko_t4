from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from app.conf.permission import IsLecturerOrReadOnly
from app.models import Homework, Lecture
from app.serializers.serializers_homework import HomeworkSerializer, LectureFofHomework


class HomeworkToLecture(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsLecturerOrReadOnly]
    serializer_class = HomeworkSerializer
    queryset = Homework.objects.all()

    def get(self, request):
        query = Lecture.objects.filter(professor=self.request.user)
        serializer = LectureFofHomework(query, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=self.request.data,
                                           context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save(professor_id=self.request.user.id)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
