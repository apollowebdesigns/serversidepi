(function() {
    angular
    .module('app')
    .service('serverSentEventService', serverSentEventService);

    serverSentEventService.$inject = ['$http'];

    function serverSentEventService($http) {
        this.getEmails = function getEmails() {
            return $http.get('/emails');
        };
    }
})();


