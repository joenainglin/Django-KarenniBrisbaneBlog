from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .models import *
from django.core.mail import send_mail
from .forms import * 
from taggit.models import Tag
from django.db.models import Count
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank

from django.shortcuts import redirect


from django.contrib import messages


from urllib import request
from django.core.files.base import ContentFile
from django.utils.text import slugify


# Create your views here.
def Post_list(request, tag_slug=None): 
    object_list = Post.published.all()
    
    tag = None 
 
    if tag_slug: 
        tag = get_object_or_404(Tag, slug=tag_slug) 
        object_list = object_list.filter(tags__in=[tag]) 
 
    paginator = Paginator(object_list, 4) # 3 posts in each page 
    page = request.GET.get('page') 
    try: 
        posts = paginator.page(page) 
    except PageNotAnInteger: 
        # If page is not an integer deliver the first page 
        posts = paginator.page(1) 
    except EmptyPage: 
        # If page is out of range deliver last page of results 
        posts = paginator.page(paginator.num_pages) 
    return render(request, 'Post/Posts/HomePopularPostList.html', {'page': page, 
                                                   'posts': posts, 
                                                   'tag': tag,
                                       
                                                  }) 

#class PostListView(ListView):
#	queryset = Post.published.all()
#	context_object_name = 'posts'
#	paginator_by = 3
#	template_name = 'Post/Posts/list.html'

def Post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                                   status='published',
                                   publish__year=year,
                                   publish__month=month,
                                   publish__day=day)

    # List of active comments for this post
    comments = post.comments.filter(active=True)
    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.name = request.user
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()
        new_comment = False

    # List of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags',
                                                                             '-publish')[:4]
    return render(request, 'Post/Posts/PostInDetail.html', {'post': post,
                                                     'comments': comments,
                                                     'comment_form': comment_form,
                                                     'similar_posts': similar_posts,
                                                     'new_comment': new_comment})


def Post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
 
    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                                          post.get_absolute_url())
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, 'admin@myblog.com',[cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'Post/Posts/SharePost.html', {'post': post,
                                                    'form': form,
                                                    'sent': sent})



def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector('title', 'body')
            search_query = SearchQuery(query)
            results = Post.objects.annotate(
                          search=search_vector,
                          rank=SearchRank(search_vector, search_query)
                      ).filter(search=search_query).order_by('-rank')
    return render(request,
                  'Post/Posts/Search.html',
                  {'form': form,
                   'query': query,
                   'results': results})
# SOME THING NOT RIGHT 
# ABLE TO SAVE 
# BUT THE SLUG AND IMG ISSUE


def post_new(request):

    if request.method == "POST":
        form = CreatePostForm(
                                    request.POST, request.FILES)

        if form.is_valid():
          cd = form.cleaned_data
          new_item = form.save(commit=False)
          # assign current user to the item
          new_item.user = request.user

          #tags = form.cleaned_data['tags']
          new_item.slug = new_item.title.replace(" ", "-")  
          new_item.author = request.user   

          #for tag in tags:
          #    new_item.tags.add(tag)
          new_item.save()
        
          messages.success(request, 'Post added successfully')
          return redirect( '/Post/')
          #form = CreatePostForm()
        else:
          messages.error(request, 'Error adding new post')
    else:
        form = CreatePostForm()
    return render(request, 'Post/Posts/CreatePost.html',{'form': form, } )






def post_edit(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == 'POST':
        
        post_form = EditPost( instance=request.user,
                                    data=request.POST,
                                    files=request.FILES)
        
        if post_form.is_valid():
            post = form.save(commit=False)
            post.save()
            messages.success(request, "Post Saved")
        

    else:
   
        post_form = EditPost(
                              instance=request.user,
                                    data=request.POST,
                                    files=request.FILES)
    return render(request,
                  'Post/Posts/PostEdit.html',
                  {'post_form': post_form,
                  'post':post})


def post_delete(request, slug):
    post = get_object_or_404(Post, slug= slug)
    UserPost = Post.objects.filter(author_id=request.user).order_by("-publish")
    post.delete()
    messages.success(request, "Successfully delete")
    #return redirect( '/accounts/dashboard.html')
    return render(request, 'accounts/dashboard.html', {'post':post, 'UserPost':UserPost})