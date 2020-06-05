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


class Equipment(models.Model):
    code = models.CharField(max_length=10, primary_key=True)
    equipment_name = models.CharField(max_length=50)
    purpose = models.TextField()
    speciality = models.CharField(max_length=25)
    picture = models.ImageField(upload_to='media/', max_length=1000)
    general_specs = models.ManyToManyField(General_Specs, blank=True)
    technical_specs = models.ManyToManyField(Technical_Specs, blank=True)


    def __str__(self):
        return self.equipment_name


class Technical_Report(models.Model):
    report_id = models.IntegerField(default=0, primary_key=True)
    equipment_name = models.ForeignKey(Equipment, on_delete=models.CASCADE, blank=True, null=True)
    modification_date = models.DateField(auto_now=False, auto_now_add=False)
    addition_date = models.DateField(auto_now=False, auto_now_add=False)
    technology_level = models.CharField(max_length=10)
    facility_level = models.CharField(max_length=10)

    def __str__(self):
        return str(self.equipment_name)
