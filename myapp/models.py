from django.db import models
from django.utils import timezone

# Create your models here.
class User(models.Model):
	fname=models.CharField(max_length=100)
	lname=models.CharField(max_length=100)
	email=models.CharField(max_length=100)
	address=models.CharField(max_length=100)
	mobile=models.IntegerField(blank=False)
	password=models.CharField(max_length=100)
	profile_pic=models.ImageField(upload_to='profile_pic/')
	usertype=models.CharField(max_length=100,default='patient')
	

	def __str__(self):
		return self.fname +'= '+ self.lname

class Contact(models.Model):
	name=models.CharField(max_length=100)
	email=models.CharField(max_length=100)
	subject=models.CharField(max_length=100)
	message=models.TextField()


	def __str__(self):
		return self.name 
class Doctor_profile(models.Model):
	doctor=models.ForeignKey(User,on_delete=models.CASCADE)
	doctor_degree=models.CharField(max_length=100)
	doctor_speciality=models.CharField(max_length=100)
	doctor_start_time=models.CharField(max_length=100)
	doctor_end_time=models.CharField(max_length=100)
	doctor_fees=models.PositiveSmallIntegerField()

	def __str__(self):
		return self.doctor.fname+ '=' +self.doctor_degree

class Appointment(models.Model):
	patient=models.ForeignKey(User,on_delete=models.CASCADE)
	doctor=models.ForeignKey(Doctor_profile,on_delete=models.CASCADE)
	date=models.DateTimeField(default=timezone.now)
	time=models.CharField(max_length=100)
	discrpiton=models.TextField()
	fees_status=models.CharField(max_length=100,default='pending')
	status=models.CharField(max_length=100,default='pending')
	prescription=models.TextField(default='not given yet')
	

	def __str__(self):
		return self.patient.fname

class cancelappointmentaptient(models.Model):
	appointments=models.ForeignKey(Appointment,on_delete=models.CASCADE)
	cancel_issue=models.CharField(max_length=100)

	def __str__(self):
		return self.appointments.patient.fname+ '=' +self.appointments.doctor.doctor.fname

class doctorappointmentaptient(models.Model):
	appointments=models.ForeignKey(Appointment,on_delete=models.CASCADE)
	doctor_issue=models.CharField(max_length=100)

	def __str__(self):
		return self.appointments.patient.fname+ '=' +self.appointments.doctor.doctor.fname

class Transaction(models.Model):
    made_by = models.ForeignKey(User, related_name='transactions', 
                                on_delete=models.CASCADE)
    made_on = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()
    order_id = models.CharField(unique=True, max_length=100, null=True, blank=True)
    checksum = models.CharField(max_length=100, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.order_id is None and self.made_on and self.id:
            self.order_id = self.made_on.strftime('PAY2ME%Y%m%dODR') + str(self.id)
        return super().save(*args, **kwargs)
class HealthProfile(models.Model):
	patient=models.ForeignKey(User,on_delete=models.CASCADE)
	blood_group=models.CharField(max_length=100)
	weights=models.CharField(max_length=100)
	blood_pressue=models.BooleanField(default=False)
	diabetes=models.BooleanField(default=False)

	def __str__(self):
		return self.patient.fname