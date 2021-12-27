from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from app.conf.permission import IsProfessorOrReadOnlyMark, IsProfessorOrReadOnlyMarkDetail, IsStudentReadOnly
from app.models import MyUser, Mark, Solution, MessageTeacher
from app.serializers.serializers_mark_message import MarkDetailSerializers, MarkSerializer, \
    SolutionForCheckProfessorSerializer, StudentLookHisSolutionSerializers, StudentMessageSerializers, \
    ListMessageForProfessorSerialezers


class ProfessorWatchHomework(generics.GenericAPIView):
    """ Профессор смотрит solution и ставит оценку, может написать коментарий"""

    permission_classes = [IsAuthenticated, IsProfessorOrReadOnlyMark]
    serializer_class = MarkSerializer
    queryset = MyUser.objects.all()

    def get(self, request):
        # query = Solution.objects.filter(task_solved=True,
        #                                 homework_solution__professor_id=request.user.pk,
        #                                 task_cheked=False)

        # serializer = SolutionForCheckProfessorSerializer(query, many=True)
        query = Solution.objects.filter(task_solved=True,
                                        homework_solution__professor_id=request.user.pk)
        checked_query = query.filter(task_cheked=True)
        unchecked_query = query.filter(task_cheked=False)
        checked_serializer = SolutionForCheckProfessorSerializer(checked_query, many=True)
        unchecked_serializer = SolutionForCheckProfessorSerializer(unchecked_query, many=True)
        # return Response(serializer.data)
        return Response(({'unchecked_solution': unchecked_serializer.data},
                         {'checked_solution': checked_serializer.data},)
                        )

    def post(self, request):
        serializer = self.serializer_class(data=self.request.data,
                                           context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save(user_mark_id=request.user.pk)
            Solution.objects.filter(id=request.data["solution_id"]).update(task_cheked=True)
            MessageTeacher.objects.create(message_solution_teachers_id=request.data["solution_id"],
                                          text=request.data["text_message_teacher"])
            return Response(status=status.HTTP_200_OK)


# class ProfessorChangeMark(generics.GenericAPIView):
#     serializer_class = MarkDetailSerializers
#
#     def get_queryset(self):
#         return Mark.objects.get(solution_id=self.request.data['solution_id'])
#
#     def put(self, request):
#         object = self.get_queryset()
#         print(object,'88888888888')
#         # serializer = MarkDetailSerializers({'solution_id':request.data['solution_id']},
#         #                                    {'user_mark_id': request.data.user.pk},
#         #                                    instance=object,
#         #                                    partial=True )
#         serializer = MarkDetailSerializers(instance=object,
#                                            partial=True)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             return Response(status=status.HTTP_201_CREATED)
#         else:
#             return Response(status=status.HTTP_400_BAD_REQUEST)


class ProfessorMarkDetail(generics.RetrieveUpdateAPIView):
    """ Профессор меняет оценку"""

    permission_classes = [IsAuthenticated, IsProfessorOrReadOnlyMarkDetail]
    serializer_class = MarkDetailSerializers
    queryset = Mark.objects.all()
    lookup_field = 'solution_id'

    def put(self, request, *args, **kwargs):
        print(kwargs, request.data, '********Добавить сохраненияе*****')
        MessageTeacher.objects.create(message_solution_teachers_id=kwargs['solution_id'],
                                      text=request.data["text_message_teacher"])
        return self.update(request, *args, **kwargs)


class StudentLookHisSolution(generics.GenericAPIView):
    """ Студент смотрит solution и оценку, может написать коментарий"""

    permission_classes = [IsAuthenticated, IsStudentReadOnly]
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


class StudentMessage(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsStudentReadOnly]
    serializer_class = StudentMessageSerializers

    # def get(self, request, solution_id):
    #     query = Solution.objects.get(id=solution_id)
    #     serializer = StudentMessageGETSerializers(query)
    #     return Response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=self.request.data,
                                           context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save(user_message_id=request.user.pk)
            return Response(status=status.HTTP_200_OK)


class ListMessageForProfessor(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsProfessorOrReadOnlyMarkDetail]
    serializer_class = ListMessageForProfessorSerialezers

    def get_queryset(self):
        return Solution.objects.filter(task_solved=True,
                                       homework_solution__professor_id=self.request.user.pk)
