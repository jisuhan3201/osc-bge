// $(document).ready(function(){

  // $.ajax({                       // initialize an AJAX request
  //   url: "/charts/bge/statistics",                    // set the url of the request (= localhost:8000/hr/ajax/load-cities/)
  //   success: function (data) {   // `data` is the return of the `load_cities` view function
  //     var months = data.months;
  //     var result = data.data;
  //     var array = []
  //     result.forEach(function(element){
  //       array.push(
  //         {
  //           label: element.agent,
  //           data: element.data,
  //           fill:false,
  //           borderColor: [
  //             'rgb(' + (Math.floor(Math.random() * 256)) + ',' +
  //             (Math.floor(Math.random() * 256)) + ',' +
  //             (Math.floor(Math.random() * 256)) + ',1' + ')',
  //           ],
  //           borderWidth: 2
  //         }
  //       )
  //     })
  //     var ctx = document.getElementById("BgeStatisticChart");
  //     var myChart = new Chart(ctx, {
  //         type: 'line',
  //         data: {
  //             labels: months,
  //             datasets: array
  //         },
  //         options: {
  //             scales: {
  //                 yAxes: [{
  //                     ticks: {
  //                         beginAtZero:true
  //                     }
  //                 }]
  //             }
  //         }
  //     });
  //   }
  // });

  // $.ajax({                       // initialize an AJAX request
  //   url: "/charts/agents/statistics",                    // set the url of the request (= localhost:8000/hr/ajax/load-cities/)
  //   success: function (data) {   // `data` is the return of the `load_cities` view function
  //     var years = data.years;
  //     var result = data.data;
  //     var array = []
  //     result.forEach(function(element){
  //       array.push(
  //         {
  //           label: element.agent,
  //           data: element.data,
  //           fill:false,
  //           borderColor: [
  //             'rgb(' + (Math.floor(Math.random() * 256)) + ',' +
  //             (Math.floor(Math.random() * 256)) + ',' +
  //             (Math.floor(Math.random() * 256)) + ',1' + ')',
  //           ],
  //           borderWidth: 2
  //         }
  //       )
  //     })
  //     var ctx = document.getElementById("AgentStatisticChart");
  //     var myChart = new Chart(ctx, {
  //         type: 'line',
  //         data: {
  //             labels: years,
  //             datasets: array
  //         },
  //         options: {
  //             scales: {
  //                 yAxes: [{
  //                     ticks: {
  //                         beginAtZero:true
  //                     }
  //                 }]
  //             }
  //         }
  //     });
  //   }
  // });


  // $.ajax({                       // initialize an AJAX request
  //   url: "/charts/branches/statistics",                    // set the url of the request (= localhost:8000/hr/ajax/load-cities/)
  //   success: function (data) {   // `data` is the return of the `load_cities` view function
  //     var array = []
  //     data.forEach(function(element){
  //       var random_color = 'rgb(' + (Math.floor(Math.random() * 256)) + ',' +
  //       (Math.floor(Math.random() * 256)) + ',' +
  //       (Math.floor(Math.random() * 256))
  //       array.push(
  //         {
  //           label: element.branch,
  //           data: element.data,
  //           backgroundColor: random_color + ',0.6' + ')',
  //           borderColor : random_color + ',1' + ')',
  //         }
  //       )
  //     })
  //     var ctx = document.getElementById("BranchStatisticChart");
  //     var myChart = new Chart(ctx, {
  //         type: 'bar',
  //         data: {
  //             labels: ["Partner Schools", "Active Host Families", "Inactive Host Families", "Prospective Host Families", "Current Students", "Student Complaints"],
  //             datasets: array
  //         },
  //         options: {
  //             scales: {
  //                 yAxes: [{
  //                     ticks: {
  //                         beginAtZero:true
  //                     }
  //                 }]
  //             }
  //         }
  //     });
  //   }
  // });

  // $.ajax({                       // initialize an AJAX request
  //   url: "/branch/chart/statistics",                    // set the url of the request (= localhost:8000/hr/ajax/load-cities/)
  //   success: function (data) {   // `data` is the return of the `load_cities` view function
  //     console.log(data)
  //     var months = data.months;
  //     console.log(months)
  //     var ctx = document.getElementById("BranchPartStatisticChart");
  //     console.log(ctx)
  //     var myChart = new Chart(ctx, {
  //         type: 'line',
  //         data: {
  //             labels: months,
  //             datasets: [
  //               {
  //                 label:data.chart_name,
  //                 data: data.data,
  //                 fill:false,
  //                 borderColor: [
  //                   'rgb(' + (Math.floor(Math.random() * 256)) + ',' +
  //                   (Math.floor(Math.random() * 256)) + ',' +
  //                   (Math.floor(Math.random() * 256)) + ',1' + ')',
  //                 ],
  //                 borderWidth: 2
  //               },
  //             ],
  //         },
  //         options: {
  //             scales: {
  //                 yAxes: [{
  //                     ticks: {
  //                         beginAtZero:true
  //                     }
  //                 }]
  //             }
  //         }
  //     });
  //   }
  // });

// })
