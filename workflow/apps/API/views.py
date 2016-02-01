# -*- coding: utf-8 -*-
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.shortcuts import get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from workflow.apps.API import serializers
from workflow.apps.team.models import Person, Team
from workflow.apps.workflow.models import Item, Comment, Workflow, ItemModel, Project, ItemCategory
from workflow.apps.workflow.models import update_workflow_position, update_item_position, update_category_position


class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


class PersonList(APIView):
    """
    List all person
    """
    def get(self, request, format=None):
        """
        List all person
        ---
        response_serializer: serializers.PersonSerializer
        """
        person = Person.objects.all()
        serializer = serializers.PersonSerializer(person, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TeamList(APIView):
    """
    List all team
    """
    def get(self, request, format=None):
        """
        List all person
        ---
        response_serializer: serializers.TeamSerializer
        """
        teams = Team.objects.all()
        serializer = serializers.TeamSerializer(teams, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProjectList(APIView):
    """
    List all project or create new
    """
    def get(self, request, format=None):
        """
        List all project
        ---
        response_serializer: serializers.ProjectSerializer
        """
        projects = Project.objects.all()
        serializer = serializers.ProjectSerializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        """
        Create new project
        ---
        request_serializer: serializers.ProjectSerializer
        response_serializer: serializers.ProjectSerializer
        """
        serializer = serializers.ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WorkflowList(APIView):
    """
    List all workflow or create new
    """
    def get(self, request, format=None):
        """
        List all workflow
        ---
        response_serializer: serializers.WorkflowSerializer
        """
        workflows = Workflow.objects.all()
        serializer = serializers.WorkflowSerializer(workflows, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        """
        Create new workflow
        ---
        request_serializer: serializers.WorkflowSerializer
        response_serializer: serializers.WorkflowSerializer
        """
        serializer = serializer.WorkflowSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UsersWorkflowList(APIView):
    """
    Display workflow with selected filter
    """
    def get(self, request, person_pk, format=None):
        """
        Display workflow with selected filter
        ---
        response_serializer: serializers.WorkflowSerializer
        """
        person = get_object_or_404(Person, pk=person_pk)
        workflows = Workflow.objects.filter(archived=False)
        workflows_list = set()
        for workflow in workflows:
            if workflow.get_items('mine', person=person):
                workflows_list.add(workflow)
        serializer = serializers.WorkflowSerializer(workflows_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class WorkflowDetailsFilter(APIView):
    """
    Display workflow details from selecte filter
    """
    def get(self, request, display, person_pk, workflow_pk):
        """
        Display workflow details for selected person
        ---
        response_serializer: serializers.ItemSerializer
        """
        person = get_object_or_404(Person, pk=person_pk)
        workflow = get_object_or_404(Workflow, pk=workflow_pk)

        items = workflow.get_items('mine', person=person)
        serializer = serializers.ItemSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProjectWorkflowList(APIView):
    """
    List all workflow of selected project
    """
    def get(self, request, project_pk, format=None):
        """
        List all workflow of selected project
        ---
        response_serializer: serializers.WorkflowSerializer
        """
        project = get_object_or_404(Project, pk=project_pk)
        workflows = Workflow.objects.filter(project=project)
        serializer = serializers.WorkflowSerializer(workflows, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CommentList(APIView):
    """
    Display comment list or create new
    """
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get(self, request, item_pk, format=None):
        """
        Display comment list of selected item
        ---
        response_serializer: serializers.CommentSerializer
        """
        comments = Comment.objects.filter(item__pk=item_pk)
        serializer = serializers.CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, item_pk, format=None):
        """
        Create new comment for selected item
        ---
        request_serializer: serializers.CommentSerializer
        response_serializer: serializers.CommentSerializer
        """
        data = dict(request.data)
        data['item'] = item_pk
        data['person'] = int(request.data['person'])
        data['text'] = str(request.data['text'])
        serializer = serializers.CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, item_pk, format=None):
        """
        Delete selected comment
        ---
        request_serializer: serializers.CommentSerializer
        """
        comment = get_object_or_404(Comment, pk=item_pk)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ItemDetails(APIView):
    """
    Retrieve or update details of selected item
    """
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def patch(self, request, item_pk, format=None):
        """
        Update partial details of selected item
        ---
        request_serializer: serializers.ItemSerializer
        response_serializer: serializers.ItemSerializer
        """
        item = get_object_or_404(Item, pk=item_pk)
        serializer = serializers.ItemSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, item_pk, format=None):
        """
        Delete selected item
        """
        item = get_object_or_404(Item, pk=item_pk)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class WorkflowDetails(APIView):
    """
    Retrieve or update details of selected workflow
    """
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get(self, request, workflow_pk, format=None):
        """
        Retrieve details of selected workflow
        ---
        response_serializer: serializers.WorkflowSerializer
        """
        workflow = get_object_or_404(Workflow, pk=workflow_pk)
        serializer = serializers.WorkflowSerializer(workflow)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, workflow_pk, format=None):
        """
        Update informations of selected workflow
        ---
        request_serializer: serializers.WorkflowSerializer
        response_serializer: serializers.WorkflowSerializer
        """
        workflow = get_object_or_404(Workflow, pk=workflow_pk)
        serializer = serializers.WorkflowSerializer(workflow, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WorkflowDragPosition(APIView):
    """
    Update workflow position with drag and drop
    """
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self, request, workflow_pk, related_pk=None):
        """
        Update workflow position with drag and drop
        """
        workflow = get_object_or_404(Workflow, pk=workflow_pk)
        if related_pk is not None:
            related_item = Workflow.objects.get(pk=related_pk)
            update_workflow_position(workflow, related_item)
        else:
            update_workflow_position(workflow)
        return Response(status=status.HTTP_200_OK)


class ItemDragPosition(APIView):
    """
    Update item position with drag and drop
    """
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self, request, item_pk, related_pk=None):
        """
        Update item position with drag and drop
        """
        item = get_object_or_404(Item, pk=item_pk)
        if related_pk is not None:
            related_item = Item.objects.get(pk=related_pk)
            update_item_position(item, related_item)
        else:
            update_item_position(item)
        return Response(status=status.HTTP_200_OK)


class CategoryDragPosition(APIView):
    """
    Update category position with drag and drop
    """
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self, request, category_pk, related_pk=None):
        """
        Update category position with drag and drop
        """
        category = get_object_or_404(ItemCategory, pk=category_pk)
        workflow = category.workflow_set.all()[0]
        if related_pk is not None:
            related_item = ItemCategory.objects.get(pk=related_pk)
            update_category_position(workflow, category, related_item)
        else:
            update_category_position(workflow, category)
        return Response(status=status.HTTP_200_OK)