$(function() {
    var input = $( "#accelerator" );
    var slider = $( "<div id='slider'></div>" ).insertAfter( input ).slider({
      min: 0,
      max: 100,
      value: 0,
      slide: function( event, ui ) {
          input.val(ui.value);
          jQuery.post($SCRIPT_ROOT + '/accelerator', { accelerator: ui.value});
      }
    });
    $( "#accelerator" ).change(function() {
        slider.slider( "value", this.value );
        jQuery.post($SCRIPT_ROOT + '/accelerator', { accelerator: this.value});
    });
  });

$(function() {
    var input = $( "#steering_wheel" );
    var slider = $( "<div id='slider'></div>" ).insertAfter( input ).slider({
      min: -600,
      max: 600,
      value: 0,
      slide: function( event, ui ) {
          input.val(ui.value);
          jQuery.post($SCRIPT_ROOT + '/steering', { angle: ui.value});
      }
    });
    $( "#steering_wheel" ).change(function() {
        slider.slider( "value", this.value );
        jQuery.post($SCRIPT_ROOT + '/steering', { angle: this.value});
    });
  });

    function StartTimer() {
        setInterval(function(){
            GetData();
        }, 1000);
    }

    function ParseData(dataJSON) {
        document.getElementById("vehicle_speed").innerHTML = dataJSON.vehicle_speed;
        document.getElementById("fuel_consumed").innerHTML = dataJSON.fuel_consumed_since_restart;
        document.getElementById("odometer").innerHTML = dataJSON.odometer;
    }

    function oldGetData() {
        var xmlHttp = null;
        xmlHttp = new XMLHttpRequest();
        xmlHttp.open( "GET", "http://localhost:5000/_get_data", false);
        xmlHttp.send( null );
        return xmlHttp.responseText;
    }

    function GetData() {
        $.getJSON($SCRIPT_ROOT + '/_get_data', ParseData );
    }

    window.onload = StartTimer();