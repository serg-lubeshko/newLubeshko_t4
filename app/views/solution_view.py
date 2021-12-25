from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from app.conf.permission import IsStudentOrReadOnly
from app.models import Homework
from app.serializers.serializers_solutions import SolutionSerializers, HomeworkForSolution


class SolutionToHomework(generics.GenericAPIView):
    """ Решения студентов """

    permission_classes = [IsAuthenticated, IsStudentOrReadOnly]
    serializer_class = SolutionSerializers
    queryset = Homework.objects.all()

    def get(self, request):
        query = Homework.objects.filter(lecture_for_homework__course__student=self.request.user)
        serializer = HomeworkForSolution(query, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=self.request.data,
                                           context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save(user_solution_id=self.request.user.id)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)