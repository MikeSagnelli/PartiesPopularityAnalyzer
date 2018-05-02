$(document).ready(function(){
    console.log("ready!");

    $("#admin-form").submit(function(){
        $("#submit").prop("disabled", true);
        return true;
    });
    
});