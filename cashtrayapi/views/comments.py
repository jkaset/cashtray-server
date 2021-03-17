from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from cashtrayapi.models import Comment, Nonsmoker
from datetime import date
from django.contrib.auth.models import User

class Comments(ViewSet):
    def list(self, request):

        comments=Comment.objects.all()
        nonsmoker = Nonsmoker.objects.get(user=request.auth.user)

        recipient = self.request.query_params.get('recipient_id', None)
        if recipient is not None: 
            comments = comments.filter(recipient_id=recipient)

        for comment in comments:
            if nonsmoker == comment.commenter:
                comment.my_comment=True
            else:
                comment.my_comment=False

        serializer = CommentSerializer(comments, many=True, context= {'request': request})
        return Response(serializer.data)
    
    def create(self, request, pk=None):
        # recipient = Nonsmoker.objects.get(pk=pk)
        commenter= Nonsmoker.objects.get(user=request.auth.user)
        # recipient = self.request.query_params.get('recipient_id')
        
        # create a new Python instance of the Comment class with properties  REQUEST client 

        comment=Comment()
        comment.recipient_id=request.data["recipient_id"]
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

class CommentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']
        depth = 1



class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Comment
        fields=('id','recipient', 'commenter', 'comment', 'created_on', 'my_comment')
        depth=2