from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from core.models import CustomUser, Books, Reviews


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the users object"""
    class Meta:
        model = get_user_model()
        fields = ('username', 'password')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication object"""
    username = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate and Authenticate the user"""
        username = attrs.get('username')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=username,
            password=password
        )

        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authentication')
        attrs['user'] = user
        return attrs


class BooksListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = ('id', 'title', 'author', 'genre')
        read_only_fields = ('id',)


class ReviewsSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    book = serializers.PrimaryKeyRelatedField(queryset=Books.objects.all())
    # user = UserSerializer(many=True, read_only=True)
    # book = BooksListSerializer(many=True, read_only=True)

    class Meta:
        model = Reviews
        fields = ('id', 'user', 'book', 'rating')
        read_only_fields = ('id',)
