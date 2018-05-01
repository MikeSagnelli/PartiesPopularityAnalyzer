$(document).ready(function(){
    console.log("ready!");

    $("#login-button").click(function(){
        window.location.href = "/login"
    });

    $("#small-login-button").click(function(){
        window.location.href = "/login"
    });

    $("#home-btn").click(function(){
        window.location.href = "/"
    });

    $("#about-btn").click(function(){
        window.location.href = "/#about"
    });

    $("#contact-btn").click(function(){
        window.location.href = "/#contact"
    });  
});