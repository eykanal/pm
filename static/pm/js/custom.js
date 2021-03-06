"use strict";

//
// SITE INTERACTIVITY
//

$('.project-name').on("click", function(event){
	$(".project-info").hide();  // ensure all other views are hidden
	$("#project-info-" + event.currentTarget.dataset.id).show();
});

//
// AJAX CONTENT
//

// ### SEE https://docs.djangoproject.com/en/dev/ref/csrf/ FOR DETAILS ON THE FOLLOWING ###
// The following code ensures that the CSRF token is properly inserted in the header of the AJAX request
// Note: I "simplified" (i.e., reduced and probably obfuscated) the code

$.ajaxSetup({
	beforeSend: function(xhr, settings) {
		// the listed HTTP methods do not require CSRF protection
		if (!(/^(GET|HEAD|OPTIONS|TRACE)$/.test(settings.type)) && !this.crossDomain) {
			xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
		}
	}
});

// ### END AJAX HEADER CONTENT

// new project
$('#create-project').on('submit', function(event){
	event.preventDefault();

	$.ajax({
			url: "create_project",
			type: "POST",
			dataType: "json",
			data: $('#create-project').serialize(),
			success: function(json) {
				$('#create-project').trigger('reset'); // remove the value from the input
				$('#newProj').modal('hide');
			},
			error: function(xhr,errmsg,err) {
				$('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: " + errmsg + "<a href='#' class='close'>&times;</a></div>");
				console.log(xhr.status + ": " + xhr.responseText);
			}
		});
	});