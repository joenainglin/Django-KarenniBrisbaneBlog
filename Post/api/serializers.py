from rest_framework import serializers
from rest_framework.exceptions import ParseError

from ..models import *

from taggit_serializer.serializers import (TagListSerializerField,
                                           TaggitSerializer)



class SubjectSerializer(serializers.ModelSerializer):


	tags = TagListSerializerField()
	class Meta:
		model = Post
		fields = ('title', 'category', 'tags')
		#fields = ('title', 'body', 'status', 'category', 'tags', 'image')
		



class SubjectDetailView(serializers.ModelSerializer):
    modules = SubjectSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ('title', 'category', 'tags', 'image')