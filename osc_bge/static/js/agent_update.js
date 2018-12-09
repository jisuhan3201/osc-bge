$(".RelationshipHistorySpanClass").click(function () {
  var history_id = $(this).attr('id').replace("RelationshipHistorySpan", "")
  if(history_id){
    $.ajax({                       // initialize an AJAX request
      url: "/agents/history/get/" + history_id,                    // set the url of the request (= localhost:8000/hr/ajax/load-cities/)
      success: function (data) {   // `data` is the return of the `load_cities` view function
        $("#PopRelationshipHistory input[name=relationship_history_id]").val(data[0].pk);
        $("#PopRelationshipHistory input[name=name]").val(data[0].fields.name);
        $("#PopRelationshipHistory input[name=location]").val(data[0].fields.location);
        $("#PopRelationshipHistory input[name=category]").val(data[0].fields.category);
        $("#PopRelationshipHistory input[name=priority]").val(data[0].fields.priority);
        $("#PopRelationshipHistory textarea[name=comment]").text(data[0].fields.comment);
        $("#PopRelationshipHistory").show();
      }
    });
  }
  else{
    alert('Review ID does not exist..')
  }
});

$("#PopRelationshipHistory .Close").click(function(){
  $("#PopRelationshipHistory input[name=relationship_history_id]").val("");
  $("#PopRelationshipHistory input[name=name]").val("");
  $("#PopRelationshipHistory input[name=location]").val("");
  $("#PopRelationshipHistory input[name=category]").val("");
  $("#PopRelationshipHistory input[name=priority]").val("");
  $("#PopRelationshipHistory textarea[name=comment]").text("");
  $("#PopRelationshipHistory").hide();
})
