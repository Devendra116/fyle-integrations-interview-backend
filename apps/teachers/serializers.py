from attr import attr
from rest_framework import serializers
from apps.students.models import Assignment


class TeacherAssignmentSerializer(serializers.ModelSerializer):
    """
    Teacher Assignment serializer
    """
    class Meta:
        model = Assignment
        fields = '__all__'

    def validate(self, attrs):
        
        if 'content' in attrs and attrs['content']:
            raise serializers.ValidationError('Teacher cannot change the content of the assignment')
        if 'student' in attrs and attrs['student']:
            raise serializers.ValidationError('Teacher cannot change the student who submitted the assignment')
        if self.initial_data['teacher'] != self.initial_data['assignment_teacher']:
            raise serializers.ValidationError('Teacher cannot grade for other teacher''s assignment')
        if attrs['state'] == 'GRADED':
            raise serializers.ValidationError('GRADED assignments cannot be graded again')
        if attrs['state'] == 'DRAFT':
            raise serializers.ValidationError('SUBMITTED assignments can only be graded')
        
        attrs['state']='GRADED'
        if self.partial:
            print("in partial")
            return attrs

        return super().validate(attrs)
