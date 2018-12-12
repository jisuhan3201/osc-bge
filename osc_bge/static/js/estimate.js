$("#ModifyButtonId").click(function(){
  var default_program_fee = $("input[name=default_program_fee]").val();
  var default_program_fee_qty = $("input[name=default_program_fee_qty]").val();
  var other_program_fee = $("input[name=other_program_fee]").val();
  var other_program_fee_qty = $("input[name=other_program_fee_qty]").val();
  $("input[name=sub_total_program_fee]").val(default_program_fee*default_program_fee_qty+other_program_fee*other_program_fee_qty);
  var sub_total_program_fee = $("input[name=sub_total_program_fee]").val();

  var default_application_fee = $("input[name=default_application_fee]").val();
  var default_application_fee_qty = $("input[name=default_application_fee_qty]").val();
  var other_application_fee = $("input[name=other_application_fee]").val();
  var other_application_fee_qty = $("input[name=other_application_fee_qty]").val();
  $("input[name=sub_total_application_fee]").val(default_application_fee*default_application_fee_qty+other_application_fee*other_application_fee_qty);
  var sub_total_application_fee = $("input[name=sub_total_application_fee]").val();

  var other_fee1 = $("input[name=other_fee1]").val();
  var other_fee1_qty = $("input[name=other_fee1_qty]").val();
  var other_fee2 = $("input[name=other_fee2]").val();
  var other_fee2_qty = $("input[name=other_fee2_qty]").val();
  var other_fee3 = $("input[name=other_fee3]").val();
  var other_fee3_qty = $("input[name=other_fee3_qty]").val();
  var other_fee4 = $("input[name=other_fee4]").val();
  var other_fee4_qty = $("input[name=other_fee4_qty]").val();
  $("input[name=total_other_fee]").val(
    other_fee1*other_fee1_qty+
    other_fee2*other_fee2_qty+
    other_fee3*other_fee3_qty+
    other_fee4*other_fee4_qty
    );
  var sub_total_other_fee = $("input[name=total_other_fee]").val();

  $("#total_cost").text(Number(sub_total_program_fee)+Number(sub_total_application_fee)+Number(sub_total_other_fee))
  var total_cost = $("#total_cost").text();
  var waive_fee = $("input[name=waive_fee]").val();

  $(".total_estimate_fee").text(Number(total_cost) - Number(waive_fee));
})



$("#CurrencyRateButtonId").click(function(){
  var default_program_fee = $("input[name=default_program_fee]").val();
  var default_program_fee_qty = $("input[name=default_program_fee_qty]").val();
  var other_program_fee = $("input[name=other_program_fee]").val();
  var other_program_fee_qty = $("input[name=other_program_fee_qty]").val();
  $("input[name=sub_total_program_fee]").val(default_program_fee*default_program_fee_qty+other_program_fee*other_program_fee_qty);
  var sub_total_program_fee = $("input[name=sub_total_program_fee]").val();

  var default_application_fee = $("input[name=default_application_fee]").val();
  var default_application_fee_qty = $("input[name=default_application_fee_qty]").val();
  var other_application_fee = $("input[name=other_application_fee]").val();
  var other_application_fee_qty = $("input[name=other_application_fee_qty]").val();
  $("input[name=sub_total_application_fee]").val(default_application_fee*default_application_fee_qty+other_application_fee*other_application_fee_qty);
  var sub_total_application_fee = $("input[name=sub_total_application_fee]").val();

  var other_fee1 = $("input[name=other_fee1]").val();
  var other_fee1_qty = $("input[name=other_fee1_qty]").val();
  var other_fee2 = $("input[name=other_fee2]").val();
  var other_fee2_qty = $("input[name=other_fee2_qty]").val();
  var other_fee3 = $("input[name=other_fee3]").val();
  var other_fee3_qty = $("input[name=other_fee3_qty]").val();
  var other_fee4 = $("input[name=other_fee4]").val();
  var other_fee4_qty = $("input[name=other_fee4_qty]").val();
  $("input[name=total_other_fee]").val(
    other_fee1*other_fee1_qty+
    other_fee2*other_fee2_qty+
    other_fee3*other_fee3_qty+
    other_fee4*other_fee4_qty
    );
  var sub_total_other_fee = $("input[name=total_other_fee]").val();
  var currency_rate = $('input[name=currency_rate]').val();

  sub_total_program_fee = sub_total_program_fee*currency_rate
  $("input[name=sub_total_program_fee]").val(sub_total_program_fee)

  sub_total_application_fee = sub_total_application_fee*currency_rate
  $("input[name=sub_total_application_fee]").val(sub_total_application_fee);

  sub_total_other_fee = sub_total_other_fee*currency_rate
  $("input[name=total_other_fee]").val(sub_total_other_fee);

  $("#total_cost").text(parseFloat(sub_total_program_fee) + parseFloat(sub_total_application_fee) + parseFloat(sub_total_other_fee));
  var total_cost = $("#total_cost").text();
  var waive_fee = $("input[name=waive_fee]").val();

  $(".total_estimate_fee").text(parseFloat(total_cost) - Number(waive_fee))

})
