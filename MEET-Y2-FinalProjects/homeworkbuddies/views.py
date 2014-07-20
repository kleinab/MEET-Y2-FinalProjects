from django.shortcuts import render
from homeworkbuddies.models import Student, Subject, Assignment

def index(request):
    if 'student_id' not in request.session:
        return login(request)
    student = Student.objects.get(id=request.session['student_id'])
    subjects = Subject.objects.filter(students=student)
    assignments = [(subject, Assignment.objects.filter(subject=subject)) for subject in subjects]
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

def new_subject(request):
    if request.method == 'GET':
        if 'student_id' not in request.session:
            return login(request)
        students = Student.objects.all()
        return render(request, 'homeworkbuddies/new_subject.html', {'students': students})
    else:
        name = request.POST['name']
        students = request.POST['students']
        subject = Subject(name=name, students=students)
        subject.save()
        return render(request, 'homeworkbuddies/index.html')

def new_assignment(request):
    if request.method == 'GET':
        if 'student_id' not in request.session:
            return login(request)
        subjects = Subject.objects.all()
        return render(request, 'homeworkbuddies/new_assignment.html', {'subjects': subjects})
    else:
        name = request.POST['name']
        subject = Subject.objects.get(name=request.POST['subject'])
        duedate = request.POST['duedate']
        assignment = Assignment(name=name, subject=subject, duedate=duedate)
        assignment.save()
        return render(request, 'homeworkbuddies/index.html')
