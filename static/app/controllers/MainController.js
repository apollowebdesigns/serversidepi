angular
    .module('app')
    .controller('MainController', MainController);

function MainController() {
    var vm = this;

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

    // $('#automatic').click(() => engageAutomaticMode(false, sse));
    // $('#manual').click(() => engageAutomaticMode(true, sse));
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

    vm.automatic = function() {
        return eventSourceCreator('/distance');
    }

    vm.stop = function () {
        return stopRequest;
    }

    vm.distance = function(){
        eventSourceCreator('/my_event_source');
    }

    vm.ultrasonic = function() {
        return ultrasonicSourceCreator();
    }

    vm.ultrasonicStop = function() {
        return stopUltrasonicRequest();
    } 

    
    vm.forwards = function() { 
        return eventSourceCreator('/my_event_source');
    } 

    vm.backwards = function() {
        return eventSourceCreator('/backwards');
    }

    vm.right = function() {
        return eventSourceCreator('/right');
    } 

    vm.left = function() {
        return eventSourceCreator('/left');
    } 

    vm.test = 'hello from angular js!!!';
}