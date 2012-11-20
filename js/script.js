var server = "http://minionsme.appspot.com/";
var colleges;
var userID = "02";


$(document).ready(function(){
	refresh_countdown();
	$('#main_pannel_nav a').click(function (e) {
		newTab = $(this).attr('href');
		switch(newTab){
			case "#overview":
				load_overview();
				break;
			case "#colleges":
				load_colleges();
				break;
			case "#tests":
				load_tests();
				break;
			case "#other":
				load_other();
				break;
			case "#profile":
				load_profile();
				break;
		}		
  		$(this).tab('show');
	})
	$('#collegefilter').keyup(function () { 
		var key_word = (this.value).toLowerCase(), key;
		
		console.log(key_word);
		$("#addcolleges").empty();
	
		for (key in colleges) 
		{
			if(colleges[key]["Name"].toLowerCase().indexOf(key_word) != -1)
				$("#addcolleges").append('<option value="'+colleges[key]["School id"]+'">'
						+colleges[key]["Name"]+'</option>');
				
		}
		
	});	
	$("#addCollege").click(function(){

   		school_name = $("#addcolleges option:selected").text();
   		school_id = $("#addcolleges option:selected").attr("value");
   		var r=confirm("Press "+school_name+" to your application!");
		if (r==true){
		 	$.post("addPersonal", { ID: userID, schoolName: school_name, schoolID: school_id },
   				function(data) {
     				refresh_personal_colleges();
   				})
		 }
	
	});
 });

//show countdown on the side bar 
function refresh_countdown(){
	//get a list of personal colleges
	$("#upcoming-task").empty();
	$.ajax({					
		url: "/personal_colleges?id="+userID,
		dataType: 'json',
			success: function(data){
					load_schoolCountDown(data["colleges"]);
   		 }
   	 });
   	
	
	


}
function load_overview(){

}

//get the deadline for those colleges
function load_schoolCountDown(schools){
	//console.log(schools);
	var itemDeadlines= [];
	$i=0;
	
	for(var k in schools){

		$.ajax({					
		url: "/deadlines?id="+schools[k]["School id"],
		async: false,
		dataType: 'json',
			success: function(data){
					
				///	itemDeadlines[$i]["a"]= data["Deadlines"];
					//disregard all deadlines more than 100 days
					
					if((parseInt(data["Deadlines"]["Early Action Countdown"]) < 200) &&
						(parseInt(data["Deadlines"]["Early Action Countdown"]) >0)){
						itemDeadlines[$i]= new Object;
						itemDeadlines[$i].Name      = schools[k]["Name"] + " Early Action";
						itemDeadlines[$i].countdown = data["Deadlines"]["Early Action Countdown"];
					
 						$i++;
					}
					if((parseInt(data["Deadlines"]["Early Decision Countdown"]) < 200)&&
					(parseInt(data["Deadlines"]["Early Decision Countdown"]) > 0)){
						itemDeadlines[$i]= new Object;
						itemDeadlines[$i].Name = schools[k]["Name"] + " Early Decision";
						itemDeadlines[$i].countdown = data["Deadlines"]["Early Decision Countdown"];
						$i++;
					}
					if((parseInt(data["Deadlines"]["Regular Admission Countdown"]) < 200)&&
					(parseInt(data["Deadlines"]["Regular Admission Countdown"]) >0) ){
						itemDeadlines[$i]= new Object;
						itemDeadlines[$i].Name= schools[k]["Name"] + " Regular Admission";
						itemDeadlines[$i].countdown= data["Deadlines"]["Regular Admission Countdown"];
						$i++;
					
					}
	
					
				
	   		 }
	   	 });
	
	}
	itemDeadlines.sort(function (element_a, element_b) {
	    	return element_a.countdown - element_b.countdown;
		});
		
	
	console.log(itemDeadlines);
	for(var k in itemDeadlines){
	
		console.log(itemDeadlines[k].Name);
				$("#upcoming-task").append("<li class='deadline-date-header'>Count Down<div id='count-down'>"+itemDeadlines[k].countdown+"<span>days</span></div></li>");
		$("#upcoming-task").append("<li class='deadline-date-content'>"+itemDeadlines[k].Name+"</li>");

	}
	//print out
	
	
	
}
function refresh_personal_colleges(){
	$("#personalcolleges").empty();
	$.ajax({					
		url: "/personal_colleges?id="+userID,
		dataType: 'json',
			success: function(data){
					colleges = data["colleges"];
					for (var k in data["colleges"]) {
					$('#personalcolleges').append('<option value="' + data["colleges"][k]["School id"] 
								+ '">' + data["colleges"][k]["Name"] + '</option>');
			 	}
   	 }
   	 
});
refresh_countdown();
}

function load_colleges(){
	$("#addcolleges").empty();
	$("#filtercolleges").empty();
	$.ajax({					
		url: "/colleges",
		dataType: 'json',
			success: function(data){
					colleges = data["colleges"];
					for (var k in data["colleges"]) {
					$('#addcolleges').append('<option value="' + data["colleges"][k]["School id"] 
								+ '">' + data["colleges"][k]["Name"] + '</option>');
			 	}
   	 }
	});
	refresh_personal_colleges();
}

