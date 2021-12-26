from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from app.conf.permission import IsProfessorOrReadOnlyMark, IsProfessorOrReadOnlyMarkDetail
from app.models import MyUser, Mark, Homework, Solution
from app.serializers.serializers_mark_message import MarkDetailSerializers, SolutionForProfessorCheckSerializer, \
    MarkSerializer, SolutionForCheckProfessorSerializer, StudentLookHisSolutionSerializers


class ProfessorWatchHomework(generics.GenericAPIView):
    """ Профессор смотрит solution и ставит оценку, может написать коментарий"""

    permission_classes = [IsAuthenticated, IsProfessorOrReadOnlyMark]
    serializer_class = MarkSerializer
    queryset = MyUser.objects.all()

    def get(self, request):
        query = Solution.objects.filter(task_solved=True,
                                        homework_solution__professor_id=request.user.pk,
                                        task_cheked=False)
        serializer = SolutionForCheckProfessorSerializer(query, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=self.request.data,
                                           context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save(user_mark_id=request.user.pk)
            Solution.objects.filter(id=request.data["solution_id"]).update(task_cheked=True)
            return Response(status=status.HTTP_200_OK)


class ProfessorMarkDetail(generics.RetrieveUpdateAPIView):
    """ Профессор меняет оценку"""

    # permission_classes = [IsAuthenticated, IsProfessorOrReadOnlyMarkDetail]
    serializer_class = MarkDetailSerializers
    queryset = Mark.objects.all()
    lookup_field = 'solution_id'


class StudentLookHisSolution(generics.GenericAPIView):
    """ Студент смотрит solution и оценку, может написать коментарий"""

    permission_classes = [IsAuthenticated]
    serializer_class = StudentLookHisSolutionSerializers

    # queryset = Solution.objects.filter()

    def get(self, request):
        query = Solution.objects.filter(task_solved=True,
                                        user_solution_id=request.user.pk)
        verified_query = query.filter(task_cheked=True)
        unverified_query = query.filter(task_cheked=False)
        verified_serializer = StudentLookHisSolutionSerializers(verified_query, many=True)
        unverified_serializer = StudentLookHisSolutionSerializers(unverified_query, many=True)
        return Response(({'verified_homework': verified_serializer.data},
                         {'unverified_homework': unverified_serializer.data})
                        )

# ДОООООООООООООООБАВИТЬ СООБЩЕНИЯ
# Возможность студента смотреть свои работы
# Студент пишет коментарии
# Permission
# Пересмотреть название полей
# Переделать лекции


# Не понятно как решить проблему с миграциями
