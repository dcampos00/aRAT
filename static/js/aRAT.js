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

    if (data.requested_antenna.id != null || 
	(data.current_antenna.id != null && data.resource.assigned == false)) {

	if(data.resource.assigned == false){
	    data.requested_antenna.name = "None";
	    data.requested_antenna.id = "None";
	}

	tr.find(".text-antenna").text(data.requested_antenna.name).data("antennaId", data.requested_antenna.id);
	
	alerts = tr.parents(".tab-pane").find(".alerts-container");

	if (data.error == false ){
	    alert_type = "alert-success";
	    tr.addClass("btn-success");
	} else {
	    alert_type = "alert-error";
            tr.addClass("btn-danger");
	}
/*	if(data.resource.assigned == true){
	    alert_text = data.requested_antenna.name+" will be changed to "+data.resource.name;
	} else {
	    alert_text = "The PAD "+data.resource.name+" will be unassigned";
	}
	
	if (data.error != null){
            alert_type = "alert-error";
            tr.removeClass("btn-success").addClass("btn-danger");
            alert_text += data.error;
	}
	
	alert_text += " -- Request done by "+data.user.first_name+" "+data.user.last_name;
	alert_text += " on "+data.datetime.date+" at "+data.datetime.time;*/

	
	updateAlert(alerts, alert_type, data.status, data.resource.id, data.read_only);
	
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
