from django.urls import path

from api_v2.views.article import ArticleView, get_token_view
from api_v2.views.comment import CommentView

app_name = 'v2'

urlpatterns = [
    path('articles/', ArticleView.as_view(), name='articles'),
    path('articles/<int:pk>/', ArticleView.as_view(), name='article'),
    path('get-csrf/', get_token_view, name='get-csrf'),

    path('articles/<int:pk>/comments/', CommentView.as_view(), name='comments'),
    path('articles/<int:pk>/comments/<int:comment_pk>/', CommentView.as_view(), name='comment'),
]