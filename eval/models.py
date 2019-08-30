from django.db import models

# Create your models here.

class CarEval (models.Model):
	buying_price = models.CharField (max_length=100)
	maintenance = models.CharField (max_length=100)
	doors = models.CharField (max_length=100)
	persons = models.CharField (max_length=100)
	boot_space = models.CharField (max_length=100)
	safety = models.CharField (max_length=100)
	label = models.CharField (max_length=100)

	def __str__ (self):
		return self.label
