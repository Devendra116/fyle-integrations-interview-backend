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

    def patch(self, request, *args, **kwargs):
        teacher = Teacher.objects.get(user=request.user)
        request.data['teacher'] = teacher.id
        state = Assignment.objects.get(pk=request.data['id'])
        request.data['state']=state.state
        request.data['assignment_teacher']=state.teacher.id
        try:
            assignment = Assignment.objects.get(pk=request.data['id'])
        except Assignment.DoesNotExist:
            return Response(
                data={'error': 'Assignment does not exist/permission denied'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.serializer_class(assignment, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(
                data=serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            data=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
