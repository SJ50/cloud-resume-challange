var APIURL = "https://bwb1tlk55g.execute-api.ap-southeast-2.amazonaws.com/Prod/count/"
fetch(APIURL)
	.then(response => response.text())
	.then((response) => {
	document.getElementById("visits").innerHTML = response;
	})
