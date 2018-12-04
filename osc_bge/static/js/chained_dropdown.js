$(document).ready(function(){
  $("#CountryAjax1").change(function () {
    var country = $(this).val();  // get the selected country ID from the HTML input
    if(country){
      $.ajax({                       // initialize an AJAX request
        url: "/agent/load/states",                    // set the url of the request (= localhost:8000/hr/ajax/load-cities/)
        data: {
          'country': country       // add the country id to the GET parameters
        },
        success: function (data) {   // `data` is the return of the `load_cities` view function
          $("#StateAjax1").empty()
          $("#StateAjax1").append('<option>State Select..</option>')
          for (var i=0; i < data.data.length; i++){
            $("#StateAjax1").append('<option value=' + "'" + data.data[i].state + "'" + '>' + data.data[i].state.toUpperCase().toUpperCase() + '</option>')
          }
        }
      });
    }
    else {
      $("#StateAjax1").empty()
      $("#StateAjax1").append('<option>State Select..</option>')
    }
  });

  $("#StateAjax1").change(function () {
    var state = $(this).val();  // get the selected country ID from the HTML input

    if(state){
      $.ajax({                       // initialize an AJAX request
        url: "/agent/load/schools",                    // set the url of the request (= localhost:8000/hr/ajax/load-cities/)
        data: {
          'state': state       // add the country id to the GET parameters
        },
        success: function (data) {   // `data` is the return of the `load_cities` view function
          $("#SchoolAjax1").empty()
          $("#SchoolAjax1").append('<option>State Select..</option>')
          for (var i=0; i < data.length; i++){
            $("#SchoolAjax1").append('<option value=' + "'" + data[i].pk + "'" + '>' + data[i].fields.name + '</option>')
          }
        }
      });
    }
    else {
      $("#SchoolAjax1").empty()
      $("#SchoolAjax1").append('<option>State Select..</option>')
    }
  });

  $("#CountryAjax2").change(function () {
    var country = $(this).val();  // get the selected country ID from the HTML input
    if(country){
      $.ajax({                       // initialize an AJAX request
        url: "/agent/load/states",                    // set the url of the request (= localhost:8000/hr/ajax/load-cities/)
        data: {
          'country': country       // add the country id to the GET parameters
        },
        success: function (data) {   // `data` is the return of the `load_cities` view function
          $("#StateAjax2").empty()
          $("#StateAjax2").append('<option>State Select..</option>')
          for (var i=0; i < data.data.length; i++){
            $("#StateAjax2").append('<option value=' + "'" + data.data[i].state + "'" + '>' + data.data[i].state.toUpperCase() + '</option>')
          }
        }
      });
    }
    else {
      $("#StateAjax2").empty()
      $("#StateAjax2").append('<option>State Select..</option>')
    }
  });

  $("#StateAjax2").change(function () {
    var state = $(this).val();  // get the selected country ID from the HTML input

    if(state){
      $.ajax({                       // initialize an AJAX request
        url: "/agent/load/schools",                    // set the url of the request (= localhost:8000/hr/ajax/load-cities/)
        data: {
          'state': state       // add the country id to the GET parameters
        },
        success: function (data) {   // `data` is the return of the `load_cities` view function
          $("#SchoolAjax2").empty()
          $("#SchoolAjax2").append('<option>State Select..</option>')
          for (var i=0; i < data.length; i++){
            $("#SchoolAjax2").append('<option value=' + "'" + data[i].pk + "'" + '>' + data[i].fields.name + '</option>')
          }
        }
      });
    }
    else {
      $("#SchoolAjax2").empty()
      $("#SchoolAjax2").append('<option>State Select..</option>')
    }
  });


  $("#CountryAjax3").change(function () {
    var country = $(this).val();  // get the selected country ID from the HTML input
    if(country){
      $.ajax({                       // initialize an AJAX request
        url: "/agent/load/states",                    // set the url of the request (= localhost:8000/hr/ajax/load-cities/)
        data: {
          'country': country       // add the country id to the GET parameters
        },
        success: function (data) {   // `data` is the return of the `load_cities` view function
          $("#StateAjax3").empty()
          $("#StateAjax3").append('<option>State Select..</option>')
          for (var i=0; i < data.data.length; i++){
            $("#StateAjax3").append('<option value=' + "'" + data.data[i].state + "'" + '>' + data.data[i].state.toUpperCase() + '</option>')
          }
        }
      });
    }
    else {
      $("#StateAjax3").empty()
      $("#StateAjax3").append('<option>State Select..</option>')
    }
  });

  $("#StateAjax3").change(function () {
    var state = $(this).val();  // get the selected country ID from the HTML input

    if(state){
      $.ajax({                       // initialize an AJAX request
        url: "/agent/load/schools",                    // set the url of the request (= localhost:8000/hr/ajax/load-cities/)
        data: {
          'state': state       // add the country id to the GET parameters
        },
        success: function (data) {   // `data` is the return of the `load_cities` view function
          $("#SchoolAjax3").empty()
          $("#SchoolAjax3").append('<option>State Select..</option>')
          for (var i=0; i < data.length; i++){
            $("#SchoolAjax3").append('<option value=' + "'" + data[i].pk + "'" + '>' + data[i].fields.name + '</option>')
          }
        }
      });
    }
    else {
      $("#SchoolAjax3").empty()
      $("#SchoolAjax3").append('<option>State Select..</option>')
    }
  });


  $("#CountryAjax4").change(function () {
    var country = $(this).val();  // get the selected country ID from the HTML input
    if(country){
      $.ajax({                       // initialize an AJAX request
        url: "/agent/load/states",                    // set the url of the request (= localhost:8000/hr/ajax/load-cities/)
        data: {
          'country': country       // add the country id to the GET parameters
        },
        success: function (data) {   // `data` is the return of the `load_cities` view function
          $("#StateAjax4").empty()
          $("#StateAjax4").append('<option>State Select..</option>')
          for (var i=0; i < data.data.length; i++){
            $("#StateAjax4").append('<option value=' + "'" + data.data[i].state + "'" + '>' + data.data[i].state.toUpperCase() + '</option>')
          }
        }
      });
    }
    else {
      $("#StateAjax4").empty()
      $("#StateAjax4").append('<option>State Select..</option>')
    }
  });

  $("#StateAjax4").change(function () {
    var state = $(this).val();  // get the selected country ID from the HTML input

    if(state){
      $.ajax({                       // initialize an AJAX request
        url: "/agent/load/schools",                    // set the url of the request (= localhost:8000/hr/ajax/load-cities/)
        data: {
          'state': state       // add the country id to the GET parameters
        },
        success: function (data) {   // `data` is the return of the `load_cities` view function
          $("#SchoolAjax4").empty()
          $("#SchoolAjax4").append('<option>State Select..</option>')
          for (var i=0; i < data.length; i++){
            $("#SchoolAjax4").append('<option value=' + "'" + data[i].pk + "'" + '>' + data[i].fields.name + '</option>')
          }
        }
      });
    }
    else {
      $("#SchoolAjax4").empty()
      $("#SchoolAjax4").append('<option>State Select..</option>')
    }
  });


  $("#CountryAjax5").change(function () {
    var country = $(this).val();  // get the selected country ID from the HTML input
    if(country){
      $.ajax({                       // initialize an AJAX request
        url: "/agent/load/states",                    // set the url of the request (= localhost:8000/hr/ajax/load-cities/)
        data: {
          'country': country       // add the country id to the GET parameters
        },
        success: function (data) {   // `data` is the return of the `load_cities` view function
          $("#StateAjax5").empty()
          $("#StateAjax5").append('<option>State Select..</option>')
          for (var i=0; i < data.data.length; i++){
            $("#StateAjax5").append('<option value=' + "'" + data.data[i].state + "'" + '>' + data.data[i].state.toUpperCase() + '</option>')
          }
        }
      });
    }
    else {
      $("#StateAjax5").empty()
      $("#StateAjax5").append('<option>State Select..</option>')
    }
  });

  $("#StateAjax5").change(function () {
    var state = $(this).val();  // get the selected country ID from the HTML input

    if(state){
      $.ajax({                       // initialize an AJAX request
        url: "/agent/load/schools",                    // set the url of the request (= localhost:8000/hr/ajax/load-cities/)
        data: {
          'state': state       // add the country id to the GET parameters
        },
        success: function (data) {   // `data` is the return of the `load_cities` view function
          $("#SchoolAjax5").empty()
          $("#SchoolAjax5").append('<option>State Select..</option>')
          for (var i=0; i < data.length; i++){
            $("#SchoolAjax5").append('<option value=' + "'" + data[i].pk + "'" + '>' + data[i].fields.name + '</option>')
          }
        }
      });
    }
    else {
      $("#SchoolAjax5").empty()
      $("#SchoolAjax5").append('<option>State Select..</option>')
    }
  });


  $("#CountryAjax6").change(function () {
    var country = $(this).val();  // get the selected country ID from the HTML input
    if(country){
      $.ajax({                       // initialize an AJAX request
        url: "/agent/load/states",                    // set the url of the request (= localhost:8000/hr/ajax/load-cities/)
        data: {
          'country': country       // add the country id to the GET parameters
        },
        success: function (data) {   // `data` is the return of the `load_cities` view function
          $("#StateAjax6").empty()
          $("#StateAjax6").append('<option>State Select..</option>')
          for (var i=0; i < data.data.length; i++){
            $("#StateAjax6").append('<option value=' + "'" + data.data[i].state + "'" + '>' + data.data[i].state.toUpperCase() + '</option>')
          }
        }
      });
    }
    else {
      $("#StateAjax6").empty()
      $("#StateAjax6").append('<option>State Select..</option>')
    }
  });

  $("#StateAjax6").change(function () {
    var state = $(this).val();  // get the selected country ID from the HTML input

    if(state){
      $.ajax({                       // initialize an AJAX request
        url: "/agent/load/schools",                    // set the url of the request (= localhost:8000/hr/ajax/load-cities/)
        data: {
          'state': state       // add the country id to the GET parameters
        },
        success: function (data) {   // `data` is the return of the `load_cities` view function
          $("#SchoolAjax6").empty()
          $("#SchoolAjax6").append('<option>State Select..</option>')
          for (var i=0; i < data.length; i++){
            $("#SchoolAjax6").append('<option value=' + "'" + data[i].pk + "'" + '>' + data[i].fields.name + '</option>')
          }
        }
      });
    }
    else {
      $("#SchoolAjax6").empty()
      $("#SchoolAjax6").append('<option>State Select..</option>')
    }
  });


  $("#CountryAjax7").change(function () {
    var country = $(this).val();  // get the selected country ID from the HTML input
    if(country){
      $.ajax({                       // initialize an AJAX request
        url: "/agent/load/states",                    // set the url of the request (= localhost:8000/hr/ajax/load-cities/)
        data: {
          'country': country       // add the country id to the GET parameters
        },
        success: function (data) {   // `data` is the return of the `load_cities` view function
          $("#StateAjax7").empty()
          $("#StateAjax7").append('<option>State Select..</option>')
          for (var i=0; i < data.data.length; i++){
            $("#StateAjax7").append('<option value=' + "'" + data.data[i].state + "'" + '>' + data.data[i].state.toUpperCase() + '</option>')
          }
        }
      });
    }
    else {
      $("#StateAjax7").empty()
      $("#StateAjax7").append('<option>State Select..</option>')
    }
  });

  $("#StateAjax7").change(function () {
    var state = $(this).val();  // get the selected country ID from the HTML input

    if(state){
      $.ajax({                       // initialize an AJAX request
        url: "/agent/load/schools",                    // set the url of the request (= localhost:8000/hr/ajax/load-cities/)
        data: {
          'state': state       // add the country id to the GET parameters
        },
        success: function (data) {   // `data` is the return of the `load_cities` view function
          $("#SchoolAjax7").empty()
          $("#SchoolAjax7").append('<option>State Select..</option>')
          for (var i=0; i < data.length; i++){
            $("#SchoolAjax7").append('<option value=' + "'" + data[i].pk + "'" + '>' + data[i].fields.name + '</option>')
          }
        }
      });
    }
    else {
      $("#SchoolAjax7").empty()
      $("#SchoolAjax7").append('<option>State Select..</option>')
    }
  });


  $("#CountryAjax8").change(function () {
    var country = $(this).val();  // get the selected country ID from the HTML input
    if(country){
      $.ajax({                       // initialize an AJAX request
        url: "/agent/load/states",                    // set the url of the request (= localhost:8000/hr/ajax/load-cities/)
        data: {
          'country': country       // add the country id to the GET parameters
        },
        success: function (data) {   // `data` is the return of the `load_cities` view function
          $("#StateAjax8").empty()
          $("#StateAjax8").append('<option>State Select..</option>')
          for (var i=0; i < data.data.length; i++){
            $("#StateAjax8").append('<option value=' + "'" + data.data[i].state + "'" + '>' + data.data[i].state.toUpperCase() + '</option>')
          }
        }
      });
    }
    else {
      $("#StateAjax8").empty()
      $("#StateAjax8").append('<option>State Select..</option>')
    }
  });

  $("#StateAjax8").change(function () {
    var state = $(this).val();  // get the selected country ID from the HTML input

    if(state){
      $.ajax({                       // initialize an AJAX request
        url: "/agent/load/schools",                    // set the url of the request (= localhost:8000/hr/ajax/load-cities/)
        data: {
          'state': state       // add the country id to the GET parameters
        },
        success: function (data) {   // `data` is the return of the `load_cities` view function
          $("#SchoolAjax8").empty()
          $("#SchoolAjax8").append('<option>State Select..</option>')
          for (var i=0; i < data.length; i++){
            $("#SchoolAjax8").append('<option value=' + "'" + data[i].pk + "'" + '>' + data[i].fields.name + '</option>')
          }
        }
      });
    }
    else {
      $("#SchoolAjax8").empty()
      $("#SchoolAjax8").append('<option>State Select..</option>')
    }
  });


  $("#CountryAjax9").change(function () {
    var country = $(this).val();  // get the selected country ID from the HTML input
    if(country){
      $.ajax({                       // initialize an AJAX request
        url: "/agent/load/states",                    // set the url of the request (= localhost:8000/hr/ajax/load-cities/)
        data: {
          'country': country       // add the country id to the GET parameters
        },
        success: function (data) {   // `data` is the return of the `load_cities` view function
          $("#StateAjax9").empty()
          $("#StateAjax9").append('<option>State Select..</option>')
          for (var i=0; i < data.data.length; i++){
            $("#StateAjax9").append('<option value=' + "'" + data.data[i].state + "'" + '>' + data.data[i].state.toUpperCase() + '</option>')
          }
        }
      });
    }
    else {
      $("#StateAjax9").empty()
      $("#StateAjax9").append('<option>State Select..</option>')
    }
  });

  $("#StateAjax9").change(function () {
    var state = $(this).val();  // get the selected country ID from the HTML input

    if(state){
      $.ajax({                       // initialize an AJAX request
        url: "/agent/load/schools",                    // set the url of the request (= localhost:8000/hr/ajax/load-cities/)
        data: {
          'state': state       // add the country id to the GET parameters
        },
        success: function (data) {   // `data` is the return of the `load_cities` view function
          $("#SchoolAjax9").empty()
          $("#SchoolAjax9").append('<option>State Select..</option>')
          for (var i=0; i < data.length; i++){
            $("#SchoolAjax9").append('<option value=' + "'" + data[i].pk + "'" + '>' + data[i].fields.name + '</option>')
          }
        }
      });
    }
    else {
      $("#SchoolAjax9").empty()
      $("#SchoolAjax9").append('<option>State Select..</option>')
    }
  });


  $("#CountryAjax10").change(function () {
    var country = $(this).val();  // get the selected country ID from the HTML input
    if(country){
      $.ajax({                       // initialize an AJAX request
        url: "/agent/load/states",                    // set the url of the request (= localhost:8000/hr/ajax/load-cities/)
        data: {
          'country': country       // add the country id to the GET parameters
        },
        success: function (data) {   // `data` is the return of the `load_cities` view function
          $("#StateAjax10").empty()
          $("#StateAjax10").append('<option>State Select..</option>')
          for (var i=0; i < data.data.length; i++){
            $("#StateAjax10").append('<option value=' + "'" + data.data[i].state + "'" + '>' + data.data[i].state.toUpperCase() + '</option>')
          }
        }
      });
    }
    else {
      $("#StateAjax10").empty()
      $("#StateAjax10").append('<option>State Select..</option>')
    }
  });

  $("#StateAjax10").change(function () {
    var state = $(this).val();  // get the selected country ID from the HTML input

    if(state){
      $.ajax({                       // initialize an AJAX request
        url: "/agent/load/schools",                    // set the url of the request (= localhost:8000/hr/ajax/load-cities/)
        data: {
          'state': state       // add the country id to the GET parameters
        },
        success: function (data) {   // `data` is the return of the `load_cities` view function
          $("#SchoolAjax10").empty()
          $("#SchoolAjax10").append('<option>State Select..</option>')
          for (var i=0; i < data.length; i++){
            $("#SchoolAjax10").append('<option value=' + "'" + data[i].pk + "'" + '>' + data[i].fields.name + '</option>')
          }
        }
      });
    }
    else {
      $("#SchoolAjax10").empty()
      $("#SchoolAjax10").append('<option>State Select..</option>')
    }
  });


})
