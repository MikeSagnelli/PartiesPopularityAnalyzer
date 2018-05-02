$(document).ready(function(){
    console.log("ready!");

    $("#login-button").click(function(){
        window.location.href = "/login"
    });

    $("#small-login-button").click(function(){
        window.location.href = "/login"
    });

    $( window ).unload(function() {
        window.location.href("/logout");
    });
    
    window.onbeforeunload = function(){
        window.location.href("/logout");
    };
});