$(document).ready(function(){
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
});

$("#Registration").click(function () {
  $("#PopRegistration").show()
});

$(".RegistrationForm").on('submit', function(){
  event.preventDefault();
  var formality_id = $("#FormalityId").val()
  var values = $(".RegistrationForm").serializeArray()
  values.push({"name":"type", "value":"registration"})
  create_registration(formality_id, values)
})

function create_registration(formality_id, values){
  $.ajax({
    url : "/agent/process/" + formality_id,
    type: "POST",
    data: values,
    success: function(json){
      $(".AddComment").empty()
      $(".AddComment").append(
        json.apply_at + " / " + json.school_count + " Schools, processing fee $" + json.payment_complete_fee + " payment completed"
      )
      $("#PopRegistration").hide()
    },
    error: function(err){
      alert(err)
    }
  })
}

$("#CancelRegistration").click(function () {
  $("#PopCancelRegistration").show()
});

$(".CancelRegistrationForm").on('submit', function(){
  event.preventDefault();
  var formality_id = $("#FormalityId").val()
  var values = $(".CancelRegistrationForm").serializeArray()
  values.push({"name":"type", "value":"cancel_registration"})
  cancel_registration(formality_id, values)
});

function cancel_registration(formality_id, values){
  $.ajax({
    url : "/agent/process/" + formality_id,
    type: "POST",
    data: values,
    success: function(json){
      $(".AddComment").empty()
      $("#PopCancelRegistration").hide()
    },
    error: function(err){
      alert(err)
    }
  })
}
