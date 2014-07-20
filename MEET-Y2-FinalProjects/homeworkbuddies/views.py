from django.shortcuts import render
from homeworkbuddies.models import Student, Subject, Assignment, Message
import datetime
from django.utils import timezone

def index(request):
    if 'student_id' not in request.session:
        return login(request)
    student = Student.objects.get(id=request.session['student_id'])
    subjects = Subject.objects.filter(students=student)
    assignments = [(subject, Assignment.objects.filter(subject=subject).order_by('-duedate')) for subject in subjects]
    return render(request, 'homeworkbuddies/index.html', {'student': student, 'assignments': assignments});

def login(request):
    if request.method == 'GET':
        return render(request, 'homeworkbuddies/login.html', {'error_message': ''})
    else:
        student_set = Student.objects.filter(username=request.POST['username'])
        if len(student_set) == 0:
            return render(request, 'homeworkbuddies/login.html', {'error_message': 'Username not found!'})
        student = student_set[0]
        if student.password != request.POST['password']:
            return render(request, 'homeworkbuddies/login.html', {'error_message': 'Invalid password!'})
        else:
            request.session['student_id'] = student.id
            return index(request)

def signup(request):
    if request.method == 'GET':
        return render(request, 'homeworkbuddies/signup.html', {'error_message': ''})
    else:
        username = request.POST['username']
        password0 = request.POST['password0']
        password1 = request.POST['password1']
        if (password0 == password1):
            student = Student(username=username, password=password0)
            student.save()
            request.session['student_id'] = student.id
            return index(request)
        else:
            return render(request, 'homeworkbuddies/signup.html', {'error_message': 'Mismatched passwords!'})

def logout(request):
    if 'student_id' in request.session:
        del request.session['student_id']
    return login(request)

def view_assignment(request, assignment_id):
    if 'student_id' not in request.session:
        return login(request)
    student = Student.objects.get(id=request.session['student_id'])
    assignment = Assignment.objects.get(id=assignment_id)
    messages = Message.objects.filter(assignment=assignment).order_by('-date')
    return render(request, 'homeworkbuddies/assignment.html', {'student': student, 'assignment': assignment, 'messages': messages})

def post_message(request, assignment_id):
    author = Student.objects.get(id=request.session['student_id'])
    assignment = Assignment.objects.get(id=assignment_id)
    text = request.POST['text']
    date = timezone.now()
    message = Message(author=author, assignment=assignment, text=text, date=date)
    message.save()
    return view_assignment(request, assignment_id)    
