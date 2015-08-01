/**
 * Created by dheerenr on 6/7/15.
 */

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


$("#error-alert").on("close.bs.alert", function (e) {
    e.preventDefault();
    $(this).hide();
});