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

$("#CancelRegistration").click(function () {
  $("#PopCancelRegistration").show()
});

$(".EnrolmentLabelClass").click(function(){
  var formality_id = $(this).attr('id').replace("EnrolmentLabel", "")
  $('#PopEnrolmentApplication' + formality_id).show()
})

$(".SchoolInterviewLabelClass").click(function(){
  var formality_id = $(this).attr('id').replace("SchoolInterviewLabel", "")
  $('#PopSchoolinterview' + formality_id).show()
})

$(".AcceptanceLabelClass").click(function(){
  var formality_id = $(this).attr('id').replace("AcceptanceLabel", "")
  $('#PopAccepted' + formality_id).show()
})

$(".CancelEnrolmentLabelClass").click(function(){
  var formality_id = $(this).attr('id').replace("CancelEnrolmentLabel", "")
  $('#PopCancelEnrolment' + formality_id).show()
})

$(".I20RequestLabelClass").click(function(){
  var formality_id = $(this).attr('id').replace("I20RequestLabel", "")
  $('#PopI20Request' + formality_id).show()
})

$(".I20ReceivedLabelClass").click(function(){
  var formality_id = $(this).attr('id').replace("I20ReceivedLabel", "")
  $('#PopI20Received' + formality_id).show()
})

$(".ProgramFeePaymentLabelClass").click(function(){
  var formality_id = $(this).attr('id').replace("ProgramFeePaymentLabel", "")
  $('#PopProgramFeePayment' + formality_id).show()
})
$(".VisaInterviewSchedulingLabelClass").click(function(){
  $('#PopVisaInterviewScheduling').show()
})
$(".VisaGrantedLabelClass").click(function(){
  $('#PopVisaGranted').show()
})
$(".VisaRejectedLabelClass").click(function(){
  $('#PopVisaRejected').show()
})
$(".FlightTicketingLabelClass").click(function(){
  $('#PopFlightTicketing').show()
})
$(".AirportPickUpLabelClass").click(function(){
  $('#PopAirportPickupApplication').show()
})
$(".AccommodationApplicationLabelClass").click(function(){
  $('#PopApplication').show()
})
$(".HomeStayRecommendationLabelClass").click(function(){
  $('#PopHomeStayRecommendation').show()
})
$(".HostSelectionLabelClass").click(function(){
  $('#PopHostSelection').show()
})
$(".ParentsAccommodationLabelClass").click(function(){
  $('#PopParentsAccommodation').show()
})
$(".DepartureOTLabelClass").click(function(){
  $('#PopPreDepartureOrientation').show()
})
$(".DepartureConfirmedLabelClass").click(function(){
  $('#PopDepartureConfirmed').show()
})
