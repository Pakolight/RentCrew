from django.db import models
from django.utils import timezone

class Reservation(models.Model):
    """
    Model for equipment reservations.
    Tracks the reservation of items (catalog items, kits, or assets) for projects.
    """
    ITEM_TYPE_CHOICES = [
        ('catalog', 'Catalog Item'),
        ('kit', 'Kit'),
        ('asset', 'Asset'),
    ]

    STATUS_CHOICES = [
        ('hold', 'Hold'),
        ('reserved', 'Reserved'),
        ('checkedOut', 'Checked Out'),
        ('returned', 'Returned'),
        ('canceled', 'Canceled'),
    ]

    # Reference to Project model from projects app
    projectId = models.ForeignKey('projects.Project', on_delete=models.CASCADE, related_name='reservations')
    lineId = models.CharField(max_length=100)  # Reference to a line item in a quote or order
    itemType = models.CharField(max_length=10, choices=ITEM_TYPE_CHOICES)
    refId = models.IntegerField()  # ID of the referenced item (catalog item, kit, or asset)
    qty = models.PositiveIntegerField(default=1)
    dateFrom = models.DateTimeField()
    dateTo = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='hold')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Reservation {self.id} - {self.get_itemType_display()} - {self.get_status_display()}"

    class Meta:
        verbose_name_plural = "reservations"


class AvailabilityView(models.Model):
    """
    Virtual model for calculating availability based on time windows.
    This is a conceptual model and doesn't store data directly in the database.
    Availability is calculated as: availability - active reservations - subrents + returns
    """

    class Meta:
        managed = False  # This model won't create a database table
        verbose_name_plural = "availability views"

    @staticmethod
    def calculate_availability(item_type, item_id, date_from, date_to):
        """
        Calculate availability for a specific item in a given time window.

        Args:
            item_type (str): Type of item ('catalog', 'kit', 'asset')
            item_id (int): ID of the item
            date_from (datetime): Start date of the time window
            date_to (datetime): End date of the time window

        Returns:
            dict: Availability information for the specified time window
        """
        # This is a placeholder for the actual calculation logic
        # In a real implementation, this would query:
        # 1. Total inventory of the item
        # 2. Active reservations during the time window
        # 3. Subrents during the time window
        # 4. Expected returns during the time window

        # Example implementation (pseudocode):
        # total_inventory = get_total_inventory(item_type, item_id)
        # active_reservations = Reservation.objects.filter(
        #     itemType=item_type, 
        #     refId=item_id,
        #     status__in=['hold', 'reserved', 'checkedOut'],
        #     dateFrom__lt=date_to,
        #     dateTo__gt=date_from
        # ).aggregate(Sum('qty'))
        # subrents = SubRent.objects.filter(...)
        # returns = Return.objects.filter(...)
        # availability = total_inventory - active_reservations - subrents + returns

        return {
            'item_type': item_type,
            'item_id': item_id,
            'date_from': date_from,
            'date_to': date_to,
            'availability': 0,  # Placeholder value
            'calculation_time': timezone.now(),
        }
