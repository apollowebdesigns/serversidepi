angular
    .module('app')
    .service('driveService', driveService);

driveService.$inject = ['$http'];

function driveService($http) {
    this.sse = '';
    this.forwardsPromise = function () {
        return $http.get( "/end_motor_source");
    }
}