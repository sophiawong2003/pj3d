from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from . models import Contact
from django.core.mail import send_mail
# Create your views here.
def contact(request):
    if request.method == 'POST':
        course_id = request.POST["course_id"]
        course = request.POST["course"]
        name = request.POST["name"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        message = request.POST["message"]
        user_id = request.POST["user_id"]
        tutor_email = request.POST["tutor_email"]
        if request.user.is_authenticated:
            #user_id = request.user.id
            has_contacted = Contact.objects.all().filter(course_id=course_id, user_id=user_id)
            if has_contacted:
                messages.error(request, "You have already made an inquiry for this course")
                return redirect('/courses/'+course_id)
        contact = Contact(course=course, course_id=course_id, name=name, email=email, phone=phone, message=message, user_id=user_id)
        contact.save()
        # send email
        send_mail(
            '3D Printer Course Inquiry',
            'There has been an inquiry for ' + course + '. Sign into the admin panel for more info',
            'sophiawong2003@gmail.com', # from admin email
            [tutor_email], # to email 
            fail_silently=False
        )
        messages.success(request,"Your request has been submitted, a tutor will get back to you soon")    
    return redirect('/courses/'+course_id)

def delete_contact(request, contact_id):
    contact = get_object_or_404(Contact, pk=contact_id)
    contact.delete()
    return redirect('dashboard')


