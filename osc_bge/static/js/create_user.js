$('.UserTypeClass').change(function(){
  if(this.value == 'bge_branch_admin'){
    $(".BgeBranchUserPositionClass").show()
    $("#BgeUserPosition").attr('required', true)

    $('#BgeBranchSelect').show()
    $("#AgentHeadSelect").hide()
    $("#AgentBranchSelect").hide()

    $('#BgeBranchSelect').attr('required', true)
    $('#AgentHeadSelect').attr('required', false)
    $('#AgentBranchSelect').attr('required', false)
  }
  else if (this.value == 'agency_admin'){
    $(".BgeBranchUserPositionClass").hide()
    $("#BgeUserPosition").attr('required', false)

    $('#BgeBranchSelect').hide()
    $("#AgentHeadSelect").show()
    $("#AgentBranchSelect").hide()

    $('#BgeBranchSelect').attr('required', false)
    $('#AgentHeadSelect').attr('required', true)
    $('#AgentBranchSelect').attr('required', false)
  }
  else if (this.value == 'agency_branch_admin' | this.value == 'counselor'){
    $(".BgeBranchUserPositionClass").hide()
    $("#BgeUserPosition").attr('required', false)

    $('#BgeBranchSelect').hide()
    $("#AgentHeadSelect").hide()
    $("#AgentBranchSelect").show()

    $('#BgeBranchSelect').attr('required', false)
    $('#AgentHeadSelect').attr('required', false)
    $('#AgentBranchSelect').attr('required', true)
  }
  else{
    $(".BgeBranchUserPositionClass").hide()
    $("#BgeUserPosition").attr('required', false)

    $('#BgeBranchSelect').hide()
    $("#AgentHeadSelect").hide()
    $("#AgentBranchSelect").hide()

    $('#BgeBranchSelect').attr('required', false)
    $('#AgentHeadSelect').attr('required', false)
    $('#AgentBranchSelect').attr('required', false)

  }
})
