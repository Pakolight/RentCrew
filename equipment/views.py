from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from equipment.models import CatalogItem
from equipment.serializers import CatalogItemSerializer

class CatalogItemCreateAPIView(CreateAPIView):
    """
    API endpoint for creating CatalogItem records.
    """
    queryset = CatalogItem.objects.all()
    serializer_class = CatalogItemSerializer
    permission_classes = [AllowAny]

class CatalogItemListCreateAPIView(ListCreateAPIView):
    """
    API endpoint for listing and creating CatalogItem records.
    """
    queryset = CatalogItem.objects.all()
    serializer_class = CatalogItemSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        """
        Filter queryset to only return CatalogItems belonging to the user's company.
        """
        return CatalogItem.objects.filter(company=self.request.user.company)

    def perform_create(self, serializer):
        """
        Set the company to the user's company when creating a new CatalogItem.
        """
        serializer.save(company=self.request.user.company)


class CatalogItemRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """
    API endpoint for retrieving, updating, and deleting a single CatalogItem record.
    """
    queryset = CatalogItem.objects.all()
    serializer_class = CatalogItemSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        """
        Filter queryset to only return CatalogItems belonging to the user's company.
        """
        return CatalogItem.objects.filter(company=self.request.user.company)
