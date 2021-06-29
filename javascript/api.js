var URL = "https://kaptotpr8c.execute-api.ap-southeast-2.amazonaws.com/Prod/Visitors-Count"
fetch(URL)
	.then(response => response.text())
	.then((response) => {
	document.getElementById("visits").innerHTML = response;
	})