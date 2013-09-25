$(function() {
    var input = $( "#steering_wheel" );
    var slider = $( "<div id='slider'></div>" ).insertAfter( input ).slider({
      min: -600,
      max: 600,
      value: 0,
      slide: function( event, ui ) {
          input.val(ui.value);
          jQuery.post($SCRIPT_ROOT + '/_set_data', {name: "angle", value: ui.value});
      }
    });
    $( "#steering_wheel" ).change(function() {
        slider.slider( "value", this.value );
        jQuery.post($SCRIPT_ROOT + '/_set_data', { name: "angle", value: this.value});
    });
  });

$(function() {
    var input = $( "#accelerator" );
    var slider = $( "<div id='slider'></div>" ).insertAfter( input ).slider({
      min: 0,
      max: 100,
        value: input.val(),
      slide: function( event, ui ) {
          input.val(ui.value);
          jQuery.post($SCRIPT_ROOT + '/_set_data', { name: "accelerator", value: ui.value});
      }
    });
    $( "#accelerator" ).change(function() {
        slider.slider( "value", this.value );
        jQuery.post($SCRIPT_ROOT + '/_set_data', { name: "accelerator", value: this.value});
    });
  });

$(function() {
    var input = $( "#brake" );
    var slider = $( "<div id='slider'></div>" ).insertAfter( input ).slider({
      min: 0,
      max: 100,
      value: 0,
      slide: function( event, ui ) {
          input.val(ui.value);
          jQuery.post($SCRIPT_ROOT + '/_set_data', { name: "brake", value: ui.value});
      }
    });
    $( "#brake" ).change(function() {
        slider.slider( "value", this.value );
        jQuery.post($SCRIPT_ROOT + '/_set_data', { name: "brake", value: this.value});
    });
  });

$(function() {
    $('#parking_brake_check').change(function(){
        jQuery.post($SCRIPT_ROOT + '/_set_data', { name: "parking_brake_status", value: this.checked});
    });
});

$(function() {
    $( '#ignition_radio' ).buttonset();
});

$(function() {
    $('#ignition_check').change(function(){
        jQuery.post($SCRIPT_ROOT + '/_set_data', { name:"ignition_status", value: this.checked});
    });
});

$(function() {
    $('#headlamp_check').change(function(){
        jQuery.post($SCRIPT_ROOT + '/_set_data', { name: "headlamp_status", value: this.checked});
    });
});

$(function() {
    $('#high_beam_check').change(function(){
        jQuery.post($SCRIPT_ROOT + '/_set_data', { name: "high_beam_status", value: this.checked});
    });
});

$(function() {
    $('#windshield_wiper_check').change(function(){
        jQuery.post($SCRIPT_ROOT + '/_set_data', { name: "windshield_wiper_status", value: this.checked});
    });
});

$(function() {
    $('#driver_door_check').change(function(){
        jQuery.post($SCRIPT_ROOT + '/_set_data', { name: "door_status", value: "driver", event: this.checked});
    });
});

$(function() {
    $('#passenger_door_check').change(function(){
        jQuery.post($SCRIPT_ROOT + '/_set_data', { name: "door_status", value: "passenger", event: this.checked});
    });
});

$(function() {
    $('#right_rear_door_check').change(function(){
        jQuery.post($SCRIPT_ROOT + '/_set_data', { name: "door_status", value: "rear_right", event: this.checked});
    });
});

$(function() {
    $('#left_rear_door_check').change(function(){
        jQuery.post($SCRIPT_ROOT + '/_set_data', { name: "door_status", value: "rear_left", event: this.checked});
    });
});

    function StartTimer() {
        setInterval(function(){
            GetData();
        }, 1000);
    }

    function ParseData(dataJSON) {
        document.getElementById("torque").innerHTML = dataJSON.torque_at_transmission;
        document.getElementById("engine_speed").innerHTML = dataJSON.engine_speed;
        document.getElementById("vehicle_speed").innerHTML = dataJSON.vehicle_speed;
        document.getElementById("fuel_consumed").innerHTML = dataJSON.fuel_consumed_since_restart;
        document.getElementById("odometer").innerHTML = dataJSON.odometer;
        document.getElementById("fuel_level").innerHTML = dataJSON.fuel_level;
        document.getElementById("latitude").innerHTML = dataJSON.latitude;
        document.getElementById("longitude").innerHTML = dataJSON.longitude;
    }

    function GetData() {
        $.getJSON($SCRIPT_ROOT + '/_get_data', ParseData );
    }

    window.onload = StartTimer();