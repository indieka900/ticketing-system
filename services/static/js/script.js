const body = document.querySelector("body"),
      modeToggle = body.querySelector(".mode-toggle");
      sidebar = body.querySelector("nav");
      sidebarToggle = body.querySelector(".sidebar-toggle");

let getMode = localStorage.getItem("mode");
if(getMode && getMode ==="dark"){
    body.classList.toggle("dark");
}

let getStatus = localStorage.getItem("status");
if(getStatus && getStatus ==="close"){
    sidebar.classList.toggle("close");
}

modeToggle.addEventListener("click", () =>{
    body.classList.toggle("dark");
    if(body.classList.contains("dark")){
        localStorage.setItem("mode", "dark");
    }else{
        localStorage.setItem("mode", "light");
    }
});

sidebarToggle.addEventListener("click", () => {
    sidebar.classList.toggle("close");
    if(sidebar.classList.contains("close")){
        localStorage.setItem("status", "close");
    }else{
        localStorage.setItem("status", "open");
    }
})

// Hide Show Divs
function hideShow () {
    var x = document.getElementById("D0");
    var a = document.getElementById("D1");
    var b = document.getElementById("D2");
    var c = document.getElementById("D3");


    if (x.style.display === "none") {
    x.style.display = "block";
    a.style.display = "none";
    b.style.display = "none";
    c.style.display = "none";



    } else {
    x.style.display = "block";
    a.style.display = "none";
    b.style.display = "none";
    c.style.display = "none";



     }
    }

    function hideShow1 () {
    var x = document.getElementById("D1");
    var a = document.getElementById("D0");
    var b = document.getElementById("D2");
    var c = document.getElementById("D3");

    if (x.style.display === "none") {
    x.style.display = "block";
    a.style.display = "none";
    b.style.display = "none";
    c.style.display = "none";


    } else {
    x.style.display = "block";
    a.style.display = "none";
    b.style.display = "none";
    c.style.display = "none";

     }

    }

    function hideShow2 () {
    var x = document.getElementById("D2");
    var a = document.getElementById("D0");
    var b = document.getElementById("D1");
    var c = document.getElementById("D3");

    if (x.style.display === "none") {
    x.style.display = "block";
    a.style.display = "none";
    b.style.display = "none";
    c.style.display = "none";

    } else {
    x.style.display = "block";
    a.style.display = "none";
    b.style.display = "none";
    c.style.display = "none";


     }
    }

    function hideShow3 () {
    var x = document.getElementById("D3");
    var a = document.getElementById("D0");
    var b = document.getElementById("D1");
    var c = document.getElementById("D2");

    if (x.style.display === "none") {
    x.style.display = "block";
    a.style.display = "none";
    b.style.display = "none";
    c.style.display = "none";
    } else {
    x.style.display = "block";
    a.style.display = "none";
    b.style.display = "none";
    c.style.display = "none";
     }
    }

