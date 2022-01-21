from django.urls import path
from app import views

urlpatterns = [
    # 検索ページ
    path("", views.IndexView.as_view(), name="index"),
    # 書籍詳細ページ
    path("detail/<str:isbn>", views.DetailView.as_view(), name="detail"),
]
