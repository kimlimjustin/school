from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User, Blog, UserType, Class, Student, Announcement, Attachment, Teacher, Submission
from django.core.paginator import Paginator
import json
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
	news = Blog.objects.filter(target = "News").order_by('-pk')
	if request.method == "POST":
		data = json.loads(request.body)
		username = data['username']
		password = data['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			usertype = UserType.objects.filter(user = user)[0].accountType
			return JsonResponse({'message': 'Login Success', 'usertype': usertype})
		else:
			return JsonResponse({'message': 'Invalid username and/or password.'})
	usertype = None
	if request.user.is_authenticated:
		usertype = UserType.objects.filter(user = request.user)[0].accountType
	temp = Paginator(news, 10)
	news = []
	paginatorinfo = []
	for i in range(temp.num_pages):
		page = temp.page(i+1).object_list
		news.append(page)
		paginatorinfo.append(temp.page(i+1))
	return render(request, "index/index.html",{
		"profile": news,
		"usertype": usertype,
		"news": news,
		"info": paginatorinfo,
		"totalpage": len(paginatorinfo)
		})

def dashboard(request):
	blogtargetlist = ["All","Student", "News"]
	if request.method == "POST":
		data = json.loads(request.body)
		if Class.objects.filter(classLevel = int(data['classlevel']), className = data['classname']).count() > 0:
			return JsonResponse({"message": "Class With that name has exist"})
		else:
			temp = Class(classLevel = int(data['classlevel']), className = data['classname'])
			temp.save()
			return JsonResponse({"message": "Class created"})
	if not request.user.is_authenticated:
		return render(request, "index/error.html", {
			"message": "You are not signed in",
			"signin": False
			})
	usertype = UserType.objects.filter(user = request.user.id)[0].accountType
	if usertype!= "admin" and usertype!='teacher':
		if usertype == "student":
			return render(request, "index/error.html", {
				"message": "You have no access to this page.",
				"signin": False,
				"student": True
				})
		else:	
			return render(request, "index/error.html", {
				"message": "You have no access to this page.",
				"signin": False,
				"student": False
				})
	classlist = []
	studentlist = []
	studentinfo = []
	if usertype == "admin":
		classes = Class.objects.all()
		students = UserType.objects.filter(accountType = "student")
		for i in classes:
			classlist.append(i)
		for j in students:
			studentlist.append(j.user)
			info = Student.objects.filter(name = j.user.id)
			for k in info:
				classname = f"{k.Class.classLevel} - {k.Class.className}"
				studentinfo.append(classname)
	elif usertype == "teacher":
		teaching = Teacher.objects.filter(teacher_id = request.user.id)
		for i in teaching:
			teachingclass = i.teaching
			classlist.append(teachingclass)
			
			temp = Student.objects.filter(Class = teachingclass)
			for j in temp:
				studentlist.append(User.objects.filter(username = j.name)[0])
				info = Student.objects.filter(name = j.name)
				for k in info:
					classname = f"{k.Class.classLevel} - {k.Class.className}"
					studentinfo.append(classname)

	teachers = Teacher.objects.all()
	teacherList = []
	for i in classlist:
		teachers = Teacher.objects.filter(teaching_id = i.id)
		temp = []
		for j in teachers:
			temp.append(j.teacher)
		if len(temp) == 0:
			teacherList.append("")
		else:
			teacherList.append(temp)
	return render(request, "index/panel.html", {
		"classes": classlist,
		"usertype": usertype,
		"allTeacher": teachers,
		"teachers": teacherList,
		"students": studentlist,
		"studentinfo": studentinfo,
		"blogtarget": blogtargetlist
		})

def register(request):
	if request.method == "POST":
		data = json.loads(request.body)
		print(data)
		try:
			user = User.objects.create_user(username = data['username'], email = data['email'], password = data["password"], userID = data["userID"])
			usertype = UserType(user = user, accountType = data["accountType"])
			usertype.save()
			if data["accountType"] == "student":
				userclass = Student(name = user, Class_id = data['class'])
				userclass.save()
				temp = Class.objects.get(pk = data["class"])
				temp1 = f"{temp.classLevel} - {temp.className}"
				return JsonResponse({"message": "User Created Successfully", "class": temp1})
			elif data["accountType"] == "teacher":
				if data["class"] != "none":
					teachingclass = Class.objects.get(pk = data["class"])
					teach = Teacher(teaching = teachingclass, teacher = user)
					teach.save()
				return JsonResponse({"message": "Teacher added Successfully"})
		except IntegrityError:
			return JsonResponse({"message": "Username already Taken."})
		
		
	else:
		return HttpResponseRedirect(reverse('index'))


def logout_view(request):
	logout(request)
	return HttpResponseRedirect(reverse('index'))


def blog(request):
	if request.method == "POST":
		data = json.loads(request.body)
		blog = Blog(image = data["image"], title = data["title"], content = data["content"], target = data["target"])
		blog.save()
		return JsonResponse({"message": "Blog Created Successfully"})
	if request.user.is_authenticated:
		usertype = UserType.objects.filter(user = request.user)[0].accountType
		if usertype == "student" or "teacher":
			blogs = Blog.objects.filter(target = "All").order_by('-pk') | Blog.objects.filter(target = usertype.capitalize()).order_by('-pk')
		else:
			blogs = Blog.objects.filter(target = "All").order_by('-pk')
		temp = Paginator(blogs, 10)
		blogs = []
		paginatorinfo = []
		for i in range(temp.num_pages):
			page = temp.page(i+1).object_list
			blogs.append(page)
			paginatorinfo.append(temp.page(i+1))
		return render(request, "index/blog.html", {
			'blogs': blogs,
			"usertype": usertype,
			"info": paginatorinfo,
			"totalpage": temp.num_pages
			})
	else:
		blogs = Blog.objects.filter(target = "All").order_by("-pk")
		temp = Paginator(blogs, 10)
		blogs = []
		paginatorinfo = []
		for i in range(temp.num_pages):
			page = temp.page(i+1).object_list
			blogs.append(page)
			paginatorinfo.append(temp.page(i+1))
		return render(request, "index/blog.html", {
			"blogs": blogs,
			"info": paginatorinfo,
			"totalpage": temp.num_pages
			})

def edit_class(request, classlevel, classname):
	if not request.user.is_authenticated:
		return render(request, "index/error.html", {
			"message": "You are not signed in",
			"signin": False
			})
	usertype = UserType.objects.filter(user = request.user.id)[0].accountType
	if usertype!= "admin" and usertype!='teacher':
		if usertype == "student":
			return render(request, "index/error.html", {
				"message": "You have no access to this page.",
				"signin": False,
				"student": True
				})
		else:	
			return render(request, "index/error.html", {
				"message": "You have no access to this page.",
				"signin": False,
				"student": False
				})
	teacherlist = UserType.objects.filter(accountType = "teacher")
	this_class = Class.objects.get(classLevel = classlevel, className = classname)
	teachers = Teacher.objects.filter(teaching = this_class)
	streams = Announcement.objects.filter(is_assignment = False, target = this_class).order_by("-pk")
	streamAttachement = []
	for i in streams:
		attachment = Attachment.objects.filter(target_attachment = i)
		temp = []
		for j in attachment:
			temp.append(j.attachment)
		streamAttachement.append(temp)
	assignments = Announcement.objects.filter(is_assignment = True, target = this_class).order_by("-pk")
	assignmentAttachment = []
	for i in assignments:
		attachment = Attachment.objects.filter(target_attachment = i)
		temp = []
		for j in attachment:
			temp.append(j.attachment)
		assignmentAttachment.append(temp)
	return render(request, "index/class_admin.html", {
		"teacherlist": teacherlist,
		"teachers": teachers,
		"class": this_class,
		"usertype": usertype,
		"streams": streams,
		"streamattachment": streamAttachement,
		"assignments": assignments,
		"assignmentAttachment": assignmentAttachment
		})
 
def add_teacher(request):
 	if request.method == "POST":
 		data = json.loads(request.body)
 		this_class = Class.objects.get(classLevel = data["classlevel"], className = data["classname"])
 		temp = Teacher(teacher_id = int(data["teacher"]), teaching = this_class)
 		temp.save()
 		teachername = User.objects.get(pk = data["teacher"]).username
 		print(teachername)
 		return JsonResponse({"message": "Success", "teacher": teachername})
 	else:
 		return HttpResponseRedirect(reverse('index'))

def remove_teacher(request):
 	if request.method == "POST":
 		data = json.loads(request.body)
 		this_class = Class.objects.get(classLevel = data["classlevel"], className = data["classname"])
 		teacher = Teacher.objects.get(teaching = this_class, teacher = int(data["teacher"]))
 		teacher.delete()
 		return JsonResponse({"message": "Success"})
 	else:
 		return HttpResponseRedirect(reverse('index'))


def edit_blog(request):
	if request.method == "POST":
		data = json.loads(request.body)
		blog = Blog.objects.get(pk = data["id"])
		blog.title = data["title"]
		blog.content = data["content"]
		blog.save()
		return JsonResponse({"message": "Success"})
	else:
		return HttpResponseRedirect(reverse('index'))


def class_view(request):
	if not request.user.is_authenticated:
		return render(request, "index/error.html", {
			"message": "You are not signed in",
			"signin": False
			})
	usertype = UserType.objects.filter(user = request.user.id)[0].accountType
	if usertype != "admin" and usertype!="teacher":
		student = Student.objects.get(name = request.user)
		this_class = Class.objects.get(classLevel = student.Class.classLevel, className = student.Class.className)
		this_class_students = Student.objects.filter(Class = this_class)
		announcements = Announcement.objects.filter(target = this_class).order_by("-pk")
		attachments = []
		for i in announcements:
			attachment = Attachment.objects.filter(target_attachment = i)
			temp = []
			for j in attachment:
				temp.append(j.attachment)
			attachments.append(temp)
		return render(request, "index/class.html", {
			"usertype": usertype,
			"class": this_class,
			"students": this_class_students,
			"announcements": announcements,
			"attachments": attachments
			})
	else:
		return HttpResponseRedirect(reverse('dashboard'))

def add_stream(request):
	if request.method == "POST":
		data = json.loads(request.body)
		target_class = Class.objects.get(classLevel = data["classlevel"], className = data["classname"])
		stream = Announcement(title = data["title"], announcement = data["stream"], creator = request.user, target = target_class)
		stream.save()
		attachment = Attachment(target_attachment = stream, attachment = data["attachment"])
		attachment.save()
		return JsonResponse({"message": "Success", "time": stream.timestamp})
	else:
		return HttpResponseRedirect(reverse("index"))

def add_assignment(request):
	if request.method == "POST":
		data = json.loads(request.body)
		target_class = Class.objects.get(classLevel = data["classlevel"], className = data["classname"])
		duedate_date = data["duedate_date"].replace("/", "-")
		duedate = f"{duedate_date} {data['duedate_time']}:00"
		assignment = Announcement(title = data["title"], announcement = data["assignment"], creator = request.user, target = target_class,
			is_assignment = True, duedate = duedate)
		assignment.save()
		attachment = Attachment(target_attachment = assignment, attachment = data["attachment"])
		attachment.save()
		return JsonResponse({"message": "Success", "time": assignment.timestamp})

	else:
		return HttpResponseRedirect(reverse('index'))

def delete(request):
	if request.method == "POST":
		data = json.loads(request.body)
		stream = Announcement.objects.get(pk = data["id"])
		stream.delete()
		return JsonResponse({'message': "Success"})
	else:
		return HttpResponseRedirect(reverse('index'))

def see_assignment(request, id):
	if not request.user.is_authenticated:
		return render(request, "index/error.html", {
			"message": "You must Signed in",
			"signin": False
			})
	submitted = Submission.objects.filter(student = request.user, assignment_id = id).count()
	if request.method == "POST":
		assignment = Announcement.objects.get(pk = id)
		if submitted == 0:
			submission = Submission(submission = request.POST["answer"], assignment = assignment, student = request.user)
			submission.save()
		else:
			submission = Submission.objects.get(student = request.user, assignment = assignment)
			submission.delete()
	assignment = Announcement.objects.filter(pk = id)
	if assignment.count() == 0 or assignment[0].is_assignment == False:
		return render(request, "index/error.html", {
			"message": "You have no access to this page."
			})
	submitted = Submission.objects.filter(student = request.user, assignment_id = id).count()
	submittedvalue = None
	if submitted > 0:
		submittedvalue = Submission.objects.get(student = request.user, assignment_id = id).submission
	usertype = UserType.objects.get(user = request.user.id).accountType
	submissions = Submission.objects.filter(assignment_id = id)
	return render(request, "index/assignment.html", {
		"assignment": assignment[0],
		"id": id,
		"submitted": bool(submitted),
		"submittedvalue": submittedvalue,
		"usertype": usertype,
		"submissions": submissions
		})