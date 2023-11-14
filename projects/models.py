from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=255)
    floor_number = models.PositiveIntegerField()
    apartment_number = models.PositiveIntegerField()
    address = models.CharField(max_length=255)
    document = models.FileField(
        upload_to='project_documents/', blank=True, null=True)
    # You can add more fields as required
    # Adding Jalali Date fields

    def __str__(self):
        return self.name
