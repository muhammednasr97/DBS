from django.db import models


class Technical_Specs(models.Model):
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class General_Specs(models.Model):
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Technical_Report(models.Model):
    code = models.CharField(max_length=10, default='654')
    version = models.PositiveIntegerField()
    equipment_name = models.CharField(max_length=50, default='654')
    purpose = models.TextField(default='654')
    speciality = models.CharField(max_length=25, default='654')
    picture = models.ImageField(upload_to='media/', height_field=None, width_field=None, max_length=1000, default='654')
    general_specs = models.ManyToManyField(General_Specs, blank=True)
    technical_specs = models.ManyToManyField(Technical_Specs, blank=True)
    modification_date = models.CharField(max_length=20)
    addition_date = models.CharField(max_length=20)
    technology_level = models.CharField(max_length=10)
    facility_level = models.CharField(max_length=10)

    def __str__(self):
        return self.equipment_name


class Technical_Report_Copy(models.Model):
    code = models.CharField(max_length=10, default='654')
    version = models.PositiveIntegerField()
    equipment_name = models.CharField(max_length=50, default='654')
    purpose = models.TextField(default='654')
    speciality = models.CharField(max_length=25, default='654')
    picture = models.ImageField(upload_to='media/', height_field=None, width_field=None, max_length=1000, default='654')
    general_specs = models.ManyToManyField(General_Specs, blank=True)
    technical_specs = models.ManyToManyField(Technical_Specs, blank=True)
    modification_date = models.CharField(max_length=20)
    addition_date = models.CharField(max_length=20)
    technology_level = models.CharField(max_length=10)
    facility_level = models.CharField(max_length=10)

    def __str__(self):
        return self.equipment_name