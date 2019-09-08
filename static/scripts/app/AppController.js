(function() {
    angular
      .module('app')
      .controller('AppController', AppController);

    AppController.$inject = ['$log', 'serverSentEventService'];

    function AppController($log, serverSentEventService) {
        var vm = this;
        vm.sse = null;
        vm.sseDataStore = serverSentEventService.sseDataStore;
        vm.eventSourceCreator = eventSourceCreator;
        vm.engageManualMode = engageManualMode;
        vm.killRequest = serverSentEventService.killRequest;

        function eventSourceCreator(direction){
            vm.sseDataStore[direction] = new EventSource(direction);
            vm.sseDataStore[direction].onmessage = function(message) {
                $log.log('A message has arrived!');
                document.getElementById('output').innerHTML = JSON.stringify(message.data);
                $log.log(message.data);
            };
            vm.sseDataStore[direction].onerror = function(err) {
                $log.error('There has been an error!!');
                document.getElementById('output').innerHTML = JSON.stringify(err);
                $log.error(err);
            }
        }

        function engageManualMode() {
            for (direction in vm.sseDataStore) {
                vm.sseDataStore[direction].close();
            }
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
  