/**
 * Created by dheerendra on 26/9/15.
 */

var $body = $('body');
var addInputClass = 'add-input';
var removeInputClass = 'remove-input';

$body.on('click', 'a.add-input', function(e){
    e.preventDefault();
    var $form_group = $(this).closest('.form-group');
    var $new_anchor = $form_group.clone();
    var $new_input = $new_anchor.find('input');
    $new_input.val('');
    $new_input.focus();
    $new_anchor.insertAfter($form_group);
    $(this).removeClass(addInputClass);
    $(this).addClass(removeInputClass);
    $(this).children('span').removeClass('glyphicon-plus');
    $(this).children('span').addClass('glyphicon-minus');
});

$body.on('click', 'a.remove-input', function(e){
    e.preventDefault();
    var $form_group = $(this).closest('.form-group');
    $form_group.remove();
});