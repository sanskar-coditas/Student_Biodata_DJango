from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.db import IntegrityError
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
    
        photo_folder = path.join('static', 'photos')
        resume_folder = path.join(settings.BASE_DIR, 'static', 'resumes')

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
        
        student = Student(
            first_name=first_name,
            last_name=last_name,
            dob=dob,
            photo=photo_path,
            resume=resume_path
        )
        student.save()

        updated_student = Student.objects.get(pk=student.pk)
                
                # Create a dictionary with updated data for rendering in a different template
        updated_data = {
                    'first_name': updated_student.first_name,
                    'last_name': updated_student.last_name,
                    'dob': updated_student.dob,
                    'photo_url': updated_student.photo.url if updated_student.photo else None,
                    'resume_url': updated_student.resume.url if updated_student.resume else None,
                    'is_photo_uploaded': is_photo_uploaded,
                    'is_resume_uploaded': is_resume_uploaded,
                }
        print(f"path of  photo {updated_student.photo.url}")

        return render(request, 'updated_data_template.html', {'data': updated_data})
    else:
        return render(request, 'student_profile_form.html')
    

@csrf_exempt
def get(request):
    if request.method == 'POST':
            edit_first_name = request.POST.get('editFirstNameGet', '')
            students = Student.objects.filter(first_name=edit_first_name)
            data = [{'first_name': student.first_name, 'last_name': student.last_name, 'dob': student.dob, 'photo_path':student.photo.url} for student in students]
            return render(request, 'display_data.html', {'data': data})
    else: 
        return render(request, 'student_profile_form.html')

@csrf_exempt
def delete(request):
    if request.method == 'POST':
        edit_first_name = request.POST.get('editFirstNameDelete', '')
        student = Student.objects.filter(first_name=edit_first_name).first()
        if student:
            student.delete()
            message = f"First student with first name {edit_first_name} deleted successfully."
        else:
            message = f"No student found with first name {edit_first_name}. Nothing deleted."
        return HttpResponse(message)
    else:
        return render(request, 'student_profile_form.html')

@csrf_exempt
def update(request):
    if request.method == 'POST':
        edit_first_name = request.POST.get('editFirstNameUpdate', '')
        new_first_name = request.POST.get('newFirstName', '')
        new_last_name = request.POST.get('newLastName', '')
        new_dob = request.POST.get('newDob', '')
        new_photo = request.FILES.get('newImage')
        new_resume = request.FILES.get('newResume')

        new_photo_folder = path.join('static', 'photos')
        new_resume_folder = path.join(settings.BASE_DIR, 'static', 'resumes')

        try:
            student = Student.objects.filter(first_name=edit_first_name).first()

            if student:

                is_resume_uploaded = ""
                is_photo_uploaded = ""

                if new_photo:
                    photo_path = path.join(new_photo_folder, new_photo.name)
                    with open(photo_path, 'wb') as photo_file:
                        for chunk in new_photo.chunks():
                            photo_file.write(chunk)
                            is_photo_uploaded = f"Photo uploaded at {new_photo_folder}"
                else:
                    photo_path = None
                    is_photo_uploaded = "Photo not uploaded"

                if new_resume:
                    resume_path = path.join(new_resume_folder, new_resume.name)
                    with open(resume_path, 'wb') as resume_file:
                        for chunk in new_resume.chunks():
                            resume_file.write(chunk)
                            is_resume_uploaded = f"Resume uploaded at {new_resume_folder}"
                else:
                    resume_path = None
                    is_resume_uploaded = "Resume not uploaded"
                

                Student.objects.filter(first_name=edit_first_name).update(
                    first_name=new_first_name,
                    last_name=new_last_name,
                    dob=new_dob,
                    photo=photo_path,
                    resume=resume_path
                )

                updated_student = Student.objects.get(pk=student.pk)
                
                updated_data = {
                    'first_name': updated_student.first_name,
                    'last_name': updated_student.last_name,
                    'dob': updated_student.dob,
                    'photo_url': updated_student.photo.url,
                    'resume_url': updated_student.resume.url if updated_student.resume else None,
                    'is_photo_uploaded': is_photo_uploaded,
                    'is_resume_uploaded': is_resume_uploaded,
                }
                print(f"path of  photo {updated_student.photo.url}")

                return render(request, 'updated_data_template.html', {'data': updated_data})
            else:
                message = f"No student found with first name {edit_first_name}. Nothing updated."
        except IntegrityError:
            message = f"Error updating student. IntegrityError occurred."

        return HttpResponse(message)
    else:
        return render(request, 'student_profile_form.html')
