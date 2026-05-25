import uuid
from django.db import models
#from django.contrib.auth.models import User  # ← add this line
from users.models import Profile # import Profile from the users app



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
    


class Product(models.Model):
    # Which user(farmer) listed this produce
    # SET_NULL: if farmer deletes account, keep the listing but clear owner
    # null=True: a product can exist without an owner temporarily
    owner = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
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

    class Meta:
        # newest products first 
        # when we query for products, they will be order
        # -ed by created date descending by default 
        # ordering = ['-created']  
        ordering = ['created']  # oldest products first



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
    
    class Meta: # newest products first when we query for products, they will be order -ed by created date descending by default
        #ordering = ['created']  # oldest products first
        ordering = ['-vote_ratio', '-vote_total', 'title']  # order by vote ratio desc, then vote total desc, then title asc

    @property
    def reviewers(self): # this is a property method that returns a list of user IDs who have reviewed this product
        queryset = self.review_set.all().values_list('owner__id', flat=True) # get a list of user IDs who have reviewed this product using the reverse relationship
        return queryset
    
    @property # this means we can call product.vote_count without parentheses, like an attribute instead of a method
    def getVoteCount(self): 
        reviews = self.review_set.all() # get all reviews for this product using the reverse relationship
        upVotes = reviews.filter(value='up').count() # filter reviews to get only upvotes
        totalVotes = reviews.count() # count total number of reviews for this product

        ratio = (upVotes / totalVotes) * 100 # calculate the vote ratio as a percentage of upvotes out of total votes
        self.vote_total = totalVotes # update the product's vote_total field with the total number of votes
        self.vote_ratio = ratio # update the product's vote_ratio field with the calculated ratio

        self.save() # save the product to update the vote_total and vote_ratio fields in the database
    

class Review(models.Model):
    VOTE_TYPE = (
        ('up', 'Upvote'),
        ('down', 'Downvote'),
    )
    # the user who wrote the review one to many relationship: 
    # one user can write many reviews, but each review has only one owner
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE
    )
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=200, choices=VOTE_TYPE)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    
    class Meta: # Meta class to enforce one review per user per product
        unique_together = [['owner', 'product']]  # one review per user per product

    def __str__(self):
        return self.value
    

"""
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
"""













