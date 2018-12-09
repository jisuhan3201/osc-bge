$('input[name=agent_type]').change(function(){
  if(this.value == 'branch'){
    $("#SelectHeadTdId").show()
    $("#NumBranchesTdId").hide()
    $('#NumBranchesId').val("")
    $("#ChangeByTypeThId").text('Select Head : ')
    $('#AgentHeadListId').attr('required', true)
  }
  else if (this.value == 'head'){
    $("#SelectHeadTdId").hide()
    $("#NumBranchesTdId").show()
    $('#AgentHeadListId').val('')
    $("#ChangeByTypeThId").text('Branches : ')
    $('#AgentHeadListId').removeAttr('required')
  }
})
