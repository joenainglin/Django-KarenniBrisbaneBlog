from rest_framework import generics
from ..models import *
from .serializers import SubjectSerializer

class SubjectListView(generics.ListAPIView):
	# queryset: The base QuerySet to use to retrieve objects
    queryset = Post.objects.all()

    #serializer_class: The class to serialize objects
    serializer_class = SubjectSerializer

class SubjectDetailView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = SubjectSerializer