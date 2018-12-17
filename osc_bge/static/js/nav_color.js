$(document).ready(function(){
  var pathname = window.location.pathname
  $('.Menu').find('a').each(function() {
    if ($(this).attr('href') == pathname){
      $(this).addClass('On')
    }
  });
  $('.SchoolMenu').find('a').each(function() {
    if ($(this).attr('href') == pathname){
      $(this).addClass('On')
    }
});

});
