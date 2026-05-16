import uuid
from django.db import models

class Product(models.Model):
    # UUID — unique ID for each product listing
    # Better than integer IDs — no duplicates possible
    id = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        primary_key=True,
        editable=False        # no one can edit the ID via a form
    )

    # Product title — required field (null=False by default)
    title = models.CharField(max_length=200)

    # Product description — optional field
    description = models.TextField(null=True, blank=True)

    # Price description e.g. "KES 50 per kg"
    price = models.CharField(max_length=200, null=True, blank=True)

    # Location/county of the farm
    location = models.CharField(max_length=200, null=True, blank=True)

    # Contact link e.g. WhatsApp link or phone
    contact_link = models.CharField(max_length=2000, null=True, blank=True)

    # Source/farm link e.g. farmer's profile or page
    farm_link = models.CharField(max_length=2000, null=True, blank=True)

    # Auto-generated timestamp when listing is created
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title    # shows title in admin panel instead of "Product object"
