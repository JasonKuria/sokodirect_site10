import uuid
from django.db import models
from django.contrib.auth.models import User # Django's built-in User model




class Profile(models.Model):
    # OneToOne with Django's User model
    # One user = one profile, one profile = one user
    # CASCADE: if user is deleted, profile is deleted too
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True, blank=True
    )

    # Basic info — replicated from User for easy access
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=500, null=True, blank=True)
    username = models.CharField(max_length=200, null=True, blank=True)
    short_intro = models.CharField(max_length=200, blank=True, null=True)
    
    # User(Farm) profile info
    bio = models.TextField(null=True, blank=True)

    # Profile image
    # upload_to='profiles/' saves images in media/profiles/
    # default= shows this image until user(farmer) uploads their own
    profile_image = models.ImageField(
        null=True, blank=True,
        upload_to='profiles/',
        default='profiles/user-default.png'
    )

    # Location
    county = models.ForeignKey(
        'products.County',    # referencing County from products app
        on_delete=models.SET_NULL,
        null=True, blank=True
    )

    # User(Farmer) specialities - what they grow or rear
    # ManyToMany - one user(farmer) can have many specialities
    specialities = models.ManyToManyField('Speciality', blank=True)

    # Contact links
    phone = models.CharField(max_length=20, null=True, blank=True)
    whatsapp_link = models.CharField(max_length=500, null=True, blank=True)
    website = models.CharField(max_length=500, null=True, blank=True)
    social_twitter = models.CharField(max_length=200, null=True, blank=True)
    youtube = models.CharField(max_length=200, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True,
        primary_key=True, editable=False
    )

    def __str__(self):
        # Display username in admin panel instead of "Profile object"
        #return str(self.user.username)
        return str(self.username)


# User’s (Farmer's) speciality e.g. Dairy, Tomatoes, Poultry
# ManyToMany with Profile - one user(farmer) can have many specialities
# one speciality can belong to many farmers
class Speciality(models.Model):
    owner = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    name = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True,
        primary_key=True, editable=False
    )

    def __str__(self):
        return self.name
    
class Message(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)    
    recipient = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name="messages")    
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True)   
    subject = models.CharField(max_length=200, null=True, blank=True)     
    body = models.TextField()
    is_read = models.BooleanField(default=False, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True,
        primary_key=True, editable=False
    )    

    def __str__(self):
        return self.subject 
    
    class Meta:
        ordering = ['is_read', '-created']
