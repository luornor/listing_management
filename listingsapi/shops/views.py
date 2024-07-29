from rest_framework import generics, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Shop, Listing
from .serializers import ShopSerializer,ListingSerializer


class GetListingsAPIView(generics.ListAPIView):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
class ShopListingAPIView(generics.ListCreateAPIView):
    serializer_class = ListingSerializer

    def get_queryset(self):
        shop_id = self.kwargs.get('pk')
        return Listing.objects.filter(shop_id=shop_id)

    def post(self, request, *args, **kwargs):
        shop_id = self.kwargs.get('pk')
        try:
            shop = Shop.objects.get(id=shop_id)
        except Shop.DoesNotExist:
            return Response({"error": "Shop not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(shop_id=shop)
            return Response(
                {"message": "Listing created successfully", "data": serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ListingDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ListingSearchAPIView(generics.ListAPIView):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['price']
    search_fields = ['title', 'description']

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return self.get_paginated_response(serializer.data)