$(document).ready(function(){
    console.log("ready!");

    $( window ).unload(function() {
        window.location.href("/logout");
    });
    
    window.onbeforeunload = function(){
        window.location.href("/logout");
    };

});