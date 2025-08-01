
from django.db import models
from django.contrib.auth.models import User

class Company(models.Model):
    company_name = models.CharField(max_length=150)
    symbol = models.CharField(max_length=30)
    scripcode = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return f"{self.company_name} ({self.symbol})"

class WatchlistEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'company')

    def __str__(self):
        return f"{self.user.username} → {self.company.symbol}"
