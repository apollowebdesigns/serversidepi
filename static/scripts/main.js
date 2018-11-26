angular
    .module('app', ['ngTouch']);


angular
  .module('app')
  .controller('AppController', AppController);

function AppController() {
  var vm = this;

  vm.test = 'test I have been rendered';
}
