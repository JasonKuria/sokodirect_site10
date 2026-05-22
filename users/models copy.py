import uuid
from django.db import models
from django.contrib.auth.models import User # Django's built-in User model

# import some receiver function 
# to create profile automatically when a new user is created
# the save method is called on the user model, 
# and the receiver function will create a corresponding profile
from django.db.models.signals import post_save, post_delete

# using django decorators to connect the receiver function to the signal
from django.dispatch import receiver


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

# this is the receiver function (profileUpdated)
# that we are going to trigger when a new user is created
# where we will parse some sender 
# the sender is the model (User) that sends this signal and 
# the instance is the actual user that was created
#@receiver(post_save, sender=Profile)
def CreateProfile(sender, instance, created, **kwargs):
    if created: # only create profile if user is created, not updated
        user = instance # the user that was created
        profile = Profile.objects.create( # create a new profile with the following fields
            user=user, # link the profile to the user
            username=user.username, # copy username from user to profile for easy access
            email=user.email, # copy email from user to profile for easy access
            name=user.first_name # copy first name from user to profile for easy access
        )
        print('Profile created for user: ', profile)

def deleteUser(sender, instance, **kwargs):
    user = instance.user # get the user linked to the profile that is being deleted
    user.delete() # delete the user from the User model
    print('Deleting User....!')  

# Every time a user is created, 
# the CreateProfile function will be called to create a corresponding profile
# this is a receiver (post_save) 
# that listens for when a user is saved (created or updated)
post_save.connect(CreateProfile, sender=User)    

# When a profile is deleted 
# we want to delete the corresponding user as well, 
# from the User model
post_delete.connect(deleteUser, sender=Profile) # When 