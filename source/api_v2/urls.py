from django.urls import path

from api_v2.views.article import ArticleView, get_token_view

app_name = 'v2'

urlpatterns = [
    path('articles/', ArticleView.as_view(), name='articles'),
    path('articles/<int:pk>/', ArticleView.as_view(), name='article'),
    path('get-csrf/', get_token_view, name='get-csrf'),
]