let currentslide = 1
document.addEventListener("DOMContentLoaded", ()=>{
	try{
		showpage(currentslide);
		document.querySelectorAll("#edit-blog-button").forEach((blog)=>{
			blog.addEventListener("click", function(){
				document.querySelector("#edit-blog").style.display = "block";
				document.querySelector("#paginationList").style.display = "none";
				document.querySelectorAll(".page").forEach((page)=> page.style.display = "none");
				document.querySelector("#blog-title").style.display = "none";
				const blogID = this.getAttribute('data-edit');
				document.querySelector("#edit-blog-id").value = blogID;
				document.querySelector("#edit-blog-title").value = document.querySelector(`#blog-title-${blogID}`).innerText;
				document.querySelector("#edit-blog-content").value = document.querySelector(`#blog-content-${blogID}`).innerText;
				document.querySelector("#cancel-edit-blog").addEventListener("click", ()=>{
					document.querySelector("#edit-blog").style.display = "none";
					document.querySelectorAll(".page").forEach((page)=> page.style.display = "block")
					document.querySelector("#paginationList").style.display = "block";
					document.querySelector("#blog-title").style.display = "block";
				})
			})
		})
	}catch{}
	document.querySelector("#edit-blog-form").onsubmit = ()=>{
		const csrf = Cookies.get('csrftoken');
		const newtitle = document.querySelector("#edit-blog-title").value;
		const newcontent  = document.querySelector("#edit-blog-content").value;
		const blogID = document.querySelector("#edit-blog-id").value;
		fetch('/edit', {
			method: "POST",
			headers: {'X-CSRFToken': csrf},
			body: JSON.stringify({
				title: newtitle,
				content: newcontent,
				id: blogID
			})
		})
		.then(response => response.json())
		.then(result => {
			if(result["message"] === "Success"){
				document.querySelector(`#blog-title-${blogID}`).innerText = newtitle;
				document.querySelector(`#blog-content-${blogID}`).innerText = newcontent;
				document.querySelector("#page1").style.display = 'block';
				document.querySelector("#paginationList").style.display = "block";
				document.querySelector("#edit-blog").style.display = "none";
			}
		})
		return false;
	}
	document.querySelector("#previous").addEventListener('click', () => {
		if(currentslide > 1){
			showpage(currentslide-1);
		}
	})
	document.querySelector("#next").addEventListener('click', () => {
		const totalpage = document.querySelectorAll('.page').length;
		if(currentslide < totalpage){
			showpage(currentslide+1);
		}
	})
})
function showpage(page){
	document.querySelectorAll(".page").forEach((pg)=>{
		pg.style.display = "none";
		currentslide = page

	})
	document.querySelector("#page"+page).style.display = "block";
}