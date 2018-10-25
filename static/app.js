function killRequest() {
    return $.get( "/end_motor_source", function(data) {
                    console.log('ending');
                    $( ".result" ).html( data );
                });
}

$(document).ready(
        function() {
            var sse, sse1, sseUltrasonic;

            function stopRequest(){
                sse.close();
                $.get( "/end_motor_source", function(data) {
                    console.log('ending');
                    $( ".result" ).html( data );
                });
                return killRequest();
            }

            function eventSourceCreator(direction){
                sse = new EventSource(direction);
                sse.onmessage = function(message) {
                    console.log('A message has arrived!');
                    document.getElementById('output').innerHTML = JSON.stringify(message.data);
                    console.log(message.data);
                }
                sse.onerror = function(err) {
                    console.error('There has been an error!!');
                    document.getElementById('output').innerHTML = JSON.stringify(err);
                    console.error(message.data);
                }
            }

            function engageManualMode() {
                sse.close();
                $.get( "/end_motor_source", function(data) {
                    console.log('ending');
                    $( ".result" ).html( data );
                });
                return killRequest();
            }

            function stopUltrasonicRequest(){
                return sseUltrasonic.close();
            }

            function ultrasonicSourceCreator(){
                console.log('inside ultrasonic')
                sseUltrasonic = new EventSource('http://192.168.1.83/my_event_source');
                sseUltrasonic.onmessage = function(message) {
                    console.log('ultrasonic message here');
                    if (parseInt(message.data) < 8) {
                        console.error('too close');
                        $('#output').append('too close!!!!');
                        stopRequest();
                        eventSourceCreator('/right')
                    }   else {
                        eventSourceCreator('/my_event_source')
                        $('#output').append('<li>'+message.data+'</li>');
                    }
                }
            }

            $('#stop').mouseup(stopRequest)
            $('#forwards').mouseup(stopRequest).mousedown(() => eventSourceCreator('/my_event_source'))
            $('#backwards').mouseup(stopRequest).mousedown(() => eventSourceCreator('/backwards'))
            $('#right').mouseup(stopRequest).mousedown(() => eventSourceCreator('/right'))
            $('#left').mouseup(stopRequest).mousedown(() => eventSourceCreator('/left'))

            $('#distance').click(() => eventSourceCreator('/distance'))
            $('#manual').click(() => eventSourceCreator('/manual'))
        })