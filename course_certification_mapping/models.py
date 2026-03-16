from django.db import models
from core.models import TimeStampedModel


class CourseCertificationMapping(TimeStampedModel):
    course = models.ForeignKey(
        "course.Course",
        on_delete=models.CASCADE,
        related_name="certification_mappings",
    )
    certification = models.ForeignKey(
        "certification.Certification",
        on_delete=models.CASCADE,
        related_name="course_mappings",
    )
    primary_mapping = models.BooleanField(default=False)

    class Meta:
        unique_together = ("course", "certification")

    def __str__(self):
        return f"{self.course} - {self.certification}"
