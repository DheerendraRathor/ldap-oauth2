/**
 * Created by dheerenr on 6/7/15.
 */

var $errorAlert = $("#error-alert");

if (!String.prototype.format) {
    String.prototype.format = function () {
        var args = arguments;
        return this.replace(/{(\d+)}/g, function (match, number) {
            return typeof args[number] != 'undefined'
                ? args[number]
                : match
                ;
        });
    };
}


$errorAlert.on("close.bs.alert", function (e) {
    e.preventDefault();
    $(this).hide();
});