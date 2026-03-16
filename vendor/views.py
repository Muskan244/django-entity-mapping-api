from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Vendor
from .serializers import VendorSerializer


class VendorListView(APIView):
    @swagger_auto_schema(
        responses={200: VendorSerializer(many=True)},
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
        queryset = Vendor.objects.all()
        is_active = request.query_params.get('is_active')
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        serializer = VendorSerializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=VendorSerializer, responses={201: VendorSerializer})
    def post(self, request):
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VendorDetailView(APIView):
    def get_object(self, pk):
        try:
            return Vendor.objects.get(pk=pk)
        except Vendor.DoesNotExist:
            return None

    @swagger_auto_schema(responses={200: VendorSerializer})
    def get(self, request, pk):
        vendor = self.get_object(pk)
        if vendor is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = VendorSerializer(vendor)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=VendorSerializer, responses={200: VendorSerializer})
    def put(self, request, pk):
        vendor = self.get_object(pk)
        if vendor is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = VendorSerializer(vendor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=VendorSerializer, responses={200: VendorSerializer})
    def patch(self, request, pk):
        vendor = self.get_object(pk)
        if vendor is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = VendorSerializer(vendor, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={204: 'No Content'})
    def delete(self, request, pk):
        vendor = self.get_object(pk)
        if vendor is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        vendor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
