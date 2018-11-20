from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager

from django.contrib import messages

from tinymce import HTMLField
# Create your models here.

# To retrieve all post with published status
class PublishedManager(models.Manager):
	def get_queryset(self):
		return super(PublishedManager, self).get_queryset().filter(status='published')


#class PostPicture(models.Model):
 #   picture =           models.ImageField(upload_to='blog/post_pics', blank=True)
 #   postid =            models.ForeignKey('Post', on_delete=models.CASCADE)

class Category(models.Model):
	CATEGORIES_CHOICE = (
			('world', 'World'), 
			('technology', 'Technology'),
			('culture', 'Culture'),
			('design', 'Design'),
			('business', 'Business'),
			('politic', 'Politic'),
			('opinion', "Opinion"),
			('health', 'Health'),
			('travel', 'Travel')

	)
	name = models.CharField(max_length =10, choices=CATEGORIES_CHOICE, default = 'world')

	def __str__(self):
		return self.name


class Post(models.Model):
	STATUS_CHOICES = (
		('draft', 'Draft'), 
		('published', 'Publishes')
	)
	
	title = models.CharField(max_length = 250)
	slug = models.CharField(max_length = 250, unique_for_date = 'publish')
	author = models.ForeignKey(User, related_name= 'blog_post', on_delete=models.CASCADE)
	body = HTMLField('Content')
	publish = models.DateTimeField(default = timezone.now)
	created = models.DateTimeField(auto_now_add= True)
	publish = models.DateTimeField(auto_now = True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
	category = models.ForeignKey(Category, related_name= 'category', on_delete=models.CASCADE,)
	tags = TaggableManager(blank=True)
	#PostPicture = None

	image = models.ImageField(upload_to='posts/%Y/%m/%d/', blank=False)

	objects = models.Manager() # The default manager
	published = PublishedManager() # The Dehl-specific manager
	class Meta:
		ordering = ('-publish',)


	def __str__(self):
		return self.title



	def get_absolute_url(self):
		return reverse('Post:Post_detail', args=[self.publish.year,
												 self.publish.strftime('%m'),
												 self.publish.strftime('%d'),
												 self.slug
			])


class Comment(models.Model): 
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comments')
    name = models.CharField(max_length=80) 
    email = models.EmailField() 
    body = HTMLField('Content')
    created = models.DateTimeField(auto_now_add=True) 
    updated = models.DateTimeField(auto_now=True) 
    active = models.BooleanField(default=True) 
 
    class Meta: 
        ordering = ('created',) 
 
    def __str__(self): 
        return 'Comment by {} on {}'.format(self.name, self.post) 