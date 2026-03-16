from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from core.utils import get_object_or_none
from .models import ProductCourseMapping
from .serializers import ProductCourseMappingSerializer


class ProductCourseMappingListView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "product_id",
                openapi.IN_QUERY,
                description="Filter by product ID",
                type=openapi.TYPE_INTEGER,
            ),
        ],
        responses={200: ProductCourseMappingSerializer(many=True)},
    )
    def get(self, request):
        queryset = ProductCourseMapping.objects.all()
        product_id = request.query_params.get("product_id")
        if product_id:
            queryset = queryset.filter(product_id=product_id)
        serializer = ProductCourseMappingSerializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=ProductCourseMappingSerializer,
        responses={201: ProductCourseMappingSerializer, 400: "Validation Error"},
    )
    def post(self, request):
        serializer = ProductCourseMappingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductCourseMappingDetailView(APIView):
    @swagger_auto_schema(responses={200: ProductCourseMappingSerializer, 404: "Not Found"})
    def get(self, request, pk):
        mapping = get_object_or_none(ProductCourseMapping, pk)
        if mapping is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ProductCourseMappingSerializer(mapping)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=ProductCourseMappingSerializer,
        responses={200: ProductCourseMappingSerializer, 400: "Validation Error", 404: "Not Found"},
    )
    def put(self, request, pk):
        mapping = get_object_or_none(ProductCourseMapping, pk)
        if mapping is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ProductCourseMappingSerializer(mapping, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        request_body=ProductCourseMappingSerializer,
        responses={200: ProductCourseMappingSerializer, 400: "Validation Error", 404: "Not Found"},
    )
    def patch(self, request, pk):
        mapping = get_object_or_none(ProductCourseMapping, pk)
        if mapping is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ProductCourseMappingSerializer(mapping, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={204: "No Content", 404: "Not Found"})
    def delete(self, request, pk):
        mapping = get_object_or_none(ProductCourseMapping, pk)
        if mapping is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        mapping.is_active = False
        mapping.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
