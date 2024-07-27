from django.urls import path
from .views import (
    GetListingsAPIView,
    ListingCreateAPIView,
    ListingDetailAPIView,
    ListingSearchAPIView
)

urlpatterns = [
    # Listing endpoints
    path('listings/', GetListingsAPIView.as_view(), name='get-listings'),
    path('shops/<int:shopId>/listings/', ListingCreateAPIView.as_view(), name='listing-list-create'),
    path('listings/<int:pk>/', ListingDetailAPIView.as_view(), name='listing-detail-id'),  # GET, PUT, DELETE for specific listing
    path('listings/search/', ListingSearchAPIView.as_view(), name='listing-search'),
]
