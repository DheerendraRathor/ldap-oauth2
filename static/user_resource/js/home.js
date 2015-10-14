/**
 * Created by dheerendra on 26/9/15.
 */

var $body = $('body');
var addInputClass = 'add-input';
var removeInputClass = 'remove-input';
var profileBadgeFormSubmitUrl;
var $ppUploadButton = $('.pp-upload-button');
var $ppUploadInput = $('#pp-upload-input');
var $profileBadgeForm = $('#profile-badge-form');
var $errorAlertContent = $('#error-alert-content');

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

$ppUploadButton.click(function(){
    if ($(this).hasClass('timer-loader')){
        return;
    }
    $ppUploadInput.click();
});

$ppUploadInput.change(function () {
    $profileBadgeForm.submit();
});

$profileBadgeForm.submit(function(event){
    event.preventDefault();
    var formData = new FormData($(this)[0]);
    $.ajax({
        url: profileBadgeFormSubmitUrl,
        data: formData,
        type: 'POST',
        processData: false,
        contentType: false,
        success: function(data){
            data = JSON.parse(data);
            $("#profile-picture").attr('src', data.url);
        },
        error: function(data){
            $errorAlertContent.html('');
            data = JSON.parse(data.responseText);
            for (var key in data){
                if (data.hasOwnProperty(key)){
                    var error_list = data[key];
                    for (var index in error_list){
                        $errorAlertContent.append('<li>' + error_list[index] + '</li>');
                    }
                }
            }
            $errorAlert.show();
        },
        complete: function(){
            $ppUploadButton.removeClass('timer-loader');
        }
    });
    $ppUploadButton.addClass('timer-loader');
});