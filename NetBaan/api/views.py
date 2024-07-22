from rest_framework import generics, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.response import Response
from . import serializers

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core import models


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = serializers.UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user"""
    serializer_class = serializers.AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class BookListViewSet(generics.ListAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    serializer_class = serializers.BooksListSerializer

    def get_queryset(self):
        genre = self.request.query_params.get('genre')
        queryset = models.Books.objects.all()
        if genre:
            queryset = queryset.filter(genre=genre)
        return queryset


class ReviewsGenericAPIView(generics.GenericAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        books = models.Reviews.objects.filter(user=self.request.user)
        if not books.exists():
            return Response({'Warning': 'There is not enough data about you'})
        else:
            suggestion = models.Reviews.objects.filter(rating__gte=request.data.get('rating'))
            if suggestion:
                serializer = serializers.ReviewsSerializer(suggestion, many=True)
                return Response(serializer.data)


class ReviewsRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = models.Reviews.objects.all()
    serializer_class = serializers.ReviewsSerializer

    def partial_update(self, request, *args, **kwargs):
        title = self.kwargs.get('title')
        book = models.Books.objects.get(title=title)
        review_obj = models.Reviews.objects.get(book=book)
        print(review_obj)
        if review_obj:
            serializer = serializers.ReviewsSerializer(review_obj, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)


