from rest_framework import viewsets, generics , status
from .models import (UserProfile, Category, Store,
                    Order, CourierProduct,Review)
from .serializers import (UserProfileListSerializer,UserProfileDetailSerializer, CategoryListSerializer,CategoryDetailSerializer,
                          StoreListSerializer,StoreDetailSerializer,
                          OrderSerializer, CourierProductSerializer, ReviewCreateSerializer, OrderStatusSerializer, StoreCreateSerializer,UserSerializer,LoginSerializer)
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import ReviewCreatePermission , OrdersPermission , CourierPermission , StoreCreatePermission
from .filters import StoreFilterSet
from rest_framework.filters import SearchFilter, OrderingFilter
from .paginations import StorePagination
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CustomLoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({"detail": "Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)

        user = serializer.validated_data
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class UserProfileListAPIView(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileListSerializer

class UserProfileDetailAPIView(generics.RetrieveAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileDetailSerializer

    def get_queryset(self):
        return UserProfile.objects.filter(id=self.request.user.id)

class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer

class CategoryDetailAPIView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer

class StoreListAPIView(generics.ListAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filters_class = StoreFilterSet
    search_fields = ['product_name']
    ordering_fields = ['created_at']
    pagination_class = StorePagination


class StoreDetailAPIView(generics.RetrieveAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreDetailSerializer

class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreCreateSerializer
    permission_classes = [StoreCreatePermission]

    def get_queryset(self):
        return Store.objects.filter(owner=self.request.user)

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [OrdersPermission]

    def get_queryset(self):
        return Order.objects.filter(client=self.request.user)

class OrderStatusListView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderStatusSerializer


class OrderStatusDetailView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderStatusSerializer


class CourierProductViewSet(viewsets.ModelViewSet):
    queryset = CourierProduct.objects.all()
    serializer_class = CourierProductSerializer
    permission_classes = [CourierPermission]

class ReviewCreateAPIView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewCreateSerializer
    permission_classes = [ReviewCreatePermission]


class ReviewEditAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewCreateSerializer

    def get_queryset(self):
        return Review.objects.filter(client=self.request.user)