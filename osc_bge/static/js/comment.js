
// For update.html

$(".CommentButtonClass").click(function () {
    var student_id = $(this).attr('id').replace("CommentButtonId", "")
    if(student_id){
        $("#CommentInputFieldId").val(student_id)
    }
    else{
      alert('Review ID does not exist..')
    }
  });
  