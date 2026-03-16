from django.db import models
from core.models import TimeStampedModel


class ProductCourseMapping(TimeStampedModel):
    product = models.ForeignKey(
        "product.Product",
        on_delete=models.CASCADE,
        related_name="course_mappings",
    )
    course = models.ForeignKey(
        "course.Course",
        on_delete=models.CASCADE,
        related_name="product_mappings",
    )
    primary_mapping = models.BooleanField(default=False)

    class Meta:
        unique_together = ("product", "course")

    def __str__(self):
        return f"{self.product} - {self.course}"
