from django.contrib.auth import get_user_model
from django.http import HttpResponseNotAllowed, HttpResponse
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from api_v2.serializers import CommentSerializer
from webapp.models import Comment, Article


class CommentView(APIView):
    def get(self, request, pk=None, comment_pk=None, *args, **kwargs):
        if 'comment_pk' in self.kwargs:
            comment = get_object_or_404(Comment, pk=comment_pk, article=pk)
            serializer = CommentSerializer(comment)
            return Response(serializer.data)
        else:
            comments = Comment.objects.filter(article=pk)
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data)

    def post(self, request, pk, *args, **kwargs):
        article = get_object_or_404(Article, pk=pk)
        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        comment = serializer.save(article=article)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, pk, comment_pk, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=comment_pk, article=pk)
        serializer = CommentSerializer(data=request.data, instance=comment)
        if serializer.is_valid():
            comment = serializer.save()
            return Response(serializer.data)
        else:
            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, comment_pk, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=comment_pk, article=pk)
        comment.delete()
        return Response({"id": comment_pk}, status=status.HTTP_204_NO_CONTENT)


