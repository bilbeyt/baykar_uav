from django.db import models


class AircraftPartName(models.TextChoices):
    WING = "Wing"
    FUSELAGE = "Fuselage"
    TAIL = "Tail"
    AVIONICS = "Avionics"


class AircraftModel(models.TextChoices):
    TB2 = "TB2"
    TB3 = "TB3"
    AKINCI = "AKINCI"
    KIZILELMA = "KIZILELMA"


class Aircraft(models.Model):
    model = models.CharField(choices=AircraftModel, max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Aircraft {self.model} #{self.id}"


class AircraftPart(models.Model):
    name = models.CharField(choices=AircraftPartName, max_length=20)
    model = models.CharField(choices=AircraftModel, max_length=20)
    aircraft = models.ForeignKey(Aircraft, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} of {self.model}"

