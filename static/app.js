function killRequest() {
    return $.get( "/end_motor_source", function(data) {
                    console.log('ending');
                    $( ".result" ).html( data );
                });
}

(function($){
    $(function(){
        var currentUrl = $(location).attr('href');
        var firstPosition = currentUrl.indexOf("1");
        var lastPosition = currentUrl.indexOf(":");
        //remove extra url for ui router params
        var removeSlash = currentUrl.length - 1;
        var secondUrl = currentUrl.toString().slice(0, removeSlash);
        var rawness = String.raw`:2222/html/min.php`;
        var calcUrl = secondUrl.concat(rawness);
        console.log("the current url is");
        console.log(calcUrl);
        $("#camera-screen").attr("src", calcUrl);
    });
})(jQuery);

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}
  
async function demo() {
    console.log('Taking a break...');
    await sleep(2000);
    console.log('Two second later');
}

function engageAutomaticMode() {
    // Open up forwards
    var sseForwards = new EventSource('/my_event_source');

    // Start event source for ultrasonic sensor
    var sseUltrasonic = new EventSource('http://192.168.1.67/my_event_source');

    // Set directions
    // sseForwards = new EventSource('/my_event_source');

    sseUltrasonic.onmessage = async function(message) {
        console.log('Message from ultrasonic sensor');
        document.getElementById('output').innerHTML = message.data;
        console.log('what is the message for automatic?');
        console.log(message.data);
        let distance = message.data;

        if (distance < 6) {
            console.error('STOP');
            document.getElementById('stop').innerHTML = 'STOP';
            sseForwards.close();
            await $.get( "/end_motor_source", function(data) {
                console.log('stop forwards');
                $( ".result" ).html( data );
            });
            sseRight = new EventSource('/right');
            sseRight.onmessage = function(message) {
                console.log('right!');
                $('#output').append('<li>'+message.data+'</li>');
                
            }
            demo();
            sseRight.close();
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

            $('#automatic').click(engageAutomaticMode);

            $('#dist').mouseup(function(){
                sse.close();
                $.get( "/end_motor_source", function(data) {
                    console.log('ending');
                    $( ".result" ).html( data );
                });
                return killRequest();
            }).mousedown(function(){
                sse = new EventSource('/distance');
                sse.onmessage = function(message) {
                    console.log('finding that distance');
                    console.log(message);
                    $('#distance').append('<li>'+message.data+'</li>');
                }
            })

            $('#forwards').mouseup(function(){
                sse.close();
                $.get( "/end_motor_source", function(data) {
                    console.log('ending');
                    $( ".result" ).html( data );
                });
                return killRequest();
            }).mousedown(function(){
                sse = new EventSource('/my_event_source');
                sse.onmessage = function(message) {
                    console.log('A message has arrived!');
                    $('#output').append('<li>'+message.data+'</li>');
                }
            })

            $('#backwards').mouseup(function(){
                sse.close();
                $.get( "/end_motor_source", function(data) {
                    console.log('ending');
                    $( ".result" ).html( data );
                });
                return killRequest();
            }).mousedown(function(){
                sse = new EventSource('/backwards');
                sse.onmessage = function(message) {
                    console.log('A message has arrived!');
                    $('#output').append('<li>'+message.data+'</li>');
                }
            })

            $('#right').mouseup(function(){
                sse.close();
                $.get( "/end_motor_source", function(data) {
                    console.log('ending');
                    $( ".result" ).html( data );
                });
                return killRequest();
            }).mousedown(function(){
                sse = new EventSource('/right');
                sse.onmessage = function(message) {
                    console.log('A message has arrived!');
                    $('#output').append('<li>'+message.data+'</li>');
                }
            })

            $('#left').mouseup(function(){
                sse.close();
                $.get( "/end_motor_source", function(data) {
                    console.log('ending');
                    $( ".result" ).html( data );
                });
                return killRequest();
            }).mousedown(function(){
                sse = new EventSource('/left');
                sse.onmessage = function(message) {
                    console.log('A message has arrived!');
                    $('#output').append('<li>'+message.data+'</li>');
                }
            })
        })