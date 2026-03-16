from rest_framework import serializers
from course.serializers import CourseSerializer
from certification.serializers import CertificationSerializer
from .models import CourseCertificationMapping


class CourseCertificationMappingSerializer(serializers.ModelSerializer):
    course_detail = CourseSerializer(source="course", read_only=True)
    certification_detail = CertificationSerializer(source="certification", read_only=True)

    class Meta:
        model = CourseCertificationMapping
        fields = "__all__"

    def validate(self, data):
        course = data.get("course", getattr(self.instance, "course", None))
        certification = data.get(
            "certification", getattr(self.instance, "certification", None)
        )

        qs = CourseCertificationMapping.objects.filter(
            course=course, certification=certification
        )
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError(
                "This course-certification mapping already exists."
            )

        if data.get("primary_mapping", False):
            qs = CourseCertificationMapping.objects.filter(
                course=course, primary_mapping=True
            )
            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise serializers.ValidationError(
                    "A primary mapping already exists for this course."
                )

        return data
