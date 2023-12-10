function handleButtonClick(event) {
    event.preventDefault()
    let coloredButton = document.getElementById("dropdownMenuButton2")
    let clickedButton = event.target;
    let targetID = clickedButton.value
    let data = JSON.stringify({'lvl': targetID, 'date': currentdate})
    console.log("Lvl_upd")
    coloredButton.setAttribute("fcolor", targetID)
    httpRequest = new XMLHttpRequest();

    if (!httpRequest) {
        alert("Giving up :( Cannot create an XMLHTTP instance");
        return false;
    }

    httpRequest.open("POST", "lvl_upd");
    httpRequest.setRequestHeader('Content-Type', 'application/json')
    httpRequest.send(data)


    return false

}

// Get all buttons in the form
let buttons = document.getElementsByName("lvl_upd");

// Attach event listener to each button
buttons.forEach(function (button) {
    button.addEventListener('click', handleButtonClick);
});