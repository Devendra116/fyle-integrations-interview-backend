from rest_framework import generics, status
from rest_framework.response import Response

from .models import Teacher

from apps.students.models import Assignment, Student
from .serializers import TeacherAssignmentSerializer


class AssignmentsView(generics.ListCreateAPIView):
    serializer_class = TeacherAssignmentSerializer

    def get(self, request, *args, **kwargs):
        assignments = Assignment.objects.filter(teacher__user=request.user)

        return Response(
            data=self.serializer_class(assignments, many=True).data,
            status=status.HTTP_200_OK
        )
