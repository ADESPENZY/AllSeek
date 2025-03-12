from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import ResumeForm
from .models import Resume

# Custom file validation function
def is_valid_file(file):
    allowed_types = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']
    return file.content_type in allowed_types

# In your create_resume view
def create_resume(request):
    if request.method == 'POST':
        # Handling file upload
        if 'upload_resume' in request.POST:
            file = request.FILES.get('file')
            if file:
                # Validate file type
                if not is_valid_file(file):
                    messages.error(request, "Invalid file type. Only PDF and Word documents are allowed.")
                    return redirect('create_resume')
                # Save uploaded file
                Resume.objects.create(user=request.user, file=file)
                request.user.has_resume = True
                request.user.save(update_fields=['has_resume'])

                messages.success(request, "Resume uploaded successfully.")
                return redirect('dashboard')
            else:
                messages.error(request, "No file selected.")
        
        # Handling form submission for creating resume
        elif 'create_resume' in request.POST:
            form = ResumeForm(request.POST, request.FILES)
            if form.is_valid():
                resume = form.save(commit=False)
                resume.user = request.user
                resume.save()
                # Update has_resume field
                request.user.has_resume = True
                request.user.save(update_fields=['has_resume'])
                messages.success(request, "Resume created successfully.")
                return redirect('dashboard')
            else:
                messages.error(request, "There are errors in the form. Please correct them.")

    else:
        form = ResumeForm()

    # Check if the user has a resume in the Resume model
    if Resume.objects.filter(user=request.user).exists():
        messages.info(request, "You already have a resume.")
        return redirect('dashboard')  # Redirect to dashboard or wherever you need

    return render(request, 'resume/create-resume.html', {'form': form})


def update_resume(request):
    # Get the specific resume instance or return 404
    resume = get_object_or_404(Resume, user=request.user)
    
    if request.method == 'POST':
        form = ResumeForm(request.POST, request.FILES, instance=resume)
        if form.is_valid():
            form.save()
            messages.success(request, "Resume updated successfully.")
            return redirect('dashboard')  # Redirect to the desired page
        else:
            messages.error(request, "Error updating the form. Please correct the fields below.")
    else:
        form = ResumeForm(instance=resume)  # Populate form with the existing data
    
    return render(request, 'resume/update-resume.html', {'form': form})

def delete_resume(request):
    resume = get_object_or_404(Resume, user=request.user)  # Ensure the resume belongs to the current user
    
    if request.method == 'POST':
        resume.delete()
        request.user.has_resume = False
        request.user.save()
        messages.success(request, "Resume deleted successfully.")
        return redirect('dashboard')
    
    return render(request, 'resume/delete-resume.html', {'resume': resume})

def applicant_details(request):
    # Get the specific resume based on its primary key (pk)
    resume = get_object_or_404(Resume, user=request.user)

    # Check if the resume has a file uploaded or if it was created with other details
    if resume.file:  # If the resume has a file (uploaded resume)
        file_status = "Uploaded"
    else:  # If the resume was created (not uploaded as a file)
        file_status = "Created"

    return render(request, 'resume/resume-detail.html', {'resume': resume, 'file_status': file_status})

from io import BytesIO
from django.http import FileResponse
from django.shortcuts import redirect
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from PIL import Image

def resume_pdf(request):
    # Fetch the current user's resume
    resume = Resume.objects.filter(user=request.user).first()
    if not resume:
        return redirect('dashboard')  # Redirect if no resume is found

    # Create a buffer for the PDF
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    y_position = height - 1 * inch  # Starting position

    # Title
    p.setFont("Helvetica-Bold", 16)
    p.drawString(inch, y_position, f"Resume of {resume.firstname or ''} {resume.lastname or ''}")
    y_position -= 0.5 * inch

    # Details Section
    p.setFont("Helvetica", 12)

    # Image Handling
    if resume.image:
        try:
            img_path = resume.image.path
            img = ImageReader(img_path)
            p.drawImage(img, inch, y_position - 2 * inch, width=2 * inch, height=2 * inch)
            y_position -= 2.5 * inch  # Adjust position after adding the image
        except Exception:
            p.drawString(inch, y_position, "[Image could not be loaded]")
            y_position -= 1 * inch

    # Add fields to the PDF
    if resume.job_title:
        p.drawString(inch, y_position, f"Job Title: {resume.job_title}")
        y_position -= 0.3 * inch

    if resume.user:
        p.drawString(inch, y_position, f"Email: {resume.user.email}")
        y_position -= 0.3 * inch

    if resume.gender:
        p.drawString(inch, y_position, f"Gender: {resume.get_gender_display()}")
        y_position -= 0.3 * inch

    if resume.dob:
        p.drawString(inch, y_position, f"Date of Birth: {resume.dob.strftime('%B %d, %Y')}")
        y_position -= 0.3 * inch

    if resume.nationality:
        p.drawString(inch, y_position, f"Nationality: {resume.nationality}")
        y_position -= 0.3 * inch

    if resume.religion:
        p.drawString(inch, y_position, f"Religion: {resume.religion}")
        y_position -= 0.3 * inch

    if resume.phone:
        p.drawString(inch, y_position, f"Phone: {resume.phone}")
        y_position -= 0.3 * inch

    if resume.address:
        p.drawString(inch, y_position, f"Address: {resume.address}")
        y_position -= 0.3 * inch

    if resume.school:
        p.drawString(inch, y_position, f"School: {resume.school}")
        y_position -= 0.3 * inch

    if resume.qualification:
        p.drawString(inch, y_position, f"Qualification: {resume.qualification}")
        y_position -= 0.3 * inch

    if resume.year_of_graduation:
        p.drawString(inch, y_position, f"Year of Graduation: {resume.year_of_graduation}")
        y_position -= 0.3 * inch

    if resume.experience:
        p.drawString(inch, y_position, "Experience:")
        y_position -= 0.3 * inch
        for line in resume.experience.splitlines():
            p.drawString(inch + 0.2 * inch, y_position, line)
            y_position -= 0.3 * inch

    if resume.skills:
        p.drawString(inch, y_position, "Skills:")
        y_position -= 0.3 * inch
        for line in resume.skills.splitlines():
            p.drawString(inch + 0.2 * inch, y_position, line)
            y_position -= 0.3 * inch

    if resume.reference:
        p.drawString(inch, y_position, "References:")
        y_position -= 0.3 * inch
        for line in resume.reference.splitlines():
            p.drawString(inch + 0.2 * inch, y_position, line)
            y_position -= 0.3 * inch

    # Add a footer
    if y_position < inch:
        p.showPage()
        y_position = height - inch

    p.drawString(inch, y_position, "End of Resume")
    p.save()

    # Return the PDF as a file response
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='resume.pdf')

