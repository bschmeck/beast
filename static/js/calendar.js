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

function buildCalendar() {
    configAjax();
    $(".text")
    .bind("mouseover mouseout", function(event) {
        $(this).toggleClass("highlight", event.type === "mouseover");
    })
    .click(function() {
        var re = /workout_(\d+)/;
        var id = re.exec(this.id)[1];
        var rowid = $(this).closest(".row").attr("id");
        var w = this;
        $(".row").filter(":not(#" + rowid + ")").filter(":visible").hide("blind", "slow");
        $("#workout_desc").load("/workout/" + id + "/", function() {
            $("#workout:hidden").show("blind", "slow");
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
        $("#workout").hide("blind", "slow", function() {
            $(".row").filter(":hidden").show("blind", "slow");
        });
        return false;
    })
    .bind("mouseover mouseout", function(event) {
        $(this).toggleClass("highlight default");
    });
    $("#workout").hide();
}