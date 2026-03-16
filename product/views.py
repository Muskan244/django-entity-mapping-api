from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from core.utils import get_object_or_none
from .models import Product
from .serializers import ProductSerializer


class ProductListView(APIView):
    @swagger_auto_schema(
        responses={200: ProductSerializer(many=True)},
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
        queryset = Product.objects.all()
        is_active = request.query_params.get('is_active')
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=ProductSerializer, responses={201: ProductSerializer})
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailView(APIView):
    @swagger_auto_schema(responses={200: ProductSerializer})
    def get(self, request, pk):
        product = get_object_or_none(Product, pk)
        if product is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=ProductSerializer, responses={200: ProductSerializer})
    def put(self, request, pk):
        product = get_object_or_none(Product, pk)
        if product is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=ProductSerializer, responses={200: ProductSerializer})
    def patch(self, request, pk):
        product = get_object_or_none(Product, pk)
        if product is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={204: 'No Content'})
    def delete(self, request, pk):
        product = get_object_or_none(Product, pk)
        if product is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        product.is_active = False
        product.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
