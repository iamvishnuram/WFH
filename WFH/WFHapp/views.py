from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import InterimForm
from .models import Employee
from django.contrib import messages
from datetime import datetime
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from datetime import datetime

def logout_view(request):
    logout(request)
    return redirect('login')

def login_view(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid Username or Password")
    return render(request, 'Registration/login.html')

@login_required
def get_employee_details(request):
    if request.method == 'GET':
        # Query the database to retrieve the employee details
        employees = Employee.objects.filter(WorkEmail__istartswith=request.GET.get('term'))[:20]
        
        employee_data = []
        
        for employee in employees:
            employee_data.append({
                'employee_id': employee.Employee,
                'name': employee.FirstNameLastName,
                'location': employee.Location,
                'reporting_manager': employee.ReportingTo,
                'email': employee.WorkEmail,
                'department': employee.Department,
                'designation': employee.JobLevel,
                'tenure': employee.Tenure,
            })

        return JsonResponse(employee_data, safe=False)

@login_required
def get_authenticated_employee_details(request):
    authenticated_user = request.user
    authenticated_user_email = authenticated_user.email

    # Query the database to retrieve the employee details for the authenticated user
    try:
        employee = Employee.objects.get(WorkEmail__iexact=authenticated_user_email)
    except Employee.DoesNotExist:
        return JsonResponse({'error': 'Employee not found'}, status=404)

    employee_data = {
        'employee_id': employee.Employee,
        'name': employee.FirstNameLastName,
        'location': employee.Location,
        'reporting_manager': employee.ReportingTo,
        'email': employee.WorkEmail,
        'department': employee.Department,
        'designation': employee.JobLevel,
        'tenure': employee.Tenure,
    }

    return JsonResponse(employee_data)

def search(request):
    if 'term' in request.GET:
        queryset = Employee.objects.filter(WorkEmail__istartswith=request.GET.get('term'))[:20]
        titles = [employee.WorkEmail for employee in queryset]
        return JsonResponse(titles, safe=False)

@login_required(login_url='login')    
def home_view(request):
    if request.method == 'POST':
        form = InterimForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.requester_mail = request.user.email
            instance.submission_time = datetime.now().strftime("%m-%d-%Y %I:%M %p"+" UTC")
            instance.save()
            request_id = instance.request_id
            
            authenticated_user = request.user
            authenticated_user_email = authenticated_user.email
            
            today = datetime.now()
            submission_time = today.strftime("%m-%d-%Y %I:%M %p"+" UTC")
            
            name = form.cleaned_data['employee_name']
            email = form.cleaned_data['email']
           
            # Send email
            subject = f'{name} Interim Work from Home - Notification - Request ID: {request_id}'
            
            # Render HTML template with data
            context = {
                'requester':authenticated_user,
                'requester_mail': authenticated_user_email,
                'request_id': request_id,
                'submission_time': submission_time,
                'employee_name': form.cleaned_data['employee_name'],
                'employee_id': form.cleaned_data['employee_id'],
                'location': form.cleaned_data['location'],
                'department': form.cleaned_data['department'],
                'designation': form.cleaned_data['designation'],
                'reporting_manager': form.cleaned_data['reporting_manager'],
                'start_date': form.cleaned_data['start_date'],
                'end_date': form.cleaned_data['end_date'],
                'num_of_days': form.cleaned_data['num_of_days'],
                'reason': form.cleaned_data['reason'],
                'description': form.cleaned_data['description'],
                'tenure': form.cleaned_data['tenure'],
            }
            html_message = render_to_string('email_template.html', context)
            
            # Create plain text version of the email
            text_message = strip_tags(html_message)
            
            # Create EmailMultiAlternatives object
            email_message = EmailMultiAlternatives(subject, text_message, to=['vishnu.m@kaseya.com'])
            email_message.attach_alternative(html_message, "text/html")
            
            email_message.send()

            messages.success(request, 'Interim WFH Form Submitted Successfully')
            print('form saved')
            return redirect('home')

    else:
        form = InterimForm()

    context = {
        'form': form,
    }

    return render(request, 'index.html', context)

