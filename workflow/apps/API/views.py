# -*- coding: utf-8 -*-
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.shortcuts import get_object_or_404, redirect
from django.core.urlresolvers import reverse
from workflow.apps.API import serializers
from django.contrib.auth.models import User
from workflow.apps.workflow.models import Item, Comment, Workflow, ItemModel
from workflow.apps.workflow.models import update_workflow_position, update_item_position


class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


class CommentList(APIView):
    """
    Display comment list
    """
    def get(self, request, item_pk, format=None):
        """
        Display comment list of selected item
        ---
        response_serializer: serializers.CommentSerializer
        """
        comments = Comment.objects.filter(item__pk=item_pk)
        serializer = serializers.CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


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
        workflow = get_object_or_404(Workflow, pk=workflow_pk)
        if related_pk is not None:
            related_item = Workflow.objects.get(pk=related_pk)
            update_workflow_position(workflow, related_item)
        else:
            update_workflow_position(workflow)
        return Response(status=status.HTTP_200_OK)


class ItemDragPosition(APIView):
    """
    Update workflow position with drag and drop
    """
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self, request, item_pk, related_pk=None):
        item = get_object_or_404(Item, pk=item_pk)
        if related_pk is not None:
            related_item = Item.objects.get(pk=related_pk)
            update_item_position(item, related_item)
        else:
            update_item_position(item)
        return Response(status=status.HTTP_200_OK)