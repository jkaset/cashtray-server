from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from cashtrayapi.models import Comment, Nonsmoker
from datetime import date

class Comments(ViewSet):
    def list(self, request):

        comments=Comment.objects.all()
        user = Nonsmoker.objects.get(user=request.auth.user)

        # Set custom property, `my_comment` to True
        # if the logged in user is the author of the comment
        for comment in comments:
            if user == comment.author:
                    comment.my_comment=True
            else:
                comment.my_comment=False

        serializer = CommentSerializer(comments, many=True, context= {'request': request})
        return Response(serializer.data)
    
    def create(self, request):
       
        commenter= Nonsmoker.objects.get(user=request.auth.user)
        recipient= Nonsmoker.objects.get(pk=request.data["nonsmoker_id"])


        comment=Comment()
        comment.recipient=recipient
        comment.commenter=commenter
        comment.comment=request.data["comment"]
        comment.created_on= date.today()

        try:
            comment.save()
            serializer=CommentSerializer(comment, context= {'request': request} )
            return Response(serializer.data)

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):

        try:
            comment = Comment.objects.get(pk=pk)
            user = Nonsmoker.objects.get(user=request.auth.user)

            # Set custom property, `my_comment` to True
            # if the logged in user is the author of the comment
            if user == comment.commenter:
                comment.my_comment=True
            else:
                comment.my_comment=False

            serializer = CommentSerializer(comment, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def destroy(self, request, pk=None):

        try:
            comment = Comment.objects.get(pk=pk)
            comment.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Comment.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Comment
        fields=('id','recipient', 'commenter', 'comment', 'created_on', 'my_comment')
        depth=2