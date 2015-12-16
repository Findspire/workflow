# -*- coding: utf-8 -*-
from rest_framework import serializers
from workflow.apps.workflow.models import Comment, Item, Workflow, Project


class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='person.user.username', read_only=True)

    class Meta:
        model = Comment
        fields = ('username', 'date', 'text')


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item


class WorkflowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workflow


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
