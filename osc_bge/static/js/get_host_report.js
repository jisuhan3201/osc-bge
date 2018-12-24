$("#GetHostReportId").change(function () {
  var report_id = $(this).val();  // get the selected country ID from the HTML input
  if(report_id){
    $.ajax({                       // initialize an AJAX request
      url: "/student/host/report/"+report_id,                    // set the url of the request (= localhost:8000/hr/ajax/load-cities/)
      success: function (data) {   // `data` is the return of the `load_cities` view function
        console.log(data)
        var photo_list = []
        var file_list = []
        for (i=0; i<data.length; i++){
          if(data[i]["model"] == "branch.reportphoto"){
            photo_list.push(data[i]["fields"]["photo"])
            $("#HostReportHostPhoto").append(data[i]["fields"]["photo"])
          }
          if(data[i]["model"] == "branch.reportfile"){
            file_list.push(data[i]["fields"]["file"])
            $("#HostReportHostFile").append(data[i]["fields"]["file"])
          }
        }
        $("#HostReportHostName").text(data[1]["fields"]["name"])
        $("#HostReportHostAddress").text(data[1]["fields"]["address"])
        $("#HostReportHostContact").text(data[1]["fields"]["phone"] + " / " + data[1]["fields"]["email"])
        $("#HostReportHostRate").text(data[0]["fields"]["rate"])
        $("#HostReportHostImprovement").text(data[0]["fields"]["improvement"])
        $("#HostReportHostFluency").text(data[0]["fields"]["cultural_fluency"])
        $("#HostReportHostRules").text(data[0]["fields"]["house_rule_attitude"])
        $("#HostReportHostResponsibility").text(data[0]["fields"]["responsibility"])
        $("#HostReportHostCommunication").text(data[0]["fields"]["communication"])
        $("#HostReportHostHabit").text(data[0]["fields"]["sleeping_habits"])
        $("#HostReportHostAttendance").text(data[0]["fields"]["school_attendance"])
        $("#HostReportHostComment").text(data[0]["fields"]["comment"])
        $("#HostReportHostPhoto").text(photo_list)
        $("#HostReportHostFile").text(file_list + " / ")
        $("#HostReportId").val(data[0]["pk"])
      }
    });
  }
});
