from django.db import models


class Currency(models.Model):
    USD = 'USD'
    EUR = 'EUR'
    AED = 'AED'

    CURRENCY_CHOICES = [
        (USD, 'US Dollars'),
        (EUR, 'Euro'),
        (AED, 'Dirham of Emirates')
    ]

    code = models.CharField(
        max_length=3, choices=CURRENCY_CHOICES, unique=True, primary_key=True)
    name = models.CharField(max_length=50)
    symbol = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.code})"


class Project(models.Model):
    name = models.CharField(max_length=100)
    proforma_num_reg = models.IntegerField(primary_key=True)
    proforma_name = models.CharField(max_length=50)
    price = models.PositiveIntegerField()
    weight = models.PositiveIntegerField()
    currency = models.ForeignKey(
        Currency, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return str(self.proforma_num_reg)


class Document(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    document = models.FileField(upload_to='documents/', blank=True, null=True)
