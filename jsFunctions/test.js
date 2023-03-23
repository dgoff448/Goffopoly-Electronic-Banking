function myGeeks() {
    var x = document.getElementById("GFG");
    alert(x.innerHTML)
    if (x.innerHTML === "Welcome to GeeksforGeeks") {
        x.innerHTML = "A computer science portal for geeks";
    } else {
        x.innerHTML = "Welcome to GeeksforGeeks";
    }
}