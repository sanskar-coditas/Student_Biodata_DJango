from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from os import path,makedirs
from django.conf import settings
from .models import Student



@csrf_exempt
def submit(request):
    if request.method == 'POST':
        first_name = request.POST.get('firstName',"")
        last_name = request.POST.get('lastName',"")
        dob = request.POST.get('dob',"")
        photo = request.FILES.get('image')
        resume = request.FILES.get('resume')
        print("Started")
    
        photo_folder = path.join(settings.BASE_DIR, 'static', 'photos')
        resume_folder = path.join(settings.BASE_DIR, 'static', 'resumes')


        # Create an Employee instance and save it to the database
        employee = Student(
            first_name=first_name,
            last_name=last_name,
            dob=dob,
            photo=photo,
            resume=resume
        )
        employee.save()

        result2 = f"Employee record saved: {employee}"

        is_resume_uploaded = ""
        is_photo_uploaded = ""

        if photo:
            photo_path = path.join(photo_folder, photo.name)
            with open(photo_path, 'wb') as photo_file:
                for chunk in photo.chunks():
                    photo_file.write(chunk)
                    is_photo_uploaded = f"Photo uploded at {photo_folder}"
        else:
            photo_path = None
            is_photo_uploaded = "Photo not uploaded"

        if resume:
            resume_path = path.join(resume_folder, resume.name)
            with open(resume_path, 'wb') as resume_file:
                for chunk in resume.chunks():
                    resume_file.write(chunk)
                    is_resume_uploaded = f"Resume uploded at {resume_folder}"
        else:
            resume_path = None
            is_resume_uploaded = "Resume not uploaded"

        result = f"Received data: First Name - {first_name}, Last Name - {last_name}, DOB - {dob}, Resume photo Status: {is_resume_uploaded} and {is_photo_uploaded} and Sqlite Employee record saved: {employee}"
        return HttpResponse(result)
    else:
        return render(request, 'student_profile_form.html')
