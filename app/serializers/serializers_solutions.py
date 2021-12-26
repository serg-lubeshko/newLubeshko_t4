from rest_framework import serializers

from app.models import Solution, Homework
from app.serializers.serializers_lecture import LectureSerializer


class SolutionSerializers(serializers.ModelSerializer):
    # homework_solution = serializers.IntegerField(source='homework_solution.id')

    task_solved = serializers.BooleanField(read_only=True)
    class Meta:
        model = Solution
        fields = ['id', 'task_solved', 'solution_task', 'homework_solution']
        # read_only_field = ('homework_solution',)

    def validate(self, data):
        user_id = self.context['request'].user.pk

        # print(self.context['request'].data, 'ooooooooooooo')
        homework_id = self.context['request'].data['homework_solution']
        data_dict = dict(data)
        if Solution.objects.filter(user_solution_id=user_id, homework_solution_id=homework_id).count() > 0:
            raise serializers.ValidationError("Вы добавили уже решение")
        # if Lecture.objects.filter(id=data_dict['lecture_for_homework_id']).first().professor.pk != user_id:
        #     raise serializers.ValidationError("У вас нет прав")
        return data

class HomeworkForSolution(serializers.ModelSerializer):
    lecture_for_homework = LectureSerializer()
    # title = serializers.CharField(read_only=True)

    class Meta:
        model = Homework
        fields = ['id', 'title', 'homework_task', 'lecture_for_homework']
