from django.db import models

# Create your models here.

class Current(models.Model):
    num = models.IntegerField()

class Card(models.Model):
    title = models.CharField(blank = True, null=True, max_length=100)
    txt = models.TextField()
    tags = models.CharField(max_length=100, blank=True, null=True, default="")
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("Card_detail", kwargs={"pk": self.pk})
