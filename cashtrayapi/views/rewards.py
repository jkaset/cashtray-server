from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import serializers
from cashtrayapi.models import Comment, Nonsmoker, Reward
from django.contrib.auth.models import User

class Rewards(ViewSet):

    def list(self, request):
        """Handle GET requests to games resource
        Returns:
            Response -- JSON serialized list of games
        """
        # Get all post records from the database
        rewards = Reward.objects.get(user=request.auth.user)
        rewards = RewardSerializer(
          rewards, many=True, context={'request': request}
        )

        return Response(rewards.data)
       


    def retrieve(self, request, pk=None):
        """Handle GET requests for single reward
        Returns:
            Response -- JSON serialized game instance
        """
        try:
            # `pk` is a parameter to this function, and
            # Django parses it from the URL route parameter
            #   
            #
            # The `2` at the end of the route becomes `pk`
            reward = Reward.objects.get(pk=pk)
            serializer = RewardSerializer(reward, context={'request': request})
            return Response(serializer.data)
        except Reward.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        """Handle POST operations
        Returns:
            Response -- JSON serialized post instance
        """

        # Uses the token passed in the `Authorization` header
        nonsmoker = Nonsmoker.objects.get(user=request.auth.user)

        # Create a new Python instance of the Post class
        # and set its properties from what was sent in the
        # body of the request from the client.
        reward = Reward()
        reward.reward_name = request.data["reward_name"]
        reward.reward_cost = request.data["reward_cost"]
        reward.redeemed = request.data["redeemed"]
        reward.nonsmoker = nonsmoker
        

        # Try to save the new post to the database, then
        # serialize the post instance as JSON, and send the
        # JSON as a response to the client request
        try:
            reward.save()
            serializer = RewardSerializer(reward, context={'request': request})
            return Response(serializer.data)

        # If anything went wrong, catch the exception and
        # send a response with a 400 status code to tell the
        # client that something was wrong with its request data
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single game
        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            reward = Reward.objects.get(pk=pk)
            reward.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Reward.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def update(self, request, pk=None):
        """Handle PUT requests for a post
        Returns:
            Response -- Empty body with 204 status code
        """
        nonsmoker = Nonsmoker.objects.get(user=request.auth.user)

        # Do mostly the same thing as POST, but instead of
        # creating a new instance of Post, get the post record
        # from the database whose primary key is `pk`
        reward = Reward.objects.get(pk=pk)
        reward.reward_name = request.data["reward_name"]
        reward.reward_cost = request.data["reward_cost"]
        reward.redeemed = request.data["redeemed"]
        reward.nonsmoker = nonsmoker
        reward.save()

        # 204 status code means everything worked but the
        # server is not sending back any data in the response
        return Response({}, status=status.HTTP_204_NO_CONTENT)

class RewardSerializer(serializers.ModelSerializer):
    """JSON serializer for gamer's related Django user"""
    class Meta:
        model = Reward
        fields = ('reward_name', 'reward_cost', 'redeemed')
