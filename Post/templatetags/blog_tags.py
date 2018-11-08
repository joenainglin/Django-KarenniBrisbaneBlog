from django import template
from ..models import Post
from django.utils.safestring import mark_safe
import markdown
from django.db.models import Count

register = template.Library()

@register.simple_tag
def total_posts():
    return Post.published.count()


@register.simple_tag
def category():
    return Post.filter.category()


@register.inclusion_tag('Post/Posts/HomeLatestPostList.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[1:4]
    return {'latest_posts': latest_posts}


@register.inclusion_tag('Post/Posts/HomeMainPost.html')
def show_latest_posts_for_main():
    Homelatest_posts = Post.published.order_by('-publish')[0]
    return {'Homelatest_posts': Homelatest_posts}



@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(
               total_comments=Count('comments')
           ).order_by('-total_comments')[:4]



@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))