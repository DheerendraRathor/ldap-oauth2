/**
 * Created by dheerendra on 4/8/15.
 */

$("#authorizationForm").submit(function (e) {
    console.log("blah");
    var checked = [];
    $("input[name='scopes_array']:checked").each(function () {
        checked.push($(this).val());
    });

    var scope_string = checked.join(" ");
    console.log(scope_string);
    $("#id_scope").val(scope_string);
    console.log("blue");
    return true;
});
