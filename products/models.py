import uuid
from django.db import models
# DO NOT import from users here

class County(models.Model):
    name = models.CharField(max_length=200)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Counties'

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=200)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        full_path = []
        k = self
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' > '.join(full_path[::-1])

# ============ SPECIALITY MODEL (ADDED HERE) ============
class Speciality(models.Model):
    name = models.CharField(max_length=200)  # e.g. Dairy, Tomatoes, Poultry
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
# ============ END OF SPECIALITY MODEL ============


class Product(models.Model):
    # Use string reference - no import needed
    owner = models.ForeignKey(
        'users.Profile',  # ✅ String reference
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    
    county = models.ForeignKey(
        County,  # ✅ Can use direct import because it's in same file
        on_delete=models.SET_NULL,
        null=True, blank=True
    )
    
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    price = models.CharField(max_length=200, null=True, blank=True)
    quantity_available = models.CharField(max_length=200, null=True, blank=True)
    unit = models.CharField(max_length=50, null=True, blank=True)
    
    featured_image = models.ImageField(
        null=True, blank=True,
        default='default.jpg',
        upload_to='products/'
    )
    
    contact_link = models.CharField(max_length=2000, null=True, blank=True)
    farm_link = models.CharField(max_length=2000, null=True, blank=True)
    
    categories = models.ManyToManyField(Category, blank=True)
    
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)
    
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.title
    
    @property
    def imageURL(self):
        try:
            url = self.featured_image.url
        except:
            url = ''
        return url


class Review(models.Model):
    VOTE_TYPE = (
        ('up', 'Upvote'),
        ('down', 'Downvote'),
    )
    
    owner = models.ForeignKey(
        'users.Profile',  # ✅ String reference
        on_delete=models.CASCADE,
        null=True
    )
    
    product = models.ForeignKey(
        Product,  # ✅ Direct import - same file
        on_delete=models.CASCADE
    )
    
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=200, choices=VOTE_TYPE)
    
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [['owner', 'product']]

    def __str__(self):
        return self.value