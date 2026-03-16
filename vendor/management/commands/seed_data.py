from django.core.management.base import BaseCommand
from vendor.models import Vendor
from product.models import Product
from course.models import Course
from certification.models import Certification
from vendor_product_mapping.models import VendorProductMapping
from product_course_mapping.models import ProductCourseMapping
from course_certification_mapping.models import CourseCertificationMapping


class Command(BaseCommand):
    help = "Load initial data for development and testing"

    def handle(self, *args, **options):
        microsoft = Vendor.objects.create(name="Microsoft", code="MSFT", description="Microsoft Corporation")
        amazon = Vendor.objects.create(name="Amazon Web Services", code="AWS", description="Cloud computing platform by Amazon")
        google = Vendor.objects.create(name="Google Cloud", code="GCP", description="Google Cloud Platform services")

        azure = Product.objects.create(name="Microsoft Azure", code="AZURE", description="Microsoft's cloud computing service")
        aws_cloud = Product.objects.create(name="AWS Cloud", code="AWSC", description="Amazon's suite of cloud services")
        gcp = Product.objects.create(name="Google Cloud Platform", code="GCPLT", description="Google's public cloud offering")

        az900_course = Course.objects.create(name="Azure Fundamentals", code="AZ900", description="Introductory course covering core Azure concepts and services")
        saa_course = Course.objects.create(name="AWS Solutions Architect", code="SAA-C03", description="Covers designing distributed systems on AWS")
        ace_course = Course.objects.create(name="Google Cloud Associate Engineer", code="GCP-ACE", description="Covers deploying and managing applications on GCP")

        az900_cert = Certification.objects.create(name="AZ-900: Microsoft Azure Fundamentals", code="AZ-900", description="Entry-level certification for Azure cloud concepts")
        saa_cert = Certification.objects.create(name="AWS Certified Solutions Architect – Associate", code="AWS-SAA", description="Validates ability to design AWS solutions")
        ace_cert = Certification.objects.create(name="Associate Cloud Engineer", code="GCP-ACE-CERT", description="Google certification for deploying and managing cloud projects")

        VendorProductMapping.objects.create(vendor=microsoft, product=azure, primary_mapping=True)
        VendorProductMapping.objects.create(vendor=amazon, product=aws_cloud, primary_mapping=True)
        VendorProductMapping.objects.create(vendor=google, product=gcp, primary_mapping=True)

        ProductCourseMapping.objects.create(product=azure, course=az900_course, primary_mapping=True)
        ProductCourseMapping.objects.create(product=aws_cloud, course=saa_course, primary_mapping=True)
        ProductCourseMapping.objects.create(product=gcp, course=ace_course, primary_mapping=True)

        CourseCertificationMapping.objects.create(course=az900_course, certification=az900_cert, primary_mapping=True)
        CourseCertificationMapping.objects.create(course=saa_course, certification=saa_cert, primary_mapping=True)
        CourseCertificationMapping.objects.create(course=ace_course, certification=ace_cert, primary_mapping=True)

        self.stdout.write(self.style.SUCCESS("Done. Created vendors, products, courses, certifications and their mappings."))
