(function() {
    angular
      .module('app')
      .controller('AppController', AppController);

    AppController.$inject = ['$log', 'serverSentEventService'];

    function AppController($log, serverSentEventService) {
        var vm = this;
        vm.sse = null;
        vm.eventSourceCreator = eventSourceCreator;
        vm.engageManualMode = engageManualMode;
        vm.killRequest = serverSentEventService.killRequest;

        function eventSourceCreator(direction){
            vm.sse = new EventSource(direction);
            vm.sse.onmessage = function(message) {
                $log.log('A message has arrived!');
                document.getElementById('output').innerHTML = JSON.stringify(message.data);
                $log.log(message.data);
            };
            vm.sse.onerror = function(err) {
                $log.error('There has been an error!!');
                document.getElementById('output').innerHTML = JSON.stringify(err);
                $log.error(err);
            }
        }

        function engageManualMode() {
            vm.sse.close();
            $.get( "/end_motor_source", function(data) {
                $log.log('ending');
                $( ".result" ).html(data);
            });
            return vm.killRequest();
        }

        vm.testMethod = function() {
            vm.test = Math.random() * 4;
        }
    }
})();
  