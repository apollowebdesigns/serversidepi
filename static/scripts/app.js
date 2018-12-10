

function killRequest() {
    return $.get( "/end_motor_source", function(data) {
                    console.log('ending');
                    $( ".result" ).html( data );
                });
}

function getPiTemperature() {
    return $.get('/get_pi_temp').then(function(piTemperature) {
        return $('#piTemperature').html(piTemperature);
    });
}

$(document).ready(
        function() {
            var sse, sse1, sseUltrasonic;

            let piTemperature;

            getPiTemperature() ;

            function http(endpoint){
                return $.get(endpoint, function(data) {
                    console.log('ending');
                    $( ".result" ).html( data );
                });
            }

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
                sseUltrasonic = new EventSource('http://192.168.1.83/forwards');
                sseUltrasonic.onmessage = function(message) {
                    console.log('ultrasonic message here');
                    if (parseInt(message.data) < 8) {
                        console.error('too close');
                        $('#output').append('too close!!!!');
                        stopRequest();
                        eventSourceCreator('/right')
                    }   else {
                        eventSourceCreator('/forwards')
                        $('#output').append('<li>'+message.data+'</li>');
                    }
                }
            }

            $('#stop').mouseup(stopRequest)
            $('#forwards').mouseup(stopRequest).mousedown(() => eventSourceCreator('/forwards'))
            $('#backwards').mouseup(stopRequest).mousedown(() => eventSourceCreator('/backwards'))
            $('#right').mouseup(stopRequest).mousedown(() => eventSourceCreator('/right'))
            $('#left').mouseup(stopRequest).mousedown(() => eventSourceCreator('/left'))
            $('#distance').click(() => {
                return $.get('/distance', (data, status) => {
                    console.log('distance hit');
                    console.log(data);
                    console.log(status);
                })
            })
            $('#manual').click(() => {
                return $.get('/manual', (data, status) => {
                    console.log('manual, now stopping');
                    console.log(data);
                    console.log(status);
                })
            })

            function createTouchElement(direction) {
                var myElement = document.getElementById(direction);
                var hammertime = new Hammer(myElement);

                hammertime.on('press', () => eventSourceCreator('/' + direction));
                hammertime.on('pressup', stopRequest);

                return {
                    direction: direction,
                    touchElement: hammertime
                }
            }

            var directions = ['forwards', 'backwards', 'left', 'right'];
            var touchElements = directions.map(createTouchElement);
        })