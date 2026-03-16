from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from core.utils import get_object_or_none
from .models import CourseCertificationMapping
from .serializers import CourseCertificationMappingSerializer


class CourseCertificationMappingListView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "course_id",
                openapi.IN_QUERY,
                description="Filter by course ID",
                type=openapi.TYPE_INTEGER,
            ),
        ],
        responses={200: CourseCertificationMappingSerializer(many=True)},
    )
    def get(self, request):
        queryset = CourseCertificationMapping.objects.all()
        course_id = request.query_params.get("course_id")
        if course_id:
            queryset = queryset.filter(course_id=course_id)
        serializer = CourseCertificationMappingSerializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=CourseCertificationMappingSerializer,
        responses={201: CourseCertificationMappingSerializer, 400: "Validation Error"},
    )
    def post(self, request):
        serializer = CourseCertificationMappingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseCertificationMappingDetailView(APIView):
    @swagger_auto_schema(responses={200: CourseCertificationMappingSerializer, 404: "Not Found"})
    def get(self, request, pk):
        mapping = get_object_or_none(CourseCertificationMapping, pk)
        if mapping is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CourseCertificationMappingSerializer(mapping)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=CourseCertificationMappingSerializer,
        responses={200: CourseCertificationMappingSerializer, 400: "Validation Error", 404: "Not Found"},
    )
    def put(self, request, pk):
        mapping = get_object_or_none(CourseCertificationMapping, pk)
        if mapping is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CourseCertificationMappingSerializer(mapping, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        request_body=CourseCertificationMappingSerializer,
        responses={200: CourseCertificationMappingSerializer, 400: "Validation Error", 404: "Not Found"},
    )
    def patch(self, request, pk):
        mapping = get_object_or_none(CourseCertificationMapping, pk)
        if mapping is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CourseCertificationMappingSerializer(mapping, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={204: "No Content", 404: "Not Found"})
    def delete(self, request, pk):
        mapping = get_object_or_none(CourseCertificationMapping, pk)
        if mapping is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        mapping.is_active = False
        mapping.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
