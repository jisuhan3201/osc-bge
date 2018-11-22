$("[type=file]").on("change", function(){
  // Name of file and placeholder
  if(this.files[0]){
    var file = this.files[0].name;
  }else {
    var file = ""
  }
  var get_id = $(this).attr('id').replace('file_source', 'span')
  var small_comment = $(this).parent().parent().find("td > #" + get_id);
  if($(this).val()!=""){
    small_comment.show()
    small_comment.text(file);
  }
});

$(".DeleteButton").on('click', function(){
  event.preventDefault();
  $(this).parent().find("input").val("")
  $(this).parent().parent().find("td > span").text("")
  $(this).parent().parent().find("td > input").val("")
  $(this).parent().parent().find("td > span").hide()
})

function updateElementIndex(el, prefix, ndx){
  var id_regex = new RegExp('(' + prefix + '-\\d+)');
  var replacement = prefix + '-' + ndx;
  if ($(el).attr("for")) $(el).attr("for", $(el).attr("for").replace(id_regex, replacement));
  if (el.id) el.id = el.id.replace(id_regex, replacement);
  if (el.name) el.name = el.name.replace(id_regex, replacement);
  if (el.for) el.for = el.for.replace(id_regex, replacement);
}

function cloneMore(selector, prefix){
  var newElement = $(selector).clone(true);
  var total = $('#id_' + prefix + '-TOTAL_FORMS').val();
  newElement.find(':input').each(function() {
    if($(this).attr('name')){
      var name = $(this).attr('name').replace('-' + (total-1) + '-', '-' + total + '-');
      var id = 'id_' + name;
      $(this).attr({'name': name, 'id': id}).val('').removeAttr('checked');

    }
  });
  newElement.find('label').each(function(){
    if($(this).attr('for')){
      var for_val = $(this).attr('for').replace('-' + (total-1) + '-', '-' + total + '-')
      $(this).attr({'for': for_val}).val('').removeAttr('checked');
    }
  })
  newElement.find('span').each(function(){
    if($(this).attr('id')){
      var id_val = $(this).attr('id').replace('-' + (total-1) + '-', '-' + total + '-')
      $(this).attr({'id': id_val}).val('').removeAttr('checked');
      $(this).hide();
    }
  })

  total++;
  $('#id_' + prefix + '-TOTAL_FORMS').val(total);
  $(selector).after(newElement);
  var conditionRow = $('.form-tr:not(:last)');
  conditionRow.find('.add-form-row')
  .removeClass('AddFileButton').addClass('DeleteFilebutton')
  .removeClass('add-form-row').addClass('remove-form-row')
  .html('-');
  return false;
}

function deleteForm(prefix, btn) {
    var total = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
    if (total > 1){
        btn.closest('.form-tr').remove();
        var forms = $('.form-tr');
        $('#id_' + prefix + '-TOTAL_FORMS').val(forms.length);
        for (var i=0, formCount=forms.length; i<formCount; i++) {
            $(forms.get(i)).find(':input').each(function() {
              updateElementIndex(this, prefix, i);
            });
            $(forms.get(i)).find('label').each(function(){
              updateElementIndex(this, prefix, i)
            });
            $(forms.get(i)).find('span').each(function(){
              updateElementIndex(this, prefix, i)
            });

        }
    }
    return false;
}
$(document).on('click', '.add-form-row', function(e){
    e.preventDefault();
    cloneMore('.form-tr:last', 'form');
    return false;
});
$(document).on('click', '.remove-form-row', function(e){
    e.preventDefault();
    deleteForm('form', $(this));
    return false;
});
