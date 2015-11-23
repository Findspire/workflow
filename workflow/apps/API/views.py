# -*- coding: utf-8 -*-
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from workflow.apps.API import serializers
from workflow.apps.workflow.models import Item, Comment


class CommentList(APIView):
    """
    Display comment list
    """
    def get(self, request, item_pk, format=None):

        """
        Display comment list of selected item
        ---
        response_serializers: serializers.CommentSerializer
        """
        comments = Comment.objects.filter(item__pk=item_pk)
        serializer = serializers.CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


