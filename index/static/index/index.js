document.addEventListener("DOMContentLoaded", ()=>{
	document.querySelector('#home-link').addEventListener('click', () => switchpage('home'))
	document.querySelector('#news-link').addEventListener('click', () => switchpage('news'))
	if(document.querySelector("#loggedin").innerText !== "True"){
		document.querySelector('#login-link').addEventListener('click', () => switchpage('login'))
		document.querySelector('#login-form').onsubmit = ()=>{
			const csrf = Cookies.get('csrftoken');
			const username = document.querySelector('#input-username').value;
			const password = document.querySelector('#input-password').value;
			fetch('/', {
				method: 'POST',
				headers: {'X-CSRFToken': csrf},
				body: JSON.stringify({
					username: username,
					password: password
				})
			})
			.then(response=>response.json())
			.then(result=> {
				console.log(result);
				if (result['message']==='Login Success'){
					console.log(result["usertype"])
					if(result['usertype'] === "student"){
						window.location = '/class'
					}else{
						window.location = '/dashboard';
					}
				}
				else{

					document.querySelector("#message").innerHTML = result['message'];
				}
			})
			return false;
		}
	}
	document.querySelector("#login").style.display = "none";
	document.querySelector('#news').style.display = "none";
	document.querySelector('#login').style.display = "none";
	
})
function switchpage(page){
	document.querySelector('#home').style.display = "none";
	document.querySelector('#news').style.display = "none";
	document.querySelector('#login').style.display = "none";
	document.getElementById(page).style.display = "block";
}