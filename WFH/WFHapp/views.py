from django.http import JsonResponse
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from .forms import InterimForm
from .models import Employee
from django.contrib import messages
import pandas as pd
import os
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

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

def get_employee_details(request):
    if request.method == 'GET':
        term = request.GET.get('term', '')

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
            instance = form.save()

            request_id = instance.request_id
            
            name = form.cleaned_data['employee_name']
            email = form.cleaned_data['email']
            message = f"This is a notification to inform you that {name} is on a Interim Work From Home . Please find the below details."

            # send email
            subject = f'{name} Interim Work from Home - Notification - Request ID : {request_id}'
            body = f'Hi,\n\n{message}'
            email_message = EmailMessage(subject, body, to=['vishnu.m@kaseya.com'])

            # Create Excel file from form data
            data = {
                'Request ID': request_id,
                'Employee Name': [form.cleaned_data['employee_name']],
                'Employee ID': [form.cleaned_data['employee_id']],
                'Location': [form.cleaned_data['location']],
                'Department': [form.cleaned_data['department']],
                'Designation': [form.cleaned_data['designation']],
                'Reporting Manager': [form.cleaned_data['reporting_manager']],
                'WFH Start Date': [form.cleaned_data['start_date']],
                'WFH End Date': [form.cleaned_data['end_date']],
                'Number of Days': [form.cleaned_data['num_of_days']],
                'Reason for WFH': [form.cleaned_data['reason']],
                'Description': [form.cleaned_data['description']],
                'Tenure': [form.cleaned_data['tenure']],
            }
            df = pd.DataFrame(data)
            excel_file = "WFH_Details.xlsx"
            df.to_excel(excel_file, index=False)

            # Attach the Excel file to the email
            email_message.attach_file(excel_file)
            email_message.send()

            # Delete the temporary Excel file after sending the email

            os.remove(excel_file)

            messages.success(request, 'Interim WFH Form Submitted Successfully')
            print('form saved')
            return redirect('home')

    else:
        form = InterimForm()

    context = {
        'form': form,
    }

    return render(request, 'index.html', context)

