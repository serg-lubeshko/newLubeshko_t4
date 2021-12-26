from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from app.models import Lecture, Course
from app.serializers.serializers_course import CourseSerializer
from app.serializers.serializers_person import UserSerializer


class LectureSerializer(serializers.ModelSerializer):
    """>>> LectureToCourse >>>  LectureRUD """

    professor = serializers.PrimaryKeyRelatedField(read_only=True)
    name_course = serializers.PrimaryKeyRelatedField(read_only=True)
    title = serializers.CharField(max_length=255, validators=[UniqueValidator(queryset=Lecture.objects.all())])


    class Meta:
        model = Lecture
        fields = ['id', 'title', 'file_present', 'published_at', 'professor', 'name_course']


class CourseLectureSerializer(serializers.ModelSerializer):
    ''' >>> LectureToCourse '''

    # lectures=serializers.StringRelatedField(many=True, read_only=True)
    lectures = LectureSerializer(many=True, read_only=True)

    # name_course=serializers.Lecture2Serializer(many=True, read_only=True)
    class Meta:
        model = Course
        fields = ['id','name_course', 'lectures']
