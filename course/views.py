from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Course
from .serializers import CourseSerializer


class CourseListView(APIView):
    @swagger_auto_schema(
        responses={200: CourseSerializer(many=True)},
        manual_parameters=[
            openapi.Parameter(
                'is_active',
                openapi.IN_QUERY,
                type=openapi.TYPE_BOOLEAN,
                description='Filter by active status',
            )
        ],
    )
    def get(self, request):
        queryset = Course.objects.all()
        is_active = request.query_params.get('is_active')
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        serializer = CourseSerializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=CourseSerializer, responses={201: CourseSerializer})
    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseDetailView(APIView):
    def get_object(self, pk):
        try:
            return Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            return None

    @swagger_auto_schema(responses={200: CourseSerializer})
    def get(self, request, pk):
        course = self.get_object(pk)
        if course is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CourseSerializer(course)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=CourseSerializer, responses={200: CourseSerializer})
    def put(self, request, pk):
        course = self.get_object(pk)
        if course is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CourseSerializer(course, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=CourseSerializer, responses={200: CourseSerializer})
    def patch(self, request, pk):
        course = self.get_object(pk)
        if course is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CourseSerializer(course, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={204: 'No Content'})
    def delete(self, request, pk):
        course = self.get_object(pk)
        if course is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
