from django.urls import path
from .views import (
    ShopListCreateAPIView,
    ShopDetailAPIView,
    ListingListCreateAPIView,
    ListingDetailAPIView,
    ShopDashboardAPIView,
    ListingSearchAPIView
)

urlpatterns = [
    # Shop endpoints
    path('shops/', ShopListCreateAPIView.as_view(), name='shop-list-create'),
    path('shops/<int:pk>/', ShopDetailAPIView.as_view(), name='shop-detail'),
    path('shops/<int:pk>/dashboard/', ShopDashboardAPIView.as_view(), name='shop-dashboard'),

    # Listing endpoints
    path('shops/<int:shopId>/listings/', ListingListCreateAPIView.as_view(), name='listing-list-create'),
    path('listings/<int:pk>/', ListingDetailAPIView.as_view(), name='listing-detail-id'),  # GET, PUT, DELETE for specific listing
    path('listings/search/', ListingSearchAPIView.as_view(), name='listing-search'),
]
