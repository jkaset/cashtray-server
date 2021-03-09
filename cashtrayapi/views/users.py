from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from cashtrayapi.models import Comment, Nonsmoker, Reward
from datetime import date
from datetime import datetime
from django.contrib.auth.models import User

class Users(ViewSet):
    """Users"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for single User
        Returns:
            Response -- JSON serialized User instance
        """
        if pk == None:
            cashtray_user = Nonsmoker.objects.get(user=request.auth.user)

        else:
            cashtray_user = Nonsmoker.objects.get(pk=pk)

        serializer = NonsmokerSerializer(
            cashtray_user, context={'request': request})
        return Response(serializer.data)


    def list(self, request):
        """Handle GET requests to /users resource
        Returns:
            Response -- JSON serialized list of Users
        """
        # Get all users from the database
        cashtray_user = Nonsmoker.objects.all()

        
        serializer = NonsmokerSerializer(
        cashtray_user, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        # Uses the token passed in the `Authorization` header
        cashtray_user = Nonsmoker.objects.get(user=request.auth.user)

        nonsmoker = Nonsmoker()
        nonsmoker.quit_date = request.data["quit_date"]
        nonsmoker.cigs_per_day = request.data["cigs_per_day"]
        nonsmoker.price_per_pack = request.data["price_per_pack"]
        nonsmoker.cigs_per_pack = request.data["cigs_per_pack"]
        nonsmoker.start_smoking_year = request.data["start_smoking_year"]
        try:
            nonsmoker.save()
            serializer = NonsmokerSerializer(nonsmoker, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single game
        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            nonsmoker = Nonsmoker.objects.get(user=request.auth.user)
            nonsmoker.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Nonsmoker.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None):
        user = Nonsmoker.objects.get(user=request.auth.user)

        nonsmoker = Nonsmoker()
        nonsmoker.quit_date = request.data["quit_date"]
        nonsmoker.cigs_per_day = request.data["cigs_per_day"]
        nonsmoker.price_per_pack = request.data["price_per_pack"]
        nonsmoker.cigs_per_pack = request.data["cigs_per_pack"]
        nonsmoker.start_smoking_year = request.data["start_smoking_year"]

        nonsmoker.save()
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, pk=None):
        user = Nonsmoker.objects.get(pk=pk)
        user.quit_date = request.data['quit_date']
        user.save()
        
        return Response({}, status=status.HTTP_204_NO_CONTENT)


class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for Users
    Arguments:
        serializer type
    """
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'is_staff', 'username')

class NonsmokerSerializer(serializers.ModelSerializer):
    """JSON serializer for Nonsmokers
    Arguments:
        serializer type
    """
    user = UserSerializer(many=False)


    class Meta:
        model = Nonsmoker
        fields = ('id', 'quit_date', 'cigs_per_day', 'price_per_pack', 'cigs_per_pack', 'start_smoking_year')
        depth = 1
