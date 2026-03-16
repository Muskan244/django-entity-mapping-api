from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from core.utils import get_object_or_none
from .models import Certification
from .serializers import CertificationSerializer


class CertificationListView(APIView):
    @swagger_auto_schema(
        responses={200: CertificationSerializer(many=True)},
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
        queryset = Certification.objects.all()
        is_active = request.query_params.get('is_active')
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        serializer = CertificationSerializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=CertificationSerializer, responses={201: CertificationSerializer})
    def post(self, request):
        serializer = CertificationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CertificationDetailView(APIView):
    @swagger_auto_schema(responses={200: CertificationSerializer})
    def get(self, request, pk):
        certification = get_object_or_none(Certification, pk)
        if certification is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CertificationSerializer(certification)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=CertificationSerializer, responses={200: CertificationSerializer})
    def put(self, request, pk):
        certification = get_object_or_none(Certification, pk)
        if certification is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CertificationSerializer(certification, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=CertificationSerializer, responses={200: CertificationSerializer})
    def patch(self, request, pk):
        certification = get_object_or_none(Certification, pk)
        if certification is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CertificationSerializer(certification, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={204: 'No Content'})
    def delete(self, request, pk):
        certification = get_object_or_none(Certification, pk)
        if certification is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        certification.is_active = False
        certification.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