function load_tests(){
	$.ajax({					
		url: "/sat1?id="+userID,
		dataType: 'json',
			success: function(data){
			
					$("#sat1_content tbody").empty();
					for (var k in data["SATI_scores"]) {
						$("#sat1_content tbody").append("<tr><td>"+data["SATI_scores"][k]["Math_Score"]+"</td><td>"+data["SATI_scores"][k]["Reading_Score"]+"</td><td>"+data["SATI_scores"][k]["Writing_Score"]+"</td></tr>");
						
					}
					
					
			 	},
		error: function(xOptions, textStatus) {
        	alert("error..");
    	}
   	 
	});
	
	$.ajax({					
		url: "/sat2?id="+userID,
		dataType: 'json',
			success: function(data){
					$("#sat2_content tbody").empty();
					for (var k in data["SATII_scores"]) {
		
						$("#sat2_content tbody").append("<tr><td>"+data["SATII_scores"][k]["Subject"]+"</td><td>"+data["SATII_scores"][k]["Score"]+"</td></tr>");
						
					}
					
					
			 	},
		error: function(xOptions, textStatus) {
        	alert("error..");
    	}
   	 
	});

}
 //load others page
function load_other(){
	var eng_list = $("#english_requirement span");
	var math_list = $("#math_requirement span");
	var sci_list = $("#science_requirement span");
	var soc_list = $("#social_requirement span");
	var oth_list = $("#other_requirement span");
	
	eng_list.empty();
	math_list.empty();
	sci_list.empty();
	soc_list.empty();
	oth_list.empty();
	
	$.ajax({
		url: "/getAgReqs?id="+userID,
		dataType: 'json',
		success: function(data){
			for(var key in data){
				console.log(key);
				switch(key){
					case "Geometry":
					case "Algebra_II":
					case "Math_(Year_1)":
					case "Math_(Year_2)":
					case "Math_(Year_3)":
						append_ag(math_list, key, data[key]=="True");
						break;
					case "Biology":
					case "Chemistry":
					case "Physics":
					case "Science_(Year_1)":
					case "Science_(Year_2)":
					case "Science_(Year_3)":
						append_ag(sci_list, key, data[key]=="True");
						break;
					case "English_1":
					case "English_2":
					case "English_3":
					case "English_4":
						append_ag(eng_list, key, data[key]=="True");
						break;
					case "Foreign_Language_(Year_1)":
					case "Foreign_Language_(Year_2)":
					case "Foreign_Language_(Year_3)":
					case "Visual/Performing_Arts":
					case "Elective":
						append_ag(oth_list, key, data[key]=="True");
						break;
					case "US_History":
					case "World_History":
						append_ag(soc_list, key, data[key]=="True");
						break;
				}
			}
			
			//binding clicking event..
			eng_list.children().each(function(){
				$(this).on({
					click: function(){
					$v = $(this);
					$.post("editAG", { id: userID, req_name: $(this).attr("id") },
   						function(data) {
   	
   							if($v.hasClass("fullfilled"))
								$v.removeClass("fullfilled").addClass("notful");
							else
								$v.removeClass("notful").addClass("fullfilled");
     					
   					});
					
				}});
			});
			math_list.children().each(function(){
				$(this).on({
					click: function(){
					$v = $(this);
					$.post("editAG", { id: userID, req_name: $(this).attr("id") },
   						function(data) {
     					//refresh color
     					if($v.hasClass("fullfilled"))
								$v.removeClass("fullfilled").addClass("notful");
							else
								$v.removeClass("notful").addClass("fullfilled");
     					
   					});
				}});
			});
			sci_list.children().each(function(){
				$(this).on({
					click: function(){
					$v = $(this);
					$.post("editAG", { id: userID, req_name: $(this).attr("id") },
   						function(data) {
     					//refresh color
     					if($v.hasClass("fullfilled"))
								$v.removeClass("fullfilled").addClass("notful");
							else
								$v.removeClass("notful").addClass("fullfilled");
     					
   					});
				}});
			});
			oth_list.children().each(function(){
				$(this).on({
					click: function(){
					$v = $(this);
					$.post("editAG", { id: userID, req_name: $(this).attr("id") },
   						function(data) {
     					//refresh color
     					if($v.hasClass("fullfilled"))
								$v.removeClass("fullfilled").addClass("notful");
							else
								$v.removeClass("notful").addClass("fullfilled");
     					
   					});
				}});
			});
			soc_list.children().each(function(){
				$(this).on({
					click: function(){
					$v = $(this);
					$.post("editAG", { id: userID, req_name: $(this).attr("id") },
   						function(data) {
     					//refresh color
     					if($v.hasClass("fullfilled"))
								$v.removeClass("fullfilled").addClass("notful");
							else
								$v.removeClass("notful").addClass("fullfilled");
     					
   					});
				}});
			});
		},
		error: function(xOptions, textStatus) {
        	alert("error..");
    	}
	});
}

function flip($ref){
console.log($ref.attr("class"));
	
	
	
}
function append_ag( ref, name,val){
	var item;
	if(val){
		item="<li id= '"+name+"' class='selectAG fullfilled'>"+name.replace(/_/g ," ")+"</li>";
	}else{
		item="<li id= '"+name+"' class='selectAG notful'>"+name.replace(/_/g," ")+"</li>";
	}
	
	ref.append(item);
}


function edit_ag(){


}
function load_profile(){
	

}