from django.db import models
from core.models import TimeStampedModel


class VendorProductMapping(TimeStampedModel):
    vendor = models.ForeignKey(
        "vendor.Vendor",
        on_delete=models.CASCADE,
        related_name="product_mappings",
    )
    product = models.ForeignKey(
        "product.Product",
        on_delete=models.CASCADE,
        related_name="vendor_mappings",
    )
    primary_mapping = models.BooleanField(default=False)

    class Meta:
        unique_together = ("vendor", "product")

    def __str__(self):
        return f"{self.vendor} - {self.product}"
