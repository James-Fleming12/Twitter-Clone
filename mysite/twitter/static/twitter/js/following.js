function switchScreen(){
    document.getElementById("postbutton").classList.toggle("active"); 
    document.getElementById("postbutton").classList.toggle("unactive");
    document.getElementById("accountbutton").classList.toggle("active"); 
    document.getElementById("accountbutton").classList.toggle("unactive");
    if(document.getElementById("accounts").style.visibility == "hidden"){
        document.getElementById("accounts").style.visibility = "visible"; 
        document.getElementById("posts").style.visibility = "hidden";
        document.getElementById("accounts").style.position = "static"; 
    }else{
        document.getElementById("accounts").style.visibility = "hidden";
        document.getElementById("posts").style.visibility = "visible"; 
        document.getElementById("accounts").style.position = "fixed"; 
    }
}