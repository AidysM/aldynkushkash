from rest_framework import serializers

from main.models import AK, Comment

class AKSerializer(serializers.ModelSerializer):
    class Meta:
        model = AK
        fields = ('id', 'title', 'content', 'price', 'created_at')

class AKDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = AK
        fields = ('id', 'title', 'content', 'price', 'created_at', 'contacts', 'image')

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('ak', 'author', 'content', 'created_at')

