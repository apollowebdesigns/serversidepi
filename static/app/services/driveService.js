angular
    .module('app')
    .service('driveService', driveService);

function driveService() {
    this.serviceTest = 'hello from the service!';
}