
// For update.html

$(".CurrentStudentReviewClass").click(function () {
  var review_id = $(this).attr('id').replace("CurrentStudentReview", "")
  if(review_id){
    $.ajax({                       // initialize an AJAX request
      url: "/school/current/review/get/" + review_id,                    // set the url of the request (= localhost:8000/hr/ajax/load-cities/)
      success: function (data) {   // `data` is the return of the `load_cities` view function
        $("#PopRegistReview input[name=review_id]").val(data[0].pk);
        $("#PopRegistReview input[name=student]").val(data[0].fields.student);
        $("#PopRegistReview input[name=grade]").val(data[0].fields.grade);
        $("#PopRegistReview input[name=homecity]").val(data[0].fields.homecity);
        $("#PopRegistReview textarea[name=comment]").text(data[0].fields.comment);
        $("#PopRegistReview").show();
      }
    });
  }
  else{
    alert('Review ID does not exist..')
  }
});

$("#PopRegistReview .Close").click(function(){
  $("#PopRegistReview input[name=review_id]").val("");
  $("#PopRegistReview input[name=student]").val("");
  $("#PopRegistReview input[name=grade]").val("");
  $("#PopRegistReview input[name=homecity]").val("");
  $("#PopRegistReview textarea[name=comment]").text("");
  $("#PopRegistReview").hide();
})

$(".GraduateStudentReviewClass").click(function () {
  var profile_id = $(this).attr('id').replace("GraduateStudentReview", "")
  if(profile_id){
    $.ajax({                       // initialize an AJAX request
      url: "/school/graduate/review/get/" + profile_id,                    // set the url of the request (= localhost:8000/hr/ajax/load-cities/)
      success: function (data) {   // `data` is the return of the `load_cities` view function
        $("#PopRegistGraduateProfile input[name=profile_id]").val(data[0].pk);
        $("#PopRegistGraduateProfile input[name=student]").val(data[0].fields.student);
        $("#PopRegistGraduateProfile input[name=attended]").val(data[0].fields.attended);
        $("#PopRegistGraduateProfile input[name=init_eng]").val(data[0].fields.init_eng);
        $("#PopRegistGraduateProfile input[name=gpa_china]").val(data[0].fields.gpa_china);
        $("#PopRegistGraduateProfile input[name=toefl]").val(data[0].fields.toefl);
        $("#PopRegistGraduateProfile input[name=gpa]").val(data[0].fields.gpa);
        $("#PopRegistGraduateProfile input[name=sat_act]").val(data[0].fields.sat_act);
        $("#PopRegistGraduateProfile input[name=activities]").val(data[0].fields.activities);
        $("#PopRegistGraduateProfile input[name=college]").val(data[0].fields.college);
        $("#PopRegistGraduateProfile input[name=major]").val(data[0].fields.major);
        $("#PopRegistGraduateProfile").show();
      }
    });
  }
  else{
    alert('Profile ID does not exist..')
  }
});

$("#PopRegistGraduateProfile .Close").click(function(){
  $("#PopRegistGraduateProfile input[name=profile_id]").val("");
  $("#PopRegistGraduateProfile input[name=student]").val("");
  $("#PopRegistGraduateProfile input[name=attended]").val("");
  $("#PopRegistGraduateProfile input[name=init_eng]").val("");
  $("#PopRegistGraduateProfile input[name=gpa_china]").val("");
  $("#PopRegistGraduateProfile input[name=toefl]").val("");
  $("#PopRegistGraduateProfile input[name=gpa]").val("");
  $("#PopRegistGraduateProfile input[name=sat_act]").val("");
  $("#PopRegistGraduateProfile input[name=activities]").val("");
  $("#PopRegistGraduateProfile input[name=college]").val("");
  $("#PopRegistGraduateProfile input[name=major]").val("");
  $("#PopRegistGraduateProfile").hide();
})


// For review.HTML

$(".AgentCurrentStudentReviewClass").click(function () {
  var review_id = $(this).attr('id').replace("AgentCurrentStudentReview", "")
  $.ajax({                       // initialize an AJAX request
    url: "/school/current/review/get/" + review_id,                    // set the url of the request (= localhost:8000/hr/ajax/load-cities/)
    success: function (data) {   // `data` is the return of the `load_cities` view function
      $("#CurrentStudentReviewTop .Name").text(data[0].fields.student)
      $("#CurrentStudentReviewTop .Info span:nth-child(1) b").text(data[0].fields.grade)
      $("#CurrentStudentReviewTop .Info span:nth-child(3) b").text(data[0].fields.homecity)
      $("#CurrentStudentReviewTop .Contents").text(data[0].fields.comment)
      $("#CurrentStudentReviewTop").show()
    }
  });
});

$(".AgentGraduateStudentReviewClass").click(function () {
  var review_id = $(this).attr('id').replace("AgentGraduateStudentReview", "")
  $.ajax({                       // initialize an AJAX request
    url: "/school/graduate/review/get/" + review_id,                    // set the url of the request (= localhost:8000/hr/ajax/load-cities/)
    success: function (data) {   // `data` is the return of the `load_cities` view function
      console.log(data)
      $("#GraduateStudentReviewTop .Name").text(data[0].fields.student)
      $("#GraduateStudentReviewTop .Info span:nth-child(1) b").text(data[0].fields.attended)
      $("#GraduateStudentReviewTop .Info span:nth-child(2) b").text(data[0].fields.college)
      $("#GraduateStudentReviewTop .Info span:nth-child(3) b").text(data[0].fields.init_eng)
      $("#GraduateStudentReviewTop .Info span:nth-child(4) b").text(data[0].fields.gpa_china)
      $("#GraduateStudentReviewTop .Info span:nth-child(5) b").text(data[0].fields.toefl)
      $("#GraduateStudentReviewTop .Info span:nth-child(6) b").text(data[0].fields.gpa)
      $("#GraduateStudentReviewTop .Info span:nth-child(7) b").text(data[0].fields.sat_act)
      $("#GraduateStudentReviewTop .Info span:nth-child(8) b").text(data[0].fields.activities)
      $("#GraduateStudentReviewTop .Info span:last-child b").text(data[0].fields.major)
      $("#GraduateStudentReviewTop").show()
    }
  });
});
