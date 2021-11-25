from django.db import models

# this a model for the orders status 

class Order (models.Model):
    old_id = models.IntegerField()
    title = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    status = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "orders"