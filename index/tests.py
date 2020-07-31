from django.test import TestCase, Client

from .models import User, UserType, Blog, Class, Teacher, Student, Announcement, Attachment, Submission
# Create your tests here.
class TestIndex(TestCase):
	def setUp(self):
		user1 = User.objects.create_user(username = "hi", password = "hipasword", email = "hi@example.com", userID = "0")
		user1type = UserType(user = user1, accountType = "admin")
		user1type.save()
		user2 = User.objects.create_user(username = "hello", password = "hellopassword", email = "hello@example.com", userID = "1")
		user2type = UserType(user = user2, accountType = "teacher")
		user2type.save()
		user3 = User.objects.create_user(username = "student1", password = "student1password", email = "student1@example.com", userID = "1")
		user3type  = UserType(user = user3, accountType = "student")
		user3type.save()
		user4 = User.objects.create_user(username = "student2" ,password = "student2password", email = "student2@example.com", userID = "2")
		user4type = UserType(user = user4, accountType = "student")
		user4type.save()
		user5 = User.objects.create_user(username ="student3", password = "student3password", email= "student3@example.com", userID  = "3")
		user5type = UserType(user = user5, accountType = "student")
		user5type.save()

		class1 = Class(classLevel = "1", className = "1")
		class1.save()


	def test_page_response(self):
		c = Client()
		index  = c.get("/")
		self.assertEqual(index.status_code, 200)
		dashboard = c.get("/dashboard")
		self.assertEqual(dashboard.status_code, 200)
		register = c.get("/register")
		self.assertEqual(register.status_code, 302)
		blog = c.get("/blog")
		self.assertEqual(blog.status_code, 200)
		add_teacher = c.get("/add_teacher")
		self.assertEqual(add_teacher.status_code, 302)
		remove_teacher = c.get("/remove_teacher")
		self.assertEqual(remove_teacher.status_code, 302)
		edit_blog = c.get("/edit")
		self.assertEqual(edit_blog.status_code, 302)
		add_stream = c.get("/add_stream")
		self.assertEqual(add_stream.status_code, 302)
		add_assignment = c.get("/add_assignment")
		self.assertEqual(add_assignment.status_code, 302)

	def test_pagination(self):
		for i in range(100):
			blog = Blog(image = f"https://test.com/{i}", title = {i}, content = {i}, target = "All")
			blog.save()
			news = Blog(image = f"https://test/com/{i}", title = {i}, content = {i}, target = "News")
			news.save()
		c = Client()
		blog = c.get("/blog")
		self.assertEqual(blog.context["totalpage"], 10)
		news = c.get("/")
		self.assertEqual(news.context["totalpage"], 10)

	def test_class(self):
		c = Client()
		logged_in = c.login(username = "student1", password = "student1password")
		self.assertTrue(logged_in)
		user1 = User.objects.get(username = "student1")
		user2 = User.objects.get(username = "student2")
		user3 = User.objects.get(username = "student3")
		class1 = Class.objects.get(classLevel = "1", className = "1")
		Student.objects.create(name = user1, Class = class1)
		Student.objects.create(name = user2, Class = class1)
		Student.objects.create(name = user3, Class = class1)
		Class_view = c.get("/class")
		index = 0
		userlist = [user1, user2, user3]
		for i in Class_view.context["students"]:
			self.assertEqual(i.name, userlist[index])
			index +=1
			