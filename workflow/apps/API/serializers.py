# -*- coding: utf-8 -*-
from rest_framework import serializers
from workflow.apps.workflow.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='person.user.username', read_only=True)

    class Meta:
        model = Comment
        fields = ('username', 'date', 'text')