from rest_framework import serializers
from vendor.serializers import VendorSerializer
from product.serializers import ProductSerializer
from .models import VendorProductMapping


class VendorProductMappingSerializer(serializers.ModelSerializer):
    vendor_detail = VendorSerializer(source="vendor", read_only=True)
    product_detail = ProductSerializer(source="product", read_only=True)

    class Meta:
        model = VendorProductMapping
        fields = "__all__"

    def validate(self, data):
        vendor = data.get("vendor", getattr(self.instance, "vendor", None))
        product = data.get("product", getattr(self.instance, "product", None))

        qs = VendorProductMapping.objects.filter(vendor=vendor, product=product)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError(
                "This vendor-product mapping already exists."
            )

        if data.get("primary_mapping", False):
            qs = VendorProductMapping.objects.filter(
                vendor=vendor, primary_mapping=True
            )
            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise serializers.ValidationError(
                    "A primary mapping already exists for this vendor."
                )

        return data
