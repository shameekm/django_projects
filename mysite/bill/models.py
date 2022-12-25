from django.db import models

class Reciept(models.Model):
    store_name = models.CharField(max_length=200)
    total_before_tax = models.DecimalField(max_digits=19, decimal_places=10, null=True)
    tax = models.DecimalField(max_digits=19, decimal_places=10, null=True)
    tip = models.DecimalField(max_digits=19, decimal_places=10, null=True)
    total = models.DecimalField(max_digits=19, decimal_places=10, null=True)
    tax_percent = models.DecimalField(max_digits=19, decimal_places=10, null=True)
    tip_percent = models.DecimalField(max_digits=19, decimal_places=10, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def get_tax_percent(self):
        return float(self.tax)/float(self.total_before_tax)

    @property
    def get_tip_percent(self):
        return float(self.tip)/float(self.total_before_tax+self.tax)

    @property
    def get_total(self):
        return float(self.tax) + float(self.tip) + float(self.total_before_tax)
    
    def save(self, *args, **kwargs):
        self.tax_percent = self.get_tax_percent
        self.tip_percent = self.get_tip_percent
        self.total = self.get_total
        super(Reciept, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.store_name

class Item(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    persons = models.ManyToManyField('Person', through='Split')

    def __str__(self):
        return self.name

class Person(models.Model):
    name = models.CharField(max_length=200)
    balance = models.DecimalField(max_digits=7, decimal_places=3, null=True)
    reciept = models.ForeignKey(Reciept, on_delete=models.CASCADE)
    items = models.ManyToManyField('Item', through='Split')
    
    @property
    def get_balance(self):
        items = Item.objects.filter(persons=self.id)
        add_price = 0
        if len(items) > 0:
            for item in items:
                persons = item.persons.values_list('name', flat = True)
                if len(persons) > 0:
                    add_price += (item.price*(1+self.reciept.tax_percent)*(1+self.reciept.tip_percent))/len(persons)
        return add_price

    def save(self, *args, **kwargs):
        self.balance = self.get_balance
        super(Person, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class Split(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)