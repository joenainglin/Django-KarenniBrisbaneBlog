from django.urls import path
from . import views

app_name = 'Post'

urlpatterns = [
    path('Post/',views.SubjectListView.as_view(),name='subject_list'),

    path('Post/<pk>/',views.SubjectDetailView.as_view(),name='subject_detail'),
]