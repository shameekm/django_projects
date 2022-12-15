from django.db import models

class Reciept(models.Model):
    store_name = models.CharField(max_length=200)
    tax = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    tip = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    total = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    tax_percent = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    tip_percent = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    
    def __str__(self):
        return self.title

class Item(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    reciept = models.ForeignKey(Reciept, on_delete=models.CASCADE)
    persons = models.ManyToManyField('Person', through='Split')

    def __str__(self):
        return self.title

class Person(models.Model):
    name = models.CharField(max_length=200)
    balance = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    items = models.ManyToManyField('Item', through='Split')
    
    def __str__(self):
        return self.title

class Split(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title


sdfdsfdsfsdfdsf