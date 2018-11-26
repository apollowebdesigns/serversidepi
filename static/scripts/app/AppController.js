(function() {
    angular
      .module('app')
      .controller('AppController', AppController);

    function AppController() {
        var vm = this;
    
        vm.test = 'test I have been rendered';

        vm.testMethod = function() {
            vm.test = Math.random() * 4;
        }
    }
})();
  