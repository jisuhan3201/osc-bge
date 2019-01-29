
function getCookie(name)
  {
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

  $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                // Only send the token to relative URLs i.e. locally.
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        }
  });



$(".CommentButtonClass").click(function () {
    $("#PopCommentHistory").show()
    var student_id = $(this).attr('id').replace("CommentButtonId", "")
    if(student_id){
      $.ajax({                       // initialize an AJAX request
        url: "/student/comment/log/get/" + student_id,                    // set the url of the request (= localhost:8000/hr/ajax/load-cities/)
        success: function (data) {   // `data` is the return of the `load_cities` view function
        var trHtml = '';
        var csrftoken = getCookie('csrftoken')
        $.each(data, function(i, item){
          trHtml += '<tr><td>' + item['fields']["created_at"] + '</td><td>' + item['fields']["comment"] + '</td><td>' +
          "<form method='POST'>" +
          "<input type='hidden' name='csrfmiddlewaretoken' value='" + csrftoken + "'>" +
          "<input type='text' name='delete_comment' value='" + item['pk'] + "' hidden><button class='Button' type='submit'>DEL</button></form>" + '</td></tr>';
        })
        $('#comment_table').append(trHtml)
        }
      });

      $("#CommentInputFieldId").val(student_id)
    }
    else{
      alert('Review ID does not exist..')
    }
  });