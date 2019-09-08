(function () {
        angular
            .module('app')
            .service('serverSentEventService', serverSentEventService);

        serverSentEventService.$inject = ['$http', '$log'];

        function serverSentEventService($http, $log) {
            this.sseDataStore = {};

            this.getEmails = function getEmails() {
                return $http.get('/emails');
            };

            this.distance = function () {
                return $http.get("/distance").then(function (success) {
                    $log.log('distance mode engaged');
                }).catch(function (error) {
                    $log.error('error with distance mode');
                    $log.error(error);
                })
            };
            this.killRequest = function () {
                return $http.get("/end_motor_source").then(function (success) {
                    $log.log('ended successfully');
                }).catch(function (error) {
                    $log.error('there was an error');
                    $log.error(error);
                });
            };
        }
    }
)();


