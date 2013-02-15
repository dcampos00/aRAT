var refreshTimer;

function ajax(argument){
  Dajaxice.aRAT.apps.home.ste_update_alerts(argument);
  Dajaxice.aRAT.apps.home.pad_update_alerts(argument);
  Dajaxice.aRAT.apps.home.corr_update_alerts(argument);
  Dajaxice.aRAT.apps.home.clo_update_alerts(argument);
  Dajaxice.aRAT.apps.home.holo_update_alerts(argument);
}

function refresh(start, dajax_function){
  if (start == true) {
    clearInterval(refreshTimer);
    refreshTimer = null;  

    refreshTimer = setInterval(function(){
      dajax_function(Dajax.process);
    }, 3000);
  } else {
    clearInterval(refreshTimer);
    refreshTimer = null;  
  }
}

function removeAlert(alerts_container, resource_id) {
  alert = alerts_container.find("[data-id='"+resource_id+"']");
  if (alert.length > 0) {
    alert.remove();
  }
}

function updateAlert(alerts_div, type, text, id, read_only) {
    /* The default valuefor read_only is setted */
    read_only = typeof read_only !== 'undefined' ? read_only : false;

    alert_div = alerts_div.find("[data-id='"+id+"']");
    /* is proved if exist the alert */
    if (alert_div.length > 0) {
	/* if exist the content is updated */
	alert_div.children(".alert-text").html(text);
	alert_div.attr("class", "alert").addClass(type);
	if (read_only){
	    alert_div.find("button").remove();
	} else {
	    if (alert_div.find("button").length <= 0) {
		html_button = "<button type=\"button\" class=\"close close-alert\" data-dismiss=\"alert\">&times;</button>";
		alert_div.prepend( html_button );
	    }
	}
    } else {
	/* if does not exist the alert is created */
	html_alert = "<div class=\"alert "+type+"\" data-id=\""+id+"\">";
	if (!read_only) {
	    html_alert += "<button type=\"button\" class=\"close close-alert\" data-dismiss=\"alert\">&times;</button>";
	}
	html_alert += "<div class=\"alert-text\">"+text+"</div>";
	html_alert += "</div>";
	alerts_div.append( html_alert );
    }
}

function update_status(data){
    var tr = $("tr[data-resource-id='"+data.resource.id+"']");
    tr.removeClass("btn-danger btn-success");

    if (data.is_requested) {

	if(!data.resource.assigned){
	    data.requested_antenna.name = "None";
	    data.requested_antenna.id = "None";
	}

	tr.find(".text-antenna").text(data.requested_antenna.name).data("antennaId", data.requested_antenna.id);
	
	alerts = tr.parents(".tab-pane").find(".alerts-container");

	if (data.error){
	    alert_type = "alert-error";
            tr.addClass("btn-danger");	    
	} else {
	    alert_type = "alert-success";
	    tr.addClass("btn-success");
	}

	updateAlert(alerts, alert_type, data.status, data.resource.id, data.read_only);

    } else if (data.error) {
	alerts = tr.parents(".tab-pane").find(".alerts-container");

	alert_type = "alert-error";
        tr.addClass("btn-danger");	    

	/** this part of the code is very infrecuent that have real use **/
	tr.find(".text-antenna").text(data.current_antenna.name).data("antennaId", data.current_antenna.id);
	/** **/

	updateAlert(alerts, alert_type, data.status, data.resource.id, true);
    } else {
	alerts = tr.parents(".tab-pane").find(".alerts-container");
	alert_div = alerts.find("[data-id='"+data.resource.id+"']");
	if (alert_div.length > 0) {
	    alert_div.remove();
	}
	if(data.current_antenna.name == null){
	    data.current_antenna.name = "None";
	    data.current_antenna.id = "None";
	}
	tr.find(".text-antenna").text(data.current_antenna.name).data("antennaId", data.current_antenna.id);
    }
}
