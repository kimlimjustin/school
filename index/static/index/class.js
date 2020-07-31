document.addEventListener('DOMContentLoaded', ()=>{
	document.querySelector("#streams-link").addEventListener('click', ()=> showpage('streams'));
	document.querySelector("#classmates-link").addEventListener('click', ()=> showpage('classmates'));
	showpage("streams");
})
function showpage(page){
	document.querySelector("#streams").style.display = "none";
	document.querySelector("#streams").style.display = "none";
	document.querySelector("#classmates").style.display = "none";
	document.querySelector(`#${page}`).style.display = "block";
}