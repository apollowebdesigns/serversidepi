(function() {
    angular
    .module('app')
    .service('dataService', dataService);

    dataservice.$inject = ['$http'];

    function dataService($http) {
        this.getEmails = function getEmails() {
            return $http.get('/emails');
        };
    }
})();


  