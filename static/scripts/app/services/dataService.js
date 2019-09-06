(function() {
    angular
    .module('app')
    .service('dataService', dataService);

    dataService.$inject = ['$http'];

    function dataService($http) {
        this.getEmails = function getEmails() {
            return $http.get('/emails');
        };
    }
})();


  