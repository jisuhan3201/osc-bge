$(".CommunicationLogClass").click(function () {
  var log_id = $(this).attr('id').replace("CommunicationLog", "")
  if(log_id){
    $.ajax({                       // initialize an AJAX request
      url: "/branch/host/log/get/" + log_id,                    // set the url of the request (= localhost:8000/hr/ajax/load-cities/)
      success: function (data) {   // `data` is the return of the `load_cities` view function
        console.log(data)
        $("#PopCommunicationUpdate input[name=log_id]").val(data[0].pk);
        $("#PopCommunicationUpdate select[name=category]").val(data[0].fields.category);
        $("#PopCommunicationUpdate select[name=priority]").val(data[0].fields.priority);
        $("#PopCommunicationUpdate textarea[name=comment]").text(data[0].fields.comment);
        $("#PopCommunicationUpdate").show();
      }
    });
  }
  else{
    alert('Review ID does not exist..')
  }
});


$(".UpdateLogClass").click(function () {
  var log_id = $(this).attr('id').replace("UpdateLog", "")
  if(log_id){
    $.ajax({                       // initialize an AJAX request
      url: "/student/log/get/" + log_id,                    // set the url of the request (= localhost:8000/hr/ajax/load-cities/)
      success: function (data) {   // `data` is the return of the `load_cities` view function
        console.log(data)
        $("#PopStudentCommunicationUpdate input[name=log_id]").val(data[0].pk);
        $("#PopStudentCommunicationUpdate select[name=category]").val(data[0].fields.category);
        $("#PopStudentCommunicationUpdate select[name=priority]").val(data[0].fields.priority);
        $("#PopStudentCommunicationUpdate textarea[name=comment]").text(data[0].fields.comment);
        $("#PopStudentCommunicationUpdate").show();
      }
    });
  }
  else{
    alert('Review ID does not exist..')
  }
});
