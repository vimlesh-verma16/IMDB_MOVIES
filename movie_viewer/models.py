
from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=255)
    original_title = models.CharField(max_length=255, null=True, blank=True)
    release_date = models.DateField(null=True, blank=True)
    overview = models.TextField(null=True, blank=True)
    original_language = models.CharField(max_length=10)
    language = models.CharField(max_length=50)
    runtime = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=20)
    budget = models.BigIntegerField(null=False,default= -1)
    revenue = models.BigIntegerField(null=True, blank=True)
    vote_average = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    vote_count = models.IntegerField(null=True, blank=True)
    homepage = models.URLField(null=True, blank=True)
    production_company_id = models.IntegerField(null=True, blank=True)
    genre_id = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ['release_date']

    def __str__(self):
        return self.title
