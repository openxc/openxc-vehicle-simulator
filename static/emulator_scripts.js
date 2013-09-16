$(function() {
    var input = $( "#steering_wheel" );
    var slider = $( "<div id='slider'></div>" ).insertAfter( input ).slider({
      min: -600,
      max: 600,
      value: 0,
      slide: function( event, ui ) {
          input.val(ui.value);
          jQuery.post($SCRIPT_ROOT + '/_set_data', { angle: ui.value});
      }
    });
    $( "#steering_wheel" ).change(function() {
        slider.slider( "value", this.value );
        jQuery.post($SCRIPT_ROOT + '/_set_data', { angle: this.value});
    });
  });

$(function() {
    var input = $( "#accelerator" );
    var slider = $( "<div id='slider'></div>" ).insertAfter( input ).slider({
      min: 0,
      max: 100,
      value: 0,
      slide: function( event, ui ) {
          input.val(ui.value);
          jQuery.post($SCRIPT_ROOT + '/_set_data', { accelerator: ui.value});
      }
    });
    $( "#accelerator" ).change(function() {
        slider.slider( "value", this.value );
        jQuery.post($SCRIPT_ROOT + '/_set_data', { accelerator: this.value});
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
          jQuery.post($SCRIPT_ROOT + '/_set_data', { brake: ui.value});
      }
    });
    $( "#brake" ).change(function() {
        slider.slider( "value", this.value );
        jQuery.post($SCRIPT_ROOT + '/_set_data', { brake: this.value});
    });
  });

$(function() {
    $('#parking_brake_check').change(function(){
        jQuery.post($SCRIPT_ROOT + '/_set_data', { parking_brake_status: this.checked});
    });
});

$(function() {
    $('#ignition_check').change(function(){
        jQuery.post($SCRIPT_ROOT + '/_set_data', { ignition_status: this.checked});
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