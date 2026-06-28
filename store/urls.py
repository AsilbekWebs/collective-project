from django.urls import path
from .views import *

urlpatterns = [
    path('', store, name='store'),
    path('search/', search, name="search"),
    path('like/<int:product_id>/', LikeProductView.as_view(), name='like_product'),
    path('comment/<int:product_id>/', AddCommentView.as_view(), name='add_comment'),
    path('edit/<int:product_id>/', EditProductView.as_view(), name='edit_product'),
    path('delete/<int:product_id>/', DeleteProductView.as_view(), name='delete_product'),
    path('<slug:category_slug>/', store, name="products_by_category"),
    path('<slug:category_slug>/<slug:product_slug>/', product_detail, name="product_detail"),
]