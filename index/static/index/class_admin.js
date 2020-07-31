document.addEventListener("DOMContentLoaded", ()=>{
	const usertype = document.querySelector("#usertype").innerText
	document.querySelector("#assignment").style.display = "none";
	document.querySelector("#teacher").style.display = "none";
	document.querySelector("#stream").style.display = "none";
	if(usertype !== "admin" && usertype!== "teacher"){
		window.location = "/";
	}
	if(usertype === "admin"){
		document.querySelector("#teacher-link").addEventListener('click', ()=>{
			document.querySelector("#teacher").style.display = "block";
			document.querySelector("#welcome").style.display = "none";
			document.querySelector("#assignment").style.display = "none";
			document.querySelector("#stream").style.display = "none";
			document.querySelector("#add-teacher-button").addEventListener('click', ()=>{
				document.querySelector("#add-teacher").style.display = "block";
				document.querySelector("#cancel-add-teacher").addEventListener('click', ()=>{
					document.querySelector("#add-teacher").style.display = "none";
				})
				document.querySelector("#add-teacher-form").onsubmit = ()=>{
					var teacher = document.querySelector("#add-teacher-teacher").value;
					var csrf = Cookies.get('csrftoken');
					fetch('/add_teacher', {
						method: "POST",
						headers: {'X-CSRFToken': csrf},
						body: JSON.stringify({
							teacher: teacher,
							classlevel: document.querySelector("#classlevel").innerText,
							classname: document.querySelector("#classname").innerText
						})
					})
					.then(response => response.json())
					.then(result => {
						if(result["message"] === "Success"){
							document.querySelector("#add-teacher").style.display = "none";
							var element = document.createElement("LI");
							element.innerText = result["teacher"];
							document.querySelector("#teacher-lists").appendChild(element);

						}
					})
					return false;
				}
			})
		})
	}
	document.querySelector("#assignment-link").addEventListener('click', ()=>{
		document.querySelector("#welcome").style.display = "none";
		document.querySelector("#assignment").style.display = "block";
		document.querySelector("#teacher").style.display = "none";
		document.querySelector("#stream").style.display = "none";
		document.querySelector("#add-assignment-button").addEventListener("click", ()=>{
			document.querySelector("#add-assignment").style.display = "block";
			document.querySelector("#cancel-add-assignment").addEventListener('click', ()=>{
				document.querySelector("#add-assignment").style.display = "none";
			})
			document.querySelector("#add-assignment-form").onsubmit = ()=>{
				var csrf = Cookies.get('csrftoken');
				var title = document.querySelector("#add-assignment-title").value;
				var assignment = document.querySelector("#add-assignment-assignment").value;
				var attachment = document.querySelector("#add-assignment-attachment").value;
				var duedate_date = document.querySelector("#add-assignment-duedate-date").value;
				var duedate_time = document.querySelector("#add-assignment-duedate-time").value;
				fetch('/add_assignment', {
					method: "POST",
					headers: {'X-CSRFToken': csrf},
					body: JSON.stringify({
						title: title,
						assignment: assignment,
						attachment: attachment,
						duedate_date: duedate_date,
						duedate_time: duedate_time,
						classlevel: document.querySelector("#classlevel").innerText,
						classname: document.querySelector("#classname").innerText
					})
				})
				.then(response => response.json())
				.then(result => {
					if(result["message"]==="Success"){
						document.querySelector("#add-assignment").style.display = "none";
						var element = document.createElement("div");
						element.setAttribute("class", "card assignment");
						element.innerHTML = `<div class="card-body"><h1 class="card-title">${title}</h1><p>Created on ${result["time"]}</p><hr />
						<div class="card-text">${assignment}</div><p><strong>Attachment:</strong></p><a href="${attachment}">${attachment}</a></div>`;
						document.querySelector("#assignment-list").appendChild(element);
					}
				})
				return false;
			}
		})
		document.querySelectorAll("#delete-assignment-button").forEach((assignmentDelete)=>{
			assignmentDelete.addEventListener('click', function(){
				var csrf = Cookies.get('csrftoken');
				fetch('/delete', {
					method: "POST",
					headers: {'X-CSRFToken': csrf},
					body: JSON.stringify({
						id: this.dataset.deleteAssignment
					})
				})	
				.then(response => response.json())
				.then(result => {
					if(result["message"]==="Success"){
						var element = document.querySelector(`#assignment-${this.dataset.deleteAssignment}`);
						element.parentNode.removeChild(element);
					}
				})
			})
		})
	})
	document.querySelector("#stream-link").addEventListener('click', ()=>{
		document.querySelector("#welcome").style.display = "none";
		document.querySelector("#assignment").style.display = "none";
		document.querySelector("#teacher").style.display = "none";
		document.querySelector("#stream").style.display = "block";
		document.querySelector("#add-stream-button").addEventListener('click', ()=>{
			document.querySelector("#add-stream").style.display = "block";
			document.querySelector("#cancel-add-stream").addEventListener('click', ()=>{
				document.querySelector("#add-stream").style.display = "none";
			})
			document.querySelector("#add-stream-form").onsubmit = ()=>{
				var csrf = Cookies.get('csrftoken');
				var title = document.querySelector("#add-stream-title").value;
				var stream = document.querySelector("#add-stream-stream").value;
				var attachment = document.querySelector("#add-stream-attachment").value;
				fetch('/add_stream', {
					method: "POST",
					headers: {'X-CSRFToken': csrf},
					body: JSON.stringify({
						title: title,
						stream: stream,
						attachment: attachment,
						classlevel: document.querySelector("#classlevel").innerText,
						classname: document.querySelector("#classname").innerText
					})
				})
				.then(response => response.json())
				.then(result => {
					if(result["message"]==="Success"){
						document.querySelector("#add-stream").style.display = "none";
						var element = document.createElement("div");
						element.setAttribute("class", "card stream");
						element.innerHTML = `<div class="card-body"><h1 class="card-title">${title}</h1><p>Created on ${result["time"]}</p><hr />
						<div class="card-text">${stream}</div><p><strong>Attachment:</strong></p><a href="${attachment}">${attachment}</a></div>`;
						document.querySelector("#stream-list").appendChild(element);
					}
				})
				return false;
			}
		})
		document.querySelectorAll("#delete-stream-button").forEach((streamDelete)=>{
			streamDelete.addEventListener('click', function(){
				var csrf = Cookies.get('csrftoken');
				fetch('/delete', {
					method: "POST",
					headers: {'X-CSRFToken': csrf},
					body: JSON.stringify({
						id: this.dataset.deleteStream
					})
				})	
				.then(response => response.json())
				.then(result => {
					if(result["message"]==="Success"){
						var element = document.querySelector(`#stream-${this.dataset.deleteStream}`);
						element.parentNode.removeChild(element);
					}
				})
			})
		})
	})
})
function delete_teacher(id, teacher){
	var temp = confirm(`Are you sure to delete ${teacher}?`);
	const csrf = Cookies.get('csrftoken');
	if(temp){
		fetch('/remove_teacher', {
			method: "POST",
			headers: {'X-CSRFToken': csrf},
			body: JSON.stringify({
				teacher: id,
				classlevel: document.querySelector("#classlevel").innerText,
				classname: document.querySelector("#classname").innerText
			})
		})
		.then(response => response.json())
		.then(result =>{
			if(result["message"] === "Success"){
				const element = document.querySelector(`#add-teacher-${id}`);
				element.parentNode.removeChild(element);
			}
		})
	}
}