$(document).ready(function() {
	$("#alert").hide()
	
	$("form").submit(function () {
		var message = $("#message").val()
		$("#message").val("")
		sendMessage(message)
		return false
	});
	
	
	getMessages();
	setCamera();
});

function setCamera(){

	var url = window.location.href + "camport";
	$.ajax({
		url: url,
		success: function(result) {
			var camUrl = window.location.href.replace(":" + window.location.port, ":" + result.cam_port);
			console.log(camUrl);
			$("#cam").attr("src", camUrl);
		}
	});
}

function getMessages(){
	var url = window.location.href + "messages";
	$.ajax({
		url: url,
		success: function(result) {
			$("#messages").empty();
			trHtml = "";
			$.each(result, function(i, item){
				var date = new Date(result[i].timestamp * 1000);
				var time = date.toLocaleTimeString([], {hour: "2-digit", minute:"2-digit"}).toLowerCase()
				var formattedDate = $.datepicker.formatDate("M d ", date) + " " + time;
				trHtml += "<tr><td class=\"date-td\">" + formattedDate + "</td><td class=\"result-td\" >" + result[i].message + "</td></tr>"
			});
			$("#messages").append(trHtml);
			$("#messages td").click(function(){
				var message = $(this).text();
				sendMessage(message)
			});
		}
	});
}

function sendMessage(message){
	var url = window.location.href + "send?message=" + message;
	$.ajax({
		url: url, 
		success: function(result) {
			$("#alert").removeClass("alert-danger").addClass("alert-success")
			showAlert()
			getMessages()
		}
	});
}

function showAlert(){
	$("#alert").slideDown().show()
	setTimeout(function() {
		$("#alert").slideUp()
	}, 5000);
}

function takePhoto(){
	var url = window.location.href + "capture";
	$.ajax({
		url: url, 
		success: function(result) {
			$("#alert").removeClass("alert-danger").addClass("alert-success");
			showAlert();
			getMessages();
		}
	});	
}

function goToGallery(){
	var url = window.location.href + "photos";
	window.location.href = url;
}
