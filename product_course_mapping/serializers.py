from rest_framework import serializers
from product.serializers import ProductSerializer
from course.serializers import CourseSerializer
from .models import ProductCourseMapping


class ProductCourseMappingSerializer(serializers.ModelSerializer):
    product_detail = ProductSerializer(source="product", read_only=True)
    course_detail = CourseSerializer(source="course", read_only=True)

    class Meta:
        model = ProductCourseMapping
        fields = "__all__"

    def validate(self, data):
        product = data.get("product", getattr(self.instance, "product", None))
        course = data.get("course", getattr(self.instance, "course", None))

        qs = ProductCourseMapping.objects.filter(product=product, course=course)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError(
                "This product-course mapping already exists."
            )

        if data.get("primary_mapping", False):
            qs = ProductCourseMapping.objects.filter(
                product=product, primary_mapping=True
            )
            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise serializers.ValidationError(
                    "A primary mapping already exists for this product."
                )

        return data
