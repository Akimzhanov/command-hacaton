from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.decorators import action
from rest_framework import filters
from rest_framework.generics import ListAPIView

from django_filters import rest_framework as rest_filter
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie

from .serializers import (
    LaptopListSerialiers,
    LaptopSerializer,
    CategorySerializer,
    RatingSerializer,
    LikeSerializer,
    LikedLaptopSerializer
)
from .models import Laptop, Category, Rating, Like


class LaptopViewSet(ModelViewSet):
    
    queryset = Laptop.objects.all()
    serializer_class = LaptopListSerialiers
    filter_backends = [filters.SearchFilter,
    rest_filter.DjangoFilterBackend,
    filters.OrderingFilter]
    search_fields = ['title','price', 'user__username']
    
    ordering_fields = ['created_at']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        print(serializer)

    @method_decorator(cache_page(60*60*2))
    @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.action == 'list':
            return LaptopListSerialiers
        return LaptopSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def get_permissions(self):
        if self.action in ['create', 'destroy', 'update', 'partial_update']:
            self.permission_classes = [IsAdminUser]
        if self.action in ['list', 'retrive']:
            self.permission_classes = [AllowAny]
        if self.action in ['set_rating', 'like']:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views_count += 1
        instance.save()
        return super().retrieve(request, *args, **kwargs)
    
    @action(methods=['POST', 'PATCH'], detail=True, url_path='set_rating')
    def set_rating(self, request, pk=None):
        data = request.data.copy()
        data['laptop'] = pk
        serializer = RatingSerializer(data=data, context={'request': request})
        rate = Rating.objects.filter(
            user=request.user,
            laptop=pk
        ).first()
        if serializer.is_valid(raise_exception=True):
            if rate and request.method == 'POST':
                return Response(
                    {'detail': 'Rating object exists. Use PATCH method'}
                )
            elif rate and request.method == 'PATCH':
                serializer.update(rate, serializer.validated_data)
                return Response('Updated')
            elif request.method == 'POST':
                serializer.create(serializer.validated_data)
                return Response(serializer.data)
            else:
                return Response({'detail': 'Rating object does not exist. Use POST method'})

    @action(detail=True, methods=['POST', 'DELETE'])
    def like(self, request, pk=None):
        laptop = self.get_object()
        serializer = LikeSerializer(data=request.data, context={
            'request': request,
            'laptop': laptop
        })
        if serializer.is_valid(raise_exception=True):
            if request.method == 'POST':
                serializer.save(user=request.user)
                return Response('Liked!')
            if request.method == 'DELETE':
                serializer.unlike()
                return Response('Unliked!')

   

class LikedLaptoptView(ListAPIView):
    serializer_class = LikedLaptopSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Like.objects.filter(user=user)

        


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer