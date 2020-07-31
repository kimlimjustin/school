document.addEventListener("DOMContentLoaded", ()=>{
	closeall();
	document.querySelector("#welcome").style.display = "block";
	document.querySelector("#blog-link").addEventListener('click', ()=>{
		closeall();
		document.querySelector('#blog').style.display = "block";
		document.querySelector("#create-blog-button").addEventListener('click', ()=>{
			document.querySelector("#cancel-create-blog").style.display = "block";
			document.querySelector("#create-blog").style.display = "block";
			document.querySelector("#create-blog-form").onsubmit = ()=>{
				const title = document.querySelector("#create-blog-title").value;
				const target = document.querySelector("#blog-target").value;
				const image = document.querySelector("#blog-image").value;
				const content = document.querySelector("#blog-content").value;
				const csrf = Cookies.get('csrftoken');
				fetch('/blog', {
					method: 'POST',
					headers: {"X-CSRFToken": csrf},
					body:  JSON.stringify({
						"title": title,
						"target": target,
						"image": image,
						"content": content
					})
				})
				.then(response => response.json())
				.then(result =>{
					if(result["message"]==="Blog Created Successfully"){
						window.location = "/blog"
					}
				})
				return false;
			}
			document.querySelector("#cancel-create-blog").addEventListener('click', ()=>{
				document.querySelector("#cancel-create-blog").style.display = "none";
				document.querySelector("#create-blog").style.display = "none";
			})
		})
	})
	document.querySelector("#classList-link").addEventListener('click', ()=>{
		closeall();
		document.querySelector("#classList").style.display = "block";
		document.querySelector("#create-class-button").addEventListener('click', ()=>{
			var temp = confirm("Are you sure to create a new class?")
			if (temp){
				document.querySelector("#cancel-create").style.display = "block";
				document.querySelector("#create-class").style.display = "block";
				document.querySelector("#cancel-create").addEventListener('click', ()=>{
					document.querySelector("#create-class").style.display = "none";
				})
				document.querySelector("#create-class-form").onsubmit = ()=>{
					const classlevel = document.querySelector("#classLevel").value;
					const classname = document.querySelector("#className").value;
					const csrf = Cookies.get('csrftoken');
					fetch('/dashboard', {
						method: "POST",
						headers: {"X-CSRFToken": csrf},
						body: JSON.stringify({
							"classlevel": classlevel,
							"classname": classname
						})
					})
					.then(response => response.json())
					.then(result => {
						if(result["message"]=== "Class created"){
							document.querySelector("#create-class-message").innerHTML = result['message'];
							var element = document.createElement("div");
							console.log("b");
							element.innerHTML = `<div class='class'><div class='card'><div class='card-body'><h5 class='class-title'>
							${classlevel} - ${classname}</h5><p class="card-text">Teached by: None</p>
							<a class="btn btn-dark" href="/dashboard/class/${classlevel}/${classname}">See class</a></div></div></div>`;
							document.querySelector("#classList").append(element);
							document.querySelector("#create-class").style.display = "none";
						}
					})
					return false;
				}
			}
		})
	})
	document.querySelector("#students-link").addEventListener('click', ()=>{
		closeall();
		document.querySelector("#students").style.display = "block";
		document.querySelector("#add-student-button").addEventListener('click', ()=>{
			document.querySelector("#add-student").style.display = "block";
			document.querySelector("#cancel-add-student").style.display = "block";
			document.querySelector("#add-student-form").onsubmit = ()=>{
				var username = document.querySelector("#add-student-username").value;
				var email = document.querySelector("#add-student-email").value;
				var password = document.querySelector("#add-student-password").value;
				var confirmation = document.querySelector("#add-student-password-confirmation").value;
				var studentID = document.querySelector("#add-student-studentID").value;
				var csrf = Cookies.get('csrftoken');
				var studentclass = document.querySelector("#add-student-class").value;
				if(confirmation != password){
					document.querySelector("#confirm-wrong").innerHTML = "Password must match."
				}else{
					fetch('/register', {
						method: "POST",
						headers: {"X-CSRFToken": csrf},
						body: JSON.stringify({
							"username": username,
							"email": email,
							"password": password,
							"userID": studentID,
							"class": studentclass,
							"accountType": "student"
						})
					})
					.then(response => response.json())
					.then(result=>{
						console.log(result);
						document.querySelector("#confirm-wrong").innerHTML = "";
						if(result["message"] !== "User Created Successfully"){
							document.querySelector("#add-student-message").innerHTML = result["message"];
						}else{
							const Class = result["class"];
							document.querySelector("#add-student").style.display = "none";
							var element = document.createElement("tr");
							element.innerHTML = `<td>${studentID}</td><td>${username}</td><td>${email}</td><td>${Class}</td>`;
							document.querySelector("#student-data").appendChild(element);
						}
					})
				}
				return false;
			}
			document.querySelector("#cancel-add-student").addEventListener("click", ()=>{
				document.querySelector("#cancel-add-student").style.display = "none";
				document.querySelector("#add-student").style.display = "none";
			})
		})
	})
	
	document.querySelector("#teacher-link").addEventListener('click', ()=>{
		closeall();
		document.querySelector("#teacher").style.display = "block";
		document.querySelector("#add-teacher-button").addEventListener('click', ()=>{
			document.querySelector("#add-teacher").style.display = "block";
			document.querySelector("#cancel-add-teacher").style.display = "block";
			document.querySelector("#add-teacher-form").onsubmit = ()=>{
				var username = document.querySelector("#add-teacher-username").value;
				var email = document.querySelector("#add-teacher-email").value;
				var password = document.querySelector("#add-teacher-password").value;
				var confirmation = document.querySelector("#add-teacher-password-confirmation").value;
				var userID = document.querySelector("#add-teacher-userID").value;
				var teachingClass = document.querySelector("#add-teacher-class").value;
				var csrf = Cookies.get('csrftoken');
				if(confirmation != password){
					document.querySelector("#confirm-wrong").innerHTML = "Password must match."
				}
				else{
					fetch('/register', {
						method: "POST",
						headers: {"X-CSRFToken": csrf},
						body: JSON.stringify({
							"username": username,
							"email": email,
							"password": password,
							"userID": userID,
							"class": teachingClass,
							"accountType": "teacher"
						})
					})
					.then(response => response.json())
					.then(result => {
						if(result["message"]=== "Teacher added Successfully"){
							document.querySelector("#add-teacher").style.display = "none";
							var element = document.createElement("tr")
							element.innerHTML = `<td>${userID}</td><td>${username}</td><td>${email}</td>`;
							document.querySelector("#teacher-data").appendChild(element);
						}
					})
				}
				return false;
			}
			document.querySelector("#cancel-add-teacher").addEventListener('click', ()=>{
				document.querySelector("#cancel-add-teacher").style.display = "none";
				document.querySelector("#add-teacher").style.display = "none";
			})
		})
	})
})

function closeall(){
	document.querySelector("#welcome").style.display = "none";
	document.querySelector("#blog").style.display = "none";
	document.querySelector("#classList").style.display = "none";
	document.querySelector("#students").style.display = "none";
	document.querySelector("#teacher").style.display = "none";
}