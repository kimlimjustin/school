from django.contrib.auth.models import AbstractUser
from django.db import models
# Create your models here.
class User(AbstractUser, models.Model):
    userID = models.IntegerField()

class UserType(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "user")
	accountType = models.CharField(max_length = 300)

class Blog(models.Model):
	image = models.CharField(max_length = 300)
	title = models.CharField(max_length = 300)
	content = models.CharField(max_length = 10000)
	target = models.CharField(max_length = 100)
	timestamp = models.DateTimeField(auto_now_add=True)
	def serialize(self):
		return{
			"timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p")
		}

class Class(models.Model):
	classLevel = models.IntegerField()
	className = models.CharField(max_length = 50)

class Teacher(models.Model):
	teacher = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "teacher")
	teaching = models.ForeignKey(Class, on_delete = models.CASCADE, related_name = "teaching")

class Student(models.Model):
	Class = models.ForeignKey(Class, on_delete = models.CASCADE, related_name="Class")
	name = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "name")

class Announcement(models.Model):
	announcement = models.CharField(max_length = 10000)
	title = models.CharField(max_length = 500)
	timestamp = models.DateTimeField(auto_now_add = True)
	is_assignment = models.BooleanField(default = False)
	duedate = models.DateTimeField(null = True)
	creator = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "creator")
	target = models.ForeignKey(Class, on_delete = models.CASCADE, related_name = "target")
	def serialize(self):
		return{
			"timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
			"duedate": self.timestamp.strftime("%b %d %Y, %I:%M %p")
		}

class Attachment(models.Model):
	target_attachment = models.ForeignKey(Announcement, on_delete = models.CASCADE, related_name ="target_attachment")
	attachment = models.CharField(max_length = 1000)

class Submission(models.Model):
	submission = models.CharField(max_length = 1000)
	assignment = models.ForeignKey(Announcement, on_delete = models.CASCADE, related_name = "assignment")
	timestamp = models.DateTimeField(auto_now_add = True)
	student = models.ForeignKey(User, on_delete = models.CASCADE, related_name="student")