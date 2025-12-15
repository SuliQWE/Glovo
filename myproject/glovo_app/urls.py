from django.urls import path, include
from rest_framework import routers
from .views import (UserProfileListAPIView, UserProfileDetailAPIView, CategoryListAPIView, CategoryDetailAPIView,
                    StoreListAPIView, StoreDetailAPIView, OrderViewSet, CourierProductViewSet
                    , ReviewCreateAPIView, ReviewEditAPIView, OrderStatusListView, OrderStatusDetailView, StoreViewSet,RegisterView,CustomLoginView,LogoutView)

router = routers.SimpleRouter()
router.register('status_create', StoreViewSet)
router.register('orders', OrderViewSet)
router.register('courier_products', CourierProductViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register_list'),
    path('login/', CustomLoginView.as_view(), name='login_list'),
    path('logout/', LogoutView.as_view(), name='logout_list'),
    path('user/', UserProfileListAPIView.as_view(), name='user-profile-list'),
    path('user/<int:pk>/', UserProfileDetailAPIView.as_view(), name='user-profile-detail'),
    path('category/', CategoryListAPIView.as_view(), name='category-list'),
    path('category/<int:pk>/', CategoryDetailAPIView.as_view(), name='category-detail'),
    path('store/', StoreListAPIView.as_view(), name='store-list'),
    path('store/<int:pk>/', StoreDetailAPIView.as_view(), name='store-detail'),
    path('review/', ReviewCreateAPIView.as_view(), name='review-create'),
    path('review/<int:pk>/', ReviewEditAPIView.as_view(), name='review-edit'),
    path('order_status/', OrderStatusListView.as_view(), name='order-list'),
    path('order_status/<int:pk>/', OrderStatusDetailView.as_view(), name='order-detail'),
]