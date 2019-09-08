(function() {
    angular
      .module('app')
      .controller('AppController', AppController);

    function AppController() {
        var vm = this;
    
        vm.test = 'test I have been rendered';
        vm.sse = null;

        vm.eventSourceCreator = eventSourceCreator;
        vm.engageManualMode = engageManualMode;

        function eventSourceCreator(direction){
            vm.sse = new EventSource(direction);
            vm.sse.onmessage = function(message) {
                console.log('A message has arrived!');
                document.getElementById('output').innerHTML = JSON.stringify(message.data);
                console.log(message.data);
            };
            vm.sse.onerror = function(err) {
                console.error('There has been an error!!');
                document.getElementById('output').innerHTML = JSON.stringify(err);
                console.error(err);
            }
        }

        function engageManualMode() {
            vm.sse.close();
            $.get( "/end_motor_source", function(data) {
                console.log('ending');
                $( ".result" ).html(data);
            });
            return killRequest();
        }

        vm.testMethod = function() {
            vm.test = Math.random() * 4;
        }
    }
})();
  