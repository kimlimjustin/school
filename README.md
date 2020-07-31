# School ~ Final project

### This is a school website project. This Projects combines Google Classroom features, Blogs and others.

Features of this website:
- Home ~ Introducting the school
- Blog ~ List of Blogs that created by the school admin
- News ~ News that created by admin of website
- Login ~ Login for school admin, teacher and student. 
- Dashboard ~ A admin panel for admin to create blogs, class, add students and add teacher
- Class Dashboard ~ A admin panel for teacher to create Assignment and to create Announcement and for admin to add additional teacher to the class.
- Class ~ A page for student to see the announcements and assignments given by their teacher
- Assignment ~ A page for student to answer the assignments and for teacher to see their students answer

Specification of this website:
- Role:
	- Admins are able to create Blog, Class, add Student, add Assignment and add teacher
	- Teachers are able to view Blogs, Classes, Students that they thaught but not able to create those. Besides, teachers are able to see list of other teachers inside the Dashboard feature.
	- Teachers and admins are able to create announcements and assignments to their students. 
	- Students are able to see their Assignments and their teacher. They can also read Blogs that created by admin too.
	- Students are able to answer their assignments on the Class feature.
	- Guest can only see the school profile and read news and blogs.
	- NB: Only admins who are able to create Blogs and News for the school.
- Description of each file:
	- Inside templates/index/index.html, there is a main page for the website, Home Page, News page and login page.
	- Blogs are created using templates/index/blog.html and static/index/blog.js to manipulate the HTML Page
	- Whenever the user visit the page that they should not able to, they will be rendered to templates/index/error.html
	- The assignment page is created using templates/index/assignment.html.
	- templates/index/panel.html and static/index/dashboard.js are used for creating the admin panel, templates/index/class_admin.html and static/index/class_admin.js are used for Class Dashboard.