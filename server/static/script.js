var DOMAIN = "http://127.0.0.1:5000/";

function hideEvacuationAdviceElements() {
  $("#evacuate-advice-shelter-in-place").hide();
  $("#evacuate-advice-evacuate-now").hide();
  $("#evacuate-advice-prepare-to-evacuate").hide();
  $("#evacuate-advice-no-need-to-evacuate").hide();
  $('#shelter-section').hide();
}

$(document).ready(function() {
  hideEvacuationAdviceElements();
  
  // User address change handler
  $('#address').focusout(function() {
    let address = $(this).val();
    if (address == "") {
      return;
    };
    let queryPayload = {
      "address": address
    };
    console.log("Evacuation Advice queryPayload:")
    console.log(queryPayload)
    
    hideEvacuationAdviceElements()
    
    //Get shelter advice from backend
    jQuery.get(DOMAIN + "evacadvice/", queryPayload, function(data) {
      console.log(data);
      
      if (data === "SHELTER IN PLACE") {
        $("#evacuate-advice-shelter-in-place").show();
        $("#shelter-section").show();
      } else if (data === "EVACUATE NOW") {
        $("#evacuate-advice-evacuate-now").show();
        $("#shelter-section").show();
      } else if (data === "PREPARE TO EVACUATE") {
        $("#evacuate-advice-prepare-to-evacuate").show();
        $("#shelter-section").show();
      } else if (data === "YOU ARE SAFE") {
        $("#evacuate-advice-no-need-to-evacuate").show();
      } else {
        // Default
        $("#evacuate-advice-prepare-to-evacuate").show();
      }
    });
  });
  
  // Shelter selection handler
  $("#shelter-selection").on('change', function() {
    let shelterSelection = $(this).val();
    $('#address').val(shelterSelection);
  });
  
  // Infant selection handler
  $("#party-members-infants").on('change', function() {
    let totalPeople = parseInt($("#party-members-infants").val()) + parseInt($("#party-members-children").val()) + parseInt($("#party-members-adults").val()) + parseInt($("#party-members-seniors").val());
    $('#water-label').html("Water (gallons) -- " + totalPeople + " recommended per day.")
    $('#meals-label').html("Meals (per person) -- " + totalPeople * 3 + " recommended per day.")
  });
  
  // Child selection handler
  $("#party-members-children").on('change', function() {
    let totalPeople = parseInt($("#party-members-infants").val()) + parseInt($("#party-members-children").val()) + parseInt($("#party-members-adults").val()) + parseInt($("#party-members-seniors").val());
    $('#water-label').html("Water (gallons) -- " + totalPeople + " recommended per day.")
    $('#meals-label').html("Meals (per person) -- " + totalPeople * 3 + " recommended per day.")
  });
  
  // Adult selection handler
  $("#party-members-adults").on('change', function() {
    let totalPeople = parseInt($("#party-members-infants").val()) + parseInt($("#party-members-children").val()) + parseInt($("#party-members-adults").val()) + parseInt($("#party-members-seniors").val());
    $('#water-label').html("Water (gallons) -- " + totalPeople + " recommended per day.")
    $('#meals-label').html("Meals (per person) -- " + totalPeople * 3 + " recommended per day.")
  });
  
  // Senior selection handler
  $("#party-members-seniors").on('change', function() {
    let totalPeople = parseInt($("#party-members-infants").val()) + parseInt($("#party-members-children").val()) + parseInt($("#party-members-adults").val()) + parseInt($("#party-members-seniors").val());
    $('#water-label').html("Water (gallons) -- " + totalPeople + " recommended per day.")
    $('#meals-label').html("Meals (per person) -- " + totalPeople * 3 + " recommended per day.")
  });

  // Submit button handler
  $("#submit-button").on('click', function() {
    let userMobilePhoneNumbers = [
      $('#mobile-phone-number').val(),
      $('#mobile-phone-number-1').val(),
      $('#mobile-phone-number-2').val(),
      $('#mobile-phone-number-3').val(),
      $('#mobile-phone-number-4').val()
    ].filter(number => number !== "");
    
    let userInformation = {
      "address": $('#address').val(),
      "phone_numbers": userMobilePhoneNumbers,
      "supplies": {
        "water": $('#supplies-water').val(),
        "food": $('#supplies-food').val()
      },
      "party_member": {
        "adults": $('#party-members-adults').val(),
        "children": $('#party-members-children').val(),
        "infants": $('#party-members-infants').val(),
        "elderly": $('#party-members-seniors').val(),
        "pets": $('#party-members-pets').val()
      }
    }
    console.log(userInformation);
    
    jQuery.ajax({
        url : DOMAIN + "user/",
        type: "POST",
        data: JSON.stringify(userInformation),
        contentType: "application/json; charset=utf-8",
        dataType   : "json",
        success    : function(data){
          console.log("User information submitted: UserID:" + data)
        }
    });
    
  });
})