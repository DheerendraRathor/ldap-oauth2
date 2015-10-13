/**
 * Created by dheerendra on 4/8/15.
 */

$("#authorizationForm").submit(function () {
    var checked = [];
    $("input[name='scopes_array']:checked").each(function () {
        checked.push($(this).val());
    });

    var scope_string = checked.join(" ");
    $("#id_scope").val(scope_string);
    return true;
});
