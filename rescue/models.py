from django.conf import settings
from django.db import models
from django.utils import timezone


class AnimalType(models.TextChoices):
    DOG = 'Dog', 'Dog'
    CAT = 'Cat', 'Cat'
    BIRD = 'Bird', 'Bird'
    OTHER = 'Other', 'Other'


class RescueStatus(models.TextChoices):
    PENDING = 'Pending', 'Pending'
    UNDER_RESCUE = 'Under Rescue', 'Under Rescue'
    RESCUED = 'Rescued', 'Rescued'
    CLOSED = 'Closed', 'Closed'


class AdoptionStatus(models.TextChoices):
    AVAILABLE = 'Available', 'Available'
    APPLICATION_PENDING = 'Application Pending', 'Application Pending'
    ADOPTED = 'Adopted', 'Adopted'


class Animal(models.Model):
    name = models.CharField(max_length=100)
    animal_type = models.CharField(max_length=50, choices=AnimalType.choices)
    age = models.PositiveIntegerField(default=0)
    gender = models.CharField(max_length=30, blank=True)
    location = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='animals/', blank=True, null=True)
    health_status = models.CharField(max_length=100, blank=True)
    adoption_status = models.CharField(
        max_length=30,
        choices=AdoptionStatus.choices,
        default=AdoptionStatus.AVAILABLE,
    )
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class RescueReport(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='rescue_reports')
    animal_name = models.CharField(max_length=100)
    animal_type = models.CharField(max_length=50, choices=AnimalType.choices)
    description = models.TextField()
    location = models.CharField(max_length=200)
    contact_number = models.CharField(max_length=30)
    image = models.ImageField(upload_to='rescue_reports/', blank=True, null=True)
    status = models.CharField(max_length=30, choices=RescueStatus.choices, default=RescueStatus.PENDING)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.animal_name} - {self.location}'


class AdoptionApplication(models.Model):
    class Status(models.TextChoices):
        PENDING = 'Pending', 'Pending'
        APPROVED = 'Approved', 'Approved'
        REJECTED = 'Rejected', 'Rejected'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='adoption_applications')
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name='adoption_applications')
    message = models.TextField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'animal'], name='unique_adoption_application'),
        ]
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username} - {self.animal.name}'


class LostFound(models.Model):
    class ReportType(models.TextChoices):
        LOST = 'Lost', 'Lost'
        FOUND = 'Found', 'Found'

    class Status(models.TextChoices):
        ACTIVE = 'Active', 'Active'
        RESOLVED = 'Resolved', 'Resolved'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='lost_found_reports')
    report_type = models.CharField(max_length=10, choices=ReportType.choices)
    animal_name = models.CharField(max_length=100)
    animal_type = models.CharField(max_length=50, choices=AnimalType.choices)
    description = models.TextField()
    location = models.CharField(max_length=200)
    date_lost_found = models.DateField()
    contact_number = models.CharField(max_length=30)
    image = models.ImageField(upload_to='lost_found/', blank=True, null=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.ACTIVE)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.report_type}: {self.animal_name}'


class VolunteerApplication(models.Model):
    class Status(models.TextChoices):
        PENDING = 'Pending', 'Pending'
        APPROVED = 'Approved', 'Approved'
        REJECTED = 'Rejected', 'Rejected'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='volunteer_applications')
    phone = models.CharField(max_length=30)
    availability = models.CharField(max_length=200)
    interests = models.CharField(max_length=200)
    experience = models.TextField(blank=True)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Volunteer application by {self.user.username}'