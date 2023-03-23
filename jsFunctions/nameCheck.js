function nameCheck() {
    var name = document.getElementById("nameText");
    
    if (!(/^[a-zA-Z]+$/.test(name.value) || name.value === "%Bank%")){
        alert("Name must contain only alphabetic characters!");
        return false;
    } else if ((/^.*bank.*$/.test(name.value) || /^.*Bank.*$/.test(name.value)) && name.value !== "%Bank%"){
        alert("You cannot have the word 'Bank' anywhere in your name.");
        return false;
    }
}