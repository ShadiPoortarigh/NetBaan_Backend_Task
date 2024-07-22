from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('login/', views.CreateTokenView.as_view(), name='login'),
    path('books/list/', views.BookListViewSet.as_view(), name='books'),

    path('suggest/', views.ReviewsGenericAPIView.as_view(), name='suggestion'),
    path('update/<str:title>/', views.ReviewsRetrieveUpdateAPIView.as_view(), name='update'),
]

