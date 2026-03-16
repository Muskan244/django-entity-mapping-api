from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .models import VendorProductMapping
from .serializers import VendorProductMappingSerializer


class VendorProductMappingListView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "vendor_id",
                openapi.IN_QUERY,
                description="Filter by vendor ID",
                type=openapi.TYPE_INTEGER,
            ),
        ],
        responses={200: VendorProductMappingSerializer(many=True)},
    )
    def get(self, request):
        queryset = VendorProductMapping.objects.all()
        vendor_id = request.query_params.get("vendor_id")
        if vendor_id:
            queryset = queryset.filter(vendor_id=vendor_id)
        serializer = VendorProductMappingSerializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=VendorProductMappingSerializer,
        responses={201: VendorProductMappingSerializer, 400: "Validation Error"},
    )
    def post(self, request):
        serializer = VendorProductMappingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VendorProductMappingDetailView(APIView):
    def get_object(self, pk):
        try:
            return VendorProductMapping.objects.get(pk=pk)
        except VendorProductMapping.DoesNotExist:
            return None

    @swagger_auto_schema(responses={200: VendorProductMappingSerializer, 404: "Not Found"})
    def get(self, request, pk):
        mapping = self.get_object(pk)
        if mapping is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = VendorProductMappingSerializer(mapping)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=VendorProductMappingSerializer,
        responses={200: VendorProductMappingSerializer, 400: "Validation Error", 404: "Not Found"},
    )
    def put(self, request, pk):
        mapping = self.get_object(pk)
        if mapping is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = VendorProductMappingSerializer(mapping, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        request_body=VendorProductMappingSerializer,
        responses={200: VendorProductMappingSerializer, 400: "Validation Error", 404: "Not Found"},
    )
    def patch(self, request, pk):
        mapping = self.get_object(pk)
        if mapping is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = VendorProductMappingSerializer(mapping, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={204: "No Content", 404: "Not Found"})
    def delete(self, request, pk):
        mapping = self.get_object(pk)
        if mapping is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        mapping.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
