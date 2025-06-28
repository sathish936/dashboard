from django.shortcuts import render, redirect,get_object_or_404
from .models import Employee
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib import messages
from .forms import UserRegisterForm,TaskForm
from django.contrib.auth import authenticate, login
from .models import StaffProfile
from .forms import StaffProfileForm
from .models import *
from .forms import AdminRegistrationForm

# Create your views here.



def home(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            # Redirect based on user role
            if user.is_superuser or user.is_staff:
                return redirect('dashboard')  # Name in urls.py

            elif not user.is_staff and not user.is_superuser:
                return redirect('profile')

            
            else:
                messages.error(request, "You don't have access.")
                return redirect('home')  # Or 403 page
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'basic/home.html')



@login_required

def dashboard(request):
    employees = StaffProfile.objects.all()
    employee_count = employees.count() 
    department_count = employees.exclude(department__exact='').values('department').distinct().count()
    recent_logins = 5     # static for now

    return render(request, 'dashboard/dashboards.html', {
        'employees': employees,
        'employee_count': employee_count,
        'department_count': department_count,
        'recent_logins': recent_logins,
    })



def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # 🔒 Disable login until approved
            user.save()

            # Assign group, send message, etc.
            messages.success(request, "Registration successful! Please wait for manager approval.")
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'basic/register.html', {'form': form})



def pending_users(request):
    pending = User.objects.filter(is_active=False)
    return render(request, 'accounts/pending_users.html', {'pending_users': pending})


def approve_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_active = True
    user.save()
    messages.success(request, f"{user.username} has been approved.")
    return redirect('pending_users')

# create add staff

def staff_create(request):
    if request.method == 'POST':
        form = StaffProfileForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Staff added successfully.")
            return redirect('dashboard')
    else:
        form = StaffProfileForm()
    return render(request, 'dashboard/staff_add.html', {'form': form, 'title': 'Add Staff'})


def staff_update(request, id):
    staff = get_object_or_404(StaffProfile, id=id)  # Get the staff or 404 if not found
    if request.method == 'POST':
        form = StaffProfileForm(request.POST, instance=staff)  # Bind form with POST data and existing staff
        if form.is_valid():
            form.save()  # Save updates
            messages.success(request, "Staff updated successfully.")
            return redirect('dashboard')  # Redirect to list view after update
    else:
        form = StaffProfileForm(instance=staff)  # For GET, pre-fill form with existing data
    return render(request, 'dashboard/staff_update.html', {'form': form, 'title': 'Update Staff'})


def staff_delete(request, id):
    staff = get_object_or_404(StaffProfile, id=id)  # safely get staff or 404
    staff.delete()  # delete the object
    messages.success(request, "Staff deleted successfully.")
    return redirect('dashboard')







    
def profile(request):
    profile = get_object_or_404(StaffProfile, user=request.user)

    tasks = Task.objects.filter(staff=profile)
    completed_count = tasks.filter(is_completed=True).count()
    pending_count = tasks.filter(is_completed=False).count()

    return render(request, 'staff/profile.html', {
        'profile': profile,
        'tasks': tasks,
        'completed_count': completed_count,
        'pending_count': pending_count,
    })



def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  # Change to your dashboard URL name
    else:
        form = TaskForm()
    return render(request, 'tasks/add_task.html', {'form': form})




def register_admin(request):
    if request.method == 'POST':
        form = AdminRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.is_staff = form.cleaned_data['is_staff']
            user.is_superuser = form.cleaned_data['is_superuser']
            user.save()
            messages.success(request, "Admin user created successfully.")
            return redirect('home')  # Redirect to login or dashboard
    else:
        form = AdminRegistrationForm()
    return render(request, 'accounts/admin_register.html', {'form': form})
