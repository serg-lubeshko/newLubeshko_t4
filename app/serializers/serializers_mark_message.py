from rest_framework import serializers

from app.models import MessageTeacher, Solution, MyUser, Mark, Homework
from app.serializers.serializers_solutions import SolutionSerializers


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageTeacher
        fields = ['id', 'text']


class MarkSerializer(serializers.ModelSerializer):
    solution_id = serializers.ChoiceField(choices=[i.id for i in Solution.objects.all()])
    mark_message = MessageSerializer()
    mark = serializers.IntegerField(min_value=0, max_value=10)

    class Meta:
        model = Mark
        fields = ['mark', 'solution_id', 'mark_message']

    def create(self, validated_data):
        message = dict(validated_data.pop('mark_message'))
        mark_id = (Mark.objects.create(**validated_data)).pk
        instance = message | {'mark_message_id': mark_id}
        return MessageTeacher.objects.create(**instance)


class SolutionForProfessorCheckSerializer(serializers.ModelSerializer):
    id_user = serializers.IntegerField(source='id', read_only=True)
    user_solution = SolutionSerializers(many=True)

    class Meta:
        model = MyUser
        fields = ['id_user', 'username', 'user_solution', ]


class MarkDetailSerializers(serializers.ModelSerializer):
    message_professor = MessageSerializer(read_only=True, many=True, source='mark_message')

    class Meta:
        model = Mark
        fields = ['mark', 'solution', 'message_professor']


# ____________________SolutionForCheckProfessorSerializer______________________________________

class UserToSolutionForCheckProfessorSerializer(serializers.ModelSerializer):
    id_user = serializers.IntegerField(source='id', read_only=True)

    class Meta:
        model = MyUser
        fields = ['id_user', 'username']


class HSToSolutionForCheckProfessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Homework
        fields = ['id', 'title']


class SolutionForCheckProfessorSerializer(serializers.ModelSerializer):
    user_solution = UserToSolutionForCheckProfessorSerializer()
    homework_solution = HSToSolutionForCheckProfessorSerializer()

    class Meta:
        model = Solution
        fields = ['id', 'solution_task', 'user_solution', 'homework_solution']


# ____________________StudentLookHisSolutionSerializers__________________
class MarkToStudentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Mark
        fields = ['id', 'mark']


class StudentLookHisSolutionSerializers(serializers.ModelSerializer):
    mark_solution = MarkToStudentSerializers()

    class Meta:
        model = Solution
        fields = ['mark_solution' ,'id', 'solution_task']
