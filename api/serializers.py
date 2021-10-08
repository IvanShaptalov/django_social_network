from rest_framework import serializers
from social_network.models import LikeReaction, PostUser, Post


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostUser
        fields = ('username',)
        depth = 0


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer()

    class Meta:
        model = Post
        fields = ('author', 'title')
        depth = 0


class ReactionSerializer(serializers.ModelSerializer):
    author = UserSerializer(required=False)
    post = PostSerializer()

    class Meta:
        model = LikeReaction
        fields = ('author', 'reacted', 'reaction', 'post')
        depth = 0
