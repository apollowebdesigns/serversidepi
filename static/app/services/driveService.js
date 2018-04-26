angular
    .module('app')
    .service('driveService', driveService);

driveService.$inject = ['$http'];

function driveService($http) {
    this.sse = '';
    this.forwardsPromise = function () {
        return $http.get( "/end_motor_source")
                        .then(function(data) {
                        $log.info('ending');
                        $( ".result" ).html( data );
                    })
                    .catch(function() {
                        $log.error('an error happened in the drive service');
                    });
    }
}