function killRequest() {
    return $.get( "/end_motor_source", function(data) {
                    console.log('ending');
                    $( ".result" ).html( data );
                });
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}
  
async function demo() {
    console.log('Taking a break...');
    await sleep(2000);
    console.log('Two second later');
}

function engageAutomaticMode(orManual, sseForwards) {
    
    // Open up forwards
    sseForwards = new EventSource('/my_event_source');

    // Start event source for ultrasonic sensor
    var sseUltrasonic = new EventSource('http://192.168.1.67/my_event_source');

    // Set directions
    // sseForwards = new EventSource('/my_event_source');
    if(orManual) {
        
    }

    sseUltrasonic.onmessage = async function(message) {
        console.log('Message from ultrasonic sensor');
        document.getElementById('output').innerHTML = message.data;
        console.log('what is the message for automatic?');
        console.log(message.data);
        let distance = message.data;

        function flickRight() {
            return new Promise(resolve => setTimeout(function(){
                sseRight = new EventSource('/right');
                sseRight.onmessage = function(message) {
                    console.log('right!');
                    $('#output').append('<li>'+message.data+'</li>');
                    
                }
                
                sseRight.close();

                return $.get( "/end_motor_source", function(data) {
                    console.log('stop moving right');
                    $( ".result" ).html( data );
                });
            },2000))
        }

        if (distance < 6) {
            console.error('STOP');
            document.getElementById('stop').innerHTML = 'STOP';
            console.log('before the end');
            sseForwards.close();
            await $.get( "/end_motor_source", function(data) {
                console.log('stop forwards');
                $( ".result" ).html( data );
            });

            var thing = await flickRight();
            
            await $.get( "/end_motor_source", function(data) {
                console.log('right has finished');
                $( ".result" ).html( data );
            });

            // Reset to fowards
            sseForwards = new EventSource('/my_event_source');
        }
        else {
            console.info('still going');
            document.getElementById('stop').innerHTML = 'GO'
            sseForwards.onmessage = function(message) {
                console.log('A message has arrived!');
                $('#output').append('<li>'+message.data+'</li>');
            }
        };

    }
}

$(document).ready(
        function() {
            var sse, sse1;

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
                    $('#output').append('<li>'+message.data+'</li>');
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

            $('#automatic').click(() => engageAutomaticMode(false, sse));
            $('#manual').click(() => engageAutomaticMode(true, sse));

            $('#stop').mouseup(stopRequest)
            $('#distance').click(() => eventSourceCreator('/my_event_source'))
            $('#forwards').mouseup(stopRequest).mousedown(() => eventSourceCreator('/my_event_source'))
            $('#backwards').mouseup(stopRequest).mousedown(() => eventSourceCreator('/backwards'))
            $('#right').mouseup(stopRequest).mousedown(() => eventSourceCreator('/right'))
            $('#left').mouseup(stopRequest).mousedown(() => eventSourceCreator('/left'))
        })