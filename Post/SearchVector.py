from django.contrib.postgres.search import SearchVector
from Post.models import Post

Post.objects.annotate(
    search=SearchVector('title', 'body'),
).filter(search='django')