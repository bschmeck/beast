function configAjax() {
    $(document).ajaxSend(function(event, xhr, settings) {
        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
        function sameOrigin(url) {
            // url could be relative or scheme relative or absolute
            var host = document.location.host; // host + port
            var protocol = document.location.protocol;
            var sr_origin = '//' + host;
            var origin = protocol + sr_origin;
            // Allow absolute or scheme relative URLs to same origin
            return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
                (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
                // or any other URL that isn't scheme relative or absolute i.e relative.
                !(/^(\/\/|http:|https:).*/.test(url));
        }
        function safeMethod(method) {
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        }

        if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    });
}

function buildAccount() {
    configAjax();
    $("#updateInfo").click(function(event) {
	    event.preventDefault();
	    $.post("/account/update/", $("#updateForm").serialize(), function(data) {
		    if (data.success) {
			alert("Info successfully updated.");
		    } else {
			alert("Error: " + data.msg);
		    }
		}, "json");
	});
}

function buildEdit(locations) {
	$(".datePicker").datepicker({
        onSelect: function(dateText, inst) {
            /* Just hardcode this for now.  Could be more elegant. */
            $("#id_startTime").focus();
        }
    });
	
    /* Configure popovers for each part of the form. */
    var opt = {
        trigger: 'focus',
        html: true,
        content: 'content'
    };
    $("input, textarea, select").popover(opt);

	$("#id_city").attr({
	    title: 'Workout City',
	    content: "Choose a city for this workout."
	}).change(function(elt) {
        var locs = locations[$(this).val()];
        var content = "<p>Set the location for the workout.  You can choose from one of the standard locations or specify one of your own.</p>";
        var names = [];
        content += "<p>The standard location choices are:</p><ul>";
        for (var i = 0; i < locs.length; i++) {
            names.push(locs[i]["name"]);
            content += "<b><li>" + locs[i]["name"] + "<li></b>" + locs[i]["description"] + "</ul>";            
        }
        $("#id_location").attr({
            title: 'Workout Location',
            content: content
        }).autocomplete({
            source: [names.join(",")],
            minLength: 0
        });
    });
	$("#id_title").attr({
	    title: 'Workout Title',
	    content: "Give a short title to the workout."
	});
	$("id_startDate").attr({
	    title: 'Workout Date',
	    content: "Set the date for this workout."
	});
	$("#id_startTime").attr({
	    title: 'Workout Time',
	    content: "<p>Set the time when the workout will start (the 'go' time.)</p><p>Valid time formats are:</p><ul><li>7:00 am</li><li>9:30 pm</li><li>7:00am</li><li>9:30pm</li><li>7am</li><li>9pm</li><li>7:00</li><li>21:30</li></ul>"
	});
	$("#id_location").attr({
	    title: 'Workout Location',
	    content: "<p>Set the location for the workout.  You can choose from one of the standard locations or specify one of your own.</p>"
	});
	$("#id_warmupTime").attr({
	    title: 'Warmup Time',
	    content: "<p>Set the time when the warmup for the workout will start</p><p style='color: #c00;'>This is optional.</p><p>Valid time formats are:</p><ul><li>7:00 am</li><li>9:30 pm</li><li>7:00am</li><li>9:30pm</li><li>7am</li><li>9pm</li><li>7:00</li><li>21:30</li></ul>"
	});
	$("#id_description ").attr({
	    title: 'Workout Description',
	    content: "Set any details related to this workout, such as pacing, route, etc."
	});
	$("#id_notify_organizer").attr({
	    title: 'Add/Drop Notify',
		content: "Receive an email whenever anyone joins or drops the workout."
	});

    $("#id_location").bind("focus", function(event, ui) {
      $(this).autocomplete("search");
    });
    
    $("input[type='text']:first").focus();

}

function buildCalendar() {
    configAjax();
    $(".cell.in_past").height($("#week_1").css('height'));
    $(".text")
        .bind("mouseover mouseout", function(event) {
            $(this).toggleClass("highlight", event.type === "mouseover");
        })
        .click(function() {
            var re = /workout_(\d+)/;
            var id = re.exec(this.id)[1];
            var weekid = $(this).closest(".week").attr("id");
            var w = this;
            $(".week").filter(":not(#" + weekid + ")").filter(":visible").hide("blind", "slow");
            $("#workout_desc").load("/workout/" + id + "/", function() {
	            $("#workout:hidden").show("blind", "slow", function() {
		            $("#workout_close").bind("mouseover mouseout", function(event) {
	                    $(this).toggleClass("highlight default");
		            });
	            });
                $("a[rel=twipsy]").twipsy({
                    live: true
                });
            $(".workout_action").click(function(event) {
                event.preventDefault();
                var action = event.target.id;
                $.post("/workout/" + id + "/action/", {"action": action}, function(data) {
                    $("#confirmed").text(data.confirmed);
                    $("#interested").text(data.interested);
                    $("#join, #maybe, #drop").attr("disabled", "disabled");
                    if (data.showJoin) {
                        $("#join").removeAttr("disabled");
                    }
                    if (data.showMaybe) {
                        $("#maybe").removeAttr("disabled");
                    }
                    if (data.showDrop) {
                        $("#drop").removeAttr("disabled");
                    }
                    if (action === "join") {
			            $(w).addClass("mine");
			            alert("You have joined this workout.");
		            } else if (action === "maybe") {
			            $(w).addClass("mine");
			            alert("You are a 'maybe' for this workout.");                       
                    } else {
                        $(w).removeClass("mine");
			            alert("You have dropped out of this workout.");                       
                    }
                    $(w).html(data.cellText);
                }, "json");
            });
            });
        });
    $("#workout_close").click(function() {
        $(this).toggleClass("highlight", false);
        $(this).toggleClass("default", true);
	    $(this).unbind("mouseover mouseout");
        $("#workout").hide("blind", "slow", function() {
            $(".week").filter(":hidden").show("blind", "slow");
        });
        return false;
    });
    $("#workout").hide();
	$("#workout_close").trigger("click");
    $("#toggle_link").click(function() {
        $("#alt_cities").toggle();
        $("#hidden_text").toggle();
        $("#shown_text").toggle();
    });
}

function delWorkout(id) {
    var r = confirm("Are you sure you wish to delete this workout?");
    if (!r) {
	    return;
    }
    $.post("/workout/" + id + "/delete/", function(data) {
	    if (data.success) {
		    alert("Workout successfully deleted.");
		    $("#workout_close").trigger("click");
		    $("#workout_" + id).remove();
	    } else {
		    alert("Unable to delete workout: " + data.errMsg);
	    }
	}, "json");
}
