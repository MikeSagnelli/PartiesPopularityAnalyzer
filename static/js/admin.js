$(document).ready(function(){
    console.log("ready!");

    $("#admin-form").submit(function(){
        $("#submit").prop("disabled", true);
        return true;
    });

    $( window ).unload(function() {
        window.location.href("/logout");
    });
    
    window.onbeforeunload = function(){
        window.location.href("/logout");
    };

});