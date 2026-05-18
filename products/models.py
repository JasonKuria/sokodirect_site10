import uuid
from django.db import models
from django.contrib.auth.models import User  # ← add this line

class County(models.Model):
    name = models.CharField(max_length=200)  # e.g. Nairobi, Mombasa, Nakuru
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Counties'


class Category(models.Model):
    name = models.CharField(max_length=200)  # e.g. Vegetables, Dairy
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'


class Speciality(models.Model):
    name = models.CharField(max_length=200)  # e.g. Dairy, Tomatoes, Poultry
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return self.name
    



class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE,  # delete profile if user deleted
        null=True, blank=True
    )
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=500, null=True, blank=True)
    username = models.CharField(max_length=200, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    profile_image = models.ImageField(
        null=True, blank=True,
        upload_to='profiles/',       # saves to media/profiles/
        default='profiles/default.jpg'
    )
    is_farmer = models.BooleanField(default=False)  # True=farmer, False=buyer
    # Location
    county = models.ForeignKey(
        'County', on_delete=models.SET_NULL,
        null=True, blank=True
    )
    # Social/contact links
    phone = models.CharField(max_length=20, null=True, blank=True)
    whatsapp_link = models.CharField(max_length=500, null=True, blank=True)
    website = models.CharField(max_length=500, null=True, blank=True)
    # Farmer specialities — ManyToMany
    specialities = models.ManyToManyField('Speciality', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    def __str__(self):
        return str(self.username)



class Product(models.Model):
    # Owner — which farmer listed this produce
    owner = models.ForeignKey(
        Profile, on_delete=models.SET_NULL,
        null=True, blank=True
    )
    # Where the produce is from
    county = models.ForeignKey(
        County, on_delete=models.SET_NULL,
        null=True, blank=True
    )
    # Product details
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    price = models.CharField(max_length=200, null=True, blank=True)
    quantity_available = models.CharField(max_length=200, null=True, blank=True)
    unit = models.CharField(max_length=50, null=True, blank=True)  # kg, bunch, piece

    # Product image field
    # null=True, blank=True - image is optional
    # default= - shows this image if no image is uploaded
    # upload_to= - where uploaded images are saved on the server
    featured_image = models.ImageField(
        null=True, blank=True,
        default='default.jpg',
        upload_to='products/' # saves to media/products/
    )




    # Contact
    contact_link = models.CharField(max_length=2000, null=True, blank=True)
    farm_link = models.CharField(max_length=2000, null=True, blank=True)

    # Categories — ManyToMany (replaces tutorial tags)
    categories = models.ManyToManyField(Category, blank=True)

    # Vote tracking — updated by signals later
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return self.title
    

class Review(models.Model):
    VOTE_TYPE = (
        ('up', 'Upvote'),
        ('down', 'Downvote'),
    )
    # reviewer = models.ForeignKey(Profile...) — added when Profile ready
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE
    )
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=200, choices=VOTE_TYPE)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return self.value
    


class Message(models.Model):
    sender = models.ForeignKey(
        Profile, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='sent_messages'
    )
    recipient = models.ForeignKey(
        Profile, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='received_messages'
    )
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=500, null=True, blank=True)
    subject = models.CharField(max_length=200, null=True, blank=True)
    body = models.TextField()
    is_read = models.BooleanField(default=False)  # read/unread inbox
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    def __str__(self):
        return self.subject














