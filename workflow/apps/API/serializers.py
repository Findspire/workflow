# -*- coding: utf-8 -*-
from rest_framework import serializers
from workflow.apps.team.models import Person, Team
from workflow.apps.workflow.models import Comment, Item, Workflow, Project, ItemCategory


class PersonSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Person


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team


class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='person.user.username', read_only=True)

    class Meta:
        model = Comment


class WorkflowSerializer(serializers.ModelSerializer):
    success_percent = serializers.FloatField(source='get_success_percent')

    class Meta:
        model = Workflow


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project


class ItemCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemCategory


class ItemSerializer(serializers.ModelSerializer):
    category = ItemCategorySerializer()

    class Meta:
        model = Item