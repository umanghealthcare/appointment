from django.shortcuts import render,redirect
from . models import User,Contact,Doctor_profile,Appointment,cancelappointmentaptient,doctorappointmentaptient,Transaction,HealthProfile
from django.conf import settings
from django.core.mail import send_mail
import random
from django.http import JsonResponse
from django.conf import settings
from .models import Transaction
from .paytm import generate_checksum, verify_checksum
from django.views.decorators.csrf import csrf_exempt




# Create your views here.
def initiate_payment(request,pk):
	patient=Appointment.objects.get(pk=pk)
	user=User.objects.get(email=request.session['email'])
	try:
		amount = int(request.POST['amount'])
	except:
		return render(request, 'myappointment.html', context={'error': 'Wrong Accound Details or amount'})

	transaction = Transaction.objects.create(made_by=user, amount=amount)
	transaction.save()
	merchant_key = settings.PAYTM_SECRET_KEY

	params = (
		('MID', settings.PAYTM_MERCHANT_ID),
		('ORDER_ID', str(transaction.order_id)),
		('CUST_ID', str('usahu3589@gmail.com')),
		('TXN_AMOUNT', str(transaction.amount)),
		('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
		('WEBSITE', settings.PAYTM_WEBSITE),
		# ('EMAIL', request.user.email),
		# ('MOBILE_N0', '9911223388'),
		('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
		('CALLBACK_URL', 'http://127.0.0.1:8000/callback/'),
		# ('PAYMENT_MODE_ONLY', 'NO'),
	)

	paytm_params = dict(params)
	checksum = generate_checksum(paytm_params, merchant_key)

	transaction.checksum = checksum
	transaction.save()
	# patient=User.objects.get(email=request.session['email'])
	# appointments=Appointment.objects.filter(patient=patient)
	# for i in appointments:
	# 	i.fees_status='paid'
	# 	i.save()
	patient.fees_status="paid"
	patient.save()
	if patient.fees_status=="paid":
		try:

			user=patient.patient.email
			fname=patient.patient.fname
			lname=patient.patient.lname
			time=patient.time
			date=patient.date
			fees=patient.doctor.doctor_fees
			pdiscrpiton=patient.discrpiton
			de=patient.doctor.doctor.email
			dfname=patient.doctor.doctor.fname
			dlname=patient.doctor.doctor.lname
			dname=patient.doctor.doctor_speciality
			print(user)
			print(de)
			subject = 'Your appointments book  with  doctor '

			message = 'Appointments with  doctor '+str(dfname)+' '+str(dlname)+'\n Speciality In '+str(dname)+'\n At time '+str(time)+'\n '+"patient Details:"+str(fname)+' '+str(lname)+''+'\n You have paid Rs'+ str(fees)
			email_from = settings.EMAIL_HOST_USER
			recipient_list = [user]
			send_mail( subject, message, email_from, recipient_list )
		except Exception as e:
			print(e)
			pass
	else:
		try:

			user=patient.patient.email
			fname=patient.patient.fname
			lname=patient.patient.lname
			time=patient.time
			date=patient.date
			fees=patient.doctor.doctor_fees
			pdiscrpiton=patient.discrpiton
			de=patient.doctor.doctor.email
			dfname=patient.doctor.doctor.fname
			dlname=patient.doctor.doctor.lname
			dname=patient.doctor.doctor_speciality
			print(user)
			print(de)
			subject = 'Your appointments book  with  doctor '

			message = 'Appointments with  doctor '+str(dfname)+' '+str(dlname)+'\n Speciality In '+str(dname)+'\n At time '+str(time)+'\n '+"patient Details:"+str(fname)+' '+str(lname)+''+'\n You have unpaid Rs'+ str(fees)
			email_from = settings.EMAIL_HOST_USER
			recipient_list = [user]
			send_mail( subject, message, email_from, recipient_list )
		except Exception as e:
			print(e)
			pass


	paytm_params['CHECKSUMHASH'] = checksum
	print('SENT: ', checksum)
	
	return render(request, 'redirect.html', context=paytm_params)

@csrf_exempt
def callback(request):
	if request.method == 'POST':
		received_data = dict(request.POST)
		paytm_params = {}
		paytm_checksum = received_data['CHECKSUMHASH'][0]
		for key, value in received_data.items():
			if key == 'CHECKSUMHASH':
				paytm_checksum = value[0]
			else:
				paytm_params[key] = str(value[0])
		# Verify checksum
		is_valid_checksum = verify_checksum(paytm_params, settings.PAYTM_SECRET_KEY, str(paytm_checksum))
		if is_valid_checksum:
			received_data['message'] = "Checksum Matched"
		else:
			received_data['message'] = "Checksum Mismatched"
			return render(request, 'callback.html', context=received_data)
		return render(request, 'callback.html', context=received_data)


def validate_signup(request):
	email=request.GET.get('email')
	data={
		'is_taken':User.objects.filter(email__iexact=email).exists()
	}
	return JsonResponse(data)
def index(request):
	doctor=Doctor_profile.objects.all()
	return render(request,'index.html',{'doctor':doctor})
def signup(request):
	if request.method=='POST':
		try:
			user=User.objects.get(eamil=request.POST['email'])
			msg='email  is already registered'
			return render(request,'signup.html',{'msg':msg})
		except:
			if request.POST['password']==request.POST['cpassword']:
				User.objects.create(
					fname=request.POST['fname'],
					lname=request.POST['lname'],
					email=request.POST['email'],
					mobile=request.POST['mobile'],
					address=request.POST['address'],
					profile_pic=request.FILES['profile_pic'],
					password=request.POST['password'],
					)
				msg='Signup successfuly'
				return render(request,'login.html',{'msg':msg})
			else:
				msg='password  and confirm password doesnot match'
				return render(request,'signup.html',{'msg':msg})
	else:
		return render(request,'signup.html')

def login(request):
	if request.method=='POST':
		try:
			user=User.objects.get(
				email=request.POST['email'],
				password=request.POST['password'],
				) 
			if user.usertype=="patient":
				request.session['email']=user.email
				request.session['fname']=user.fname
				request.session['profile_pic']=user.profile_pic.url
 
				return render(request,'index.html')
			else:
				request.session['email']=user.email
				request.session['fname']=user.fname
				request.session['profile_pic']=user.profile_pic.url

				return render(request,'doctor_index.html')
		except Exception as e:
			print(e)
			msg='Id And Password Does Not Match'
			return render(request,'login.html',{'msg':msg})
	else:
		return render(request,'login.html')

def header(request):
	return render(request,'header.html')

def logout(request):
	try:
		del request.session['email']
		del request.session['fname']
		return render(request,'login.html')
	except:
		return render(request,'login.html')

def profile(request):
	user=User.objects.get(email=request.session['email'])
	if request.method=='POST':
		user.fname=request.POST['fname']
		user.lname=request.POST['lname']
		user.email=request.POST['email']
		user.mobile=request.POST['mobile']
		user.address=request.POST['address']
		try:
			user.profile_pic=request.FILES['profile_pic']
		except:
			pass
		user.save()
		request.session['profile_pic']=user.profile_pic.url

		msg='user update successfuly'
		return render(request,'profile.html',{'msg':msg,'user':user})
	else:
		return render(request,'profile.html',{'user':user})

def change_password(request):
	if request.method=='POST':
		user=User.objects.get(email=request.session['email'])
		if user.password==request.POST['opassword']:
			if request.POST['npassword']==request.POST['cpassword']:
				user.password=request.POST['npassword']
				user.save()
				return redirect('logout')
			else:
				msg='New password and confirm password does not match '
				return render(request,'change_password.html',{'msg':msg})
		else:
			msg='old password does not  match '
			return render(request,'change_password.html',{'msg':msg})
	else:
		return render(request,'change_password.html')

def forgot_password(request):
	if request.method=="POST":
		try:
			user=User.objects.get(email=request.POST['email'])
			print(user)
			subject = 'OTP For Forgot Password'
			otp=random.randint(1000,9999)
			message = 'Your OTP For Forgot Password Is '+str(otp)
			email_from = settings.EMAIL_HOST_USER
			recipient_list = [user.email,]
			send_mail( subject, message, email_from, recipient_list )
			return render(request,'otp.html',{'otp':otp,'email':user.email})
		except Exception as e:
			print(e)
			msg="Email Not Registered"
			return render(request,'forgot_password.html',{'msg':msg})
	else:
		return render(request,'forgot_password.html')

def otp(request):
	otp=request.POST['otp']
	uotp=request.POST['uotp']
	email=request.POST['email']

	if uotp==otp:
		return render(request,'change_pass.html',{'email':email})
	else:
		msg=' otp does not match'
		return render(request,'otp.html',{'otp':otp,'msg':msg,'email':email})

def change_pass(request):
	npassword=request.POST['npassword']
	cpassword=request.POST['cpassword']
	email=request.POST['email']
	if npassword==cpassword:
		user=User.objects.get(email=request.POST['email'])
		user.password=npassword
		user.save()
		return redirect('login')
	else:
		msg='password and confirm password does not match '
		return render(request,'change_pass.html',{'msg':msg,'email':email})

def contact(request):
	if request.method=='POST':
		Contact.objects.create(
			name=request.POST['name'],
			subject=request.POST['subject'],
			email=request.POST['email'],		
			message=request.POST['message']
			)
		msg='contact save successfuly'
		contacts=Contact.objects.all().order_by('-id')[:5]
		return render(request,'contact.html',{'msg':msg,'contacts':contacts})
	else:
		contacts=Contact.objects.all().order_by('-id')[:5]
		return render(request,'contact.html',{'contacts':contacts})

def gallery(request):
	return render(request,'gallery.html')




def medical_counseling(request):
	return render(request,'medical_counseling.html')

def medical_research(request):
	return render(request,'medical-research.html')

def blood_bank(request):
	return render(request,'blood-bank.html')

def doctor_index(request):
	return render(request,'doctor_index.html')

def doctor_profile(request):
	doctor_profile=Doctor_profile()
	doctor=User.objects.get(email=request.session['email'])
	try:
		doctor_profile=Doctor_profile.objects.get(doctor=doctor)
	except:
		pass
	if request.method=='POST':
		doctor=Doctor_profile.objects.create(
			doctor=doctor,
			doctor_degree=request.POST['doctor_degree'],
			doctor_speciality=request.POST['doctor_speciality'],
			doctor_start_time=request.POST['doctor_start_time'],
			doctor_end_time=request.POST['doctor_end_time'],
			doctor_fees=request.POST['doctor_fees'],
					)
		msg='profile update successfuly'
		return render(request,'doctor_profile.html',{'msg':msg,'doctor':doctor})	
	else:
		return render(request,'doctor_profile.html',{'doctor_profile':doctor_profile})

def doctor_pic_update(request):
	doctor=User.objects.get(email=request.session['email'])
	if request.method=='POST':
		try:
			doctor.profile_pic=request.FILES['profile_pic']
			request.session['profile_pic']=doctor.profile_pic.url

		except:
			pass
		doctor.save()
		msg='profile_pic update successfuly'
		return render(request,'doctor_pic_update.html',{'doctor':doctor,'msg':msg})
	else:
		return render(request,'doctor_pic_update.html',{'doctor':doctor})

def doctor_change_password(request):
	if request.method=='POST':
		user=User.objects.get(email=request.session['email'])
		if user.password==request.POST['opassword']:
			if request.POST['npassword']==request.POST['cpassword']:
				user.password=request.POST['npassword']
				user.save()
				return redirect('logout')
			else:
				msg='New password and confirm password does not match '
				return render(request,'doctor_change_password.html',{'msg':msg})
		else:
			msg='old password does not  match '
			return render(request,'doctor_change_password.html',{'msg':msg})
	else:
		return render(request,'doctor_change_password.html')


def doctor_profile_update(request):
	doctor=User.objects.get(email=request.session['email'])
	try:
		doctor_profile=Doctor_profile.objects.get(doctor=doctor)
	except:
		pass
	if request.method=='POST':
		doctor_profile.doctor_degree=request.POST['doctor_degree']
		doctor_profile.doctor_fees=request.POST['doctor_fees']
		doctor_profile.doctor_start_time=request.POST['doctor_start_time']
		doctor_profile.doctor_end_time=request.POST['doctor_end_time']
		doctor_profile.doctor_speciality=request.POST['doctor_speciality']
		doctor_profile.save()
		msg='User update successfuly '
		return render(request,'doctor_profile_update.html',{'doctor_profile':doctor_profile,'msg':msg})
	else:
		return render(request,'doctor_profile_update.html',{'doctor_profile':doctor_profile})

def validate_signup(request):
	email=request.GET.get('email')
	data={
		'is_taken':User.objects.filter(email__iexact=email).exists()
	}
	return JsonResponse(data)

	
def doctor(request):
	doctors=Doctor_profile.objects.all()
	return render(request,'doctor.html',{'doctors':doctors})	

def doctor_appointment(request,pk):
	doctor_profile=Doctor_profile.objects.get(pk=pk)
	return render(request,'doctor_appointment.html',{'doctor_profile':doctor_profile})

def book_doctor_appointment(request,pk):
	if 'email' in request.session:
		doctor=Doctor_profile.objects.get(pk=pk)
		patient=User.objects.get(email=request.session['email'])
		if request.method=="POST":
			try:
				message=Appointment.objects.get(doctor=doctor,patient=patient)
				msg="you have already appointments with doctor"
				return render(request,'doctor_appointment.html',{'msg':msg})
				print(message)
			except Exception as e:
				print(e)	
				Appointment.objects.create(
					doctor=doctor,
					patient=patient,
					time=request.POST['time'],
					date=request.POST['date'],
					discrpiton=request.POST['discrpiton'],
							)
				msg='appointment  successfuly'
				appointments=Appointment.objects.filter(patient=patient)
				return redirect('myappointment')

		else:
			return render (request,'book_appointment.html',{'doctor':doctor,'patient':patient})
	else:
		msg='login first '
		return render(request,'login.html',{'msg':msg})

def myappointment(request):
	patient=User.objects.get(email=request.session['email'])
	appointments=Appointment.objects.filter(patient=patient)

	return render(request,'myappointment.html',{'appointments':appointments})

def patient_cancel_appointment(request,pk):
	appointments=Appointment.objects.get(pk=pk)
	if request.method=='POST':
		cancelappointmentaptient.objects.create(
			appointments=appointments,
			cancel_issue=request.POST['cancel_issue'],
			)
		appointments.status='cancel'
		appointments.save()
		try:
			user=appointments.patient.email
			fname=appointments.patient.fname
			lname=appointments.patient.lname
			time=appointments.time
			date=appointments.date
			pdiscrpiton=appointments.discrpiton
			de=appointments.doctor.doctor.email
			dfname=appointments.doctor.doctor.fname
			dlname=appointments.doctor.doctor.lname
			dname=appointments.doctor.doctor_speciality
			print(user)
			print(de)
			subject = 'Your appointments cancel '

			message = 'Appointments cancel with  doctor '+str(dfname)+' '+str(dlname)+'Speciality In '+str(dname)+'\n At time '+str(time)+'\n '+"patient Details:"+str(fname)+' '+str(lname)
			email_from = settings.EMAIL_HOST_USER
			recipient_list = [user]
			send_mail( subject, message, email_from, recipient_list )
		except Exception as e:
			print(e)
		
		return redirect('myappointment')
	else:
		return render(request,'patient_cancel_appointment.html',{'appointments':appointments})

def doctor_appointment_schedule(request):
	doctor=User.objects.get(email=request.session['email'])
	doctor_id=Doctor_profile.objects.get(doctor=doctor)
	appointments=Appointment.objects.filter(doctor_id=doctor_id)
	return render(request,'doctor_appointment_schedule.html',{'appointments':appointments})

def doctor_cancel_appointment(request,pk):
	appointments=Appointment.objects.get(pk=pk)
	patient=doctorappointmentaptient.objects.filter(appointments=appointments)
	if request.method=='POST':
		doctorappointmentaptient.objects.create(
			appointments=appointments,
			doctor_issue=request.POST['doctor_issue'],
			)
		appointments.status='cancel'
		appointments.save()
		try:
			issue=patient[0].doctor_issue
			user=appointments.patient.email
			fname=appointments.patient.fname
			lname=appointments.patient.lname
			time=appointments.time
			date=appointments.date
			pdiscrpiton=appointments.discrpiton
			de=appointments.doctor.doctor.email
			dfname=appointments.doctor.doctor.fname
			dlname=appointments.doctor.doctor.lname
			dname=appointments.doctor.doctor_speciality
			print(user)
			print(de)
			subject = 'Your appointments cancel '

			message = 'Appointments cancel with  doctor '+str(dfname)+' '+str(dlname)+'Speciality In '+str(dname)+'\n At time '+str(time)+'\n '+"patient Details:"+str(fname)+' '+str(lname)+'\n cancel issu'+str(issue)
			email_from = settings.EMAIL_HOST_USER
			recipient_list = [user]
			send_mail( subject, message, email_from, recipient_list )
		except Exception as e:
			print(e)
		return redirect('doctor_appointment_schedule')

	else:
		return render(request,'doctor_cancel_appointment.html',{'appointments':appointments})


def doctor_accepted_appointment(request,pk):
	appointments=Appointment.objects.get(pk=pk)
	if request.method=='POST':
		appointments.status='accepted'
		appointments.save()
		try:
			user=appointments.patient.email
			fname=appointments.patient.fname
			lname=appointments.patient.lname
			time=appointments.time
			date=appointments.date
			pdiscrpiton=appointments.discrpiton
			de=appointments.doctor.doctor.email
			dfname=appointments.doctor.doctor.fname
			dlname=appointments.doctor.doctor.lname
			dname=appointments.doctor.doctor_speciality
			print(user)
			print(de)
			subject = 'Your appointments confirm'

			message = 'Appointments fix with  doctor '+str(dfname)+' '+str(dlname)+'Speciality In '+str(dname)+'at time'+str(time)+'\n'+"patient Details:"+str(fname)+' '+str(lname)+''+str(pdiscrpiton)
			email_from = settings.EMAIL_HOST_USER
			recipient_list = [user]
			send_mail( subject, message, email_from, recipient_list )
		except Exception as e:
			print(e)
		return redirect('doctor_appointment_schedule')
	else:
		return redirect('doctor_appointment_schedule')


def health_profile(request):
	patient_health_profile=HealthProfile()
	patient=User.objects.get(email=request.session['email'])
	try:
		patient_health_profile=HealthProfile.objects.get(patient=patient)
	except:
		pass
	if request.method=='POST':
		if patient_health_profile.blood_group:
			patient_health_profile.patient=patient
			if request.POST['diabetes']=='yes':
				flag1=True
			else:
				flag1=False
			if request.POST['blood_pressue']=='yes':
				flag2=True
			else:
				flag2=False
			
			patient_health_profile.blood_group=request.POST['blood_group']
			patient_health_profile.weights=request.POST['weights']
			patient_health_profile.diabetes=flag1
			patient_health_profile.blood_pressue=flag2
			patient_health_profile.save()
			msg='update successfuly'
			return render(request,'health_profile.html',{'patient_health_profile':patient_health_profile,'msg':msg})

		else:	
			diabetes=request.POST['diabetes']
			if diabetes=='yes':
				flag1=True
			else:
				flag1=False
			blood_pressue=request.POST['blood_pressue']
			if blood_pressue=='yes':
				flag2=True
			else:
				flag2=False
			patient_health_profile=HealthProfile.objects.create(
				patient=patient,
				blood_group=request.POST['blood_group'],
				weights=request.POST['weights'],
				diabetes=flag1,
				blood_pressue=flag2,
				)

		return render(request,'health_profile.html',{'patient_health_profile':patient_health_profile})
	else:
		return render(request,'health_profile.html',{'patient_health_profile':patient_health_profile})

def patient_health_report(request,pk):
	appointment=Appointment.objects.get(pk=pk)
	patient=appointment.patient
	health_profile=HealthProfile.objects.get(patient=patient)
	return render(request,'patient_health_report.html',{'health_profile':health_profile})

def prescription_by_doctor(request,pk):
	appointment=Appointment.objects.get(pk=pk)
	if request.method=='POST':
		appointment.prescription=request.POST['prescription']
		appointment.status='completed'
		appointment.save()
		return redirect('doctor_appointment_schedule')

	else:
		return render(request,"prescription_by_doctor.html",{'appointment':appointment})

def prescription_by_doctor_patient(request,pk):
	appointment=Appointment.objects.get(pk=pk)
	return render(request,"prescription_by_doctor_patient.html",{'appointment':appointment})