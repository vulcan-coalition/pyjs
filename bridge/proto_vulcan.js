window.server = (function(){

	const request = new XMLHttpRequest();
	const app_prefix = "<%app_prefix>";

	var makeRequest = function (url, method, body) {
		return new Promise(function (resolve, reject) {
			request.onreadystatechange = function () {
				if (request.readyState !== 4) return;
				if (request.status >= 200 && request.status < 300) {
					resolve(request.response);
				} else {
					reject({
						status: request.status,
						statusText: request.statusText
					});
				}
			};
			request.open(method || 'POST', url, true);
			request.setRequestHeader("Content-Type", "application/json")
			request.send(JSON.stringify(body));
		});
	};
	makeRequest("/" + app_prefix + "/vulcan_start");
	return {
		//<%functions>
	};
})()