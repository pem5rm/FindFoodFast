from django.db import models


class RestaurantManager(models.Model):
    question_text = models.CharField(max_length=200)
    city_text = models.CharField(max_length=200)
    state_text = models.CharField(max_length=200)


class RestaurantInfo(models.Model):
    manager = models.ForeignKey(RestaurantManager, on_delete=models.CASCADE)
    info_text = models.CharField(max_length=200)
