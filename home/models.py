from django.db import models
from django.conf import settings

class Property(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    LABEL_CHOICES = [
        ('land_to_sell', 'Land to Sell'),
        ('short_let', 'Short Let'),
        ('long_let', 'Long Let'),
        ('building_to_sell', 'Building to Sell'),
    ]

    title = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    zip_code = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    label = models.CharField(max_length=50, choices=LABEL_CHOICES, blank=True, null=True)
    size = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Size in square meters, for example
    land_area = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Land area in square meters
    property_id = models.CharField(max_length=50, unique=True, blank=True, null=True)  # Unique property ID
    rooms = models.PositiveIntegerField(blank=True, null=True)
    bedrooms = models.PositiveIntegerField(blank=True, null=True)
    bathrooms = models.PositiveIntegerField(blank=True, null=True)
    year_built = models.PositiveIntegerField(blank=True, null=True)  # Year built
    video_url = models.URLField(blank=True, null=True)  # Optional video tour link

    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    agent = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='properties'
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title if self.title else "Untitled Property"
    
    
class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='property_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.property.title}"
