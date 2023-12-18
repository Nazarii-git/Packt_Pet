let httpRequest;
let globaltaskid
let input = document.getElementById("inputTaskField");

// Execute a function when the user presses a key on the keyboard
input.addEventListener("keypress", function(event) {
  // If the user presses the "Enter" key on the keyboard
  if (event.key === "Enter") {
    // Cancel the default action, if needed
    event.preventDefault();
    // Trigger the button element with a click
    addSingleTask()
  }
});


let checkboxes = document.getElementsByClassName('task-check');

        // Attach an event listener to each checkbox
        for (let i = 0; i < checkboxes.length; i++) {
            let flag = parseInt(checkboxes[i].getAttribute("data-in-db"))

            checkboxes[i].checked = flag

            checkboxes[i].addEventListener('change', function (e) {
                // Check if the current checkbox is checked
                if (this.checked) {
                    console.log('Checkbox is checked!');
                    e.stopPropagation()
                    console.log(this.parentNode.id)
                } else {
                    console.log('Checkbox is unchecked!');

                    editSingleTask(this, 0)
                }
            });
        }

function editSingleTask(checkbox, value) {
    let id = checkbox.parentNode.id;

    fetch("/editSingleTaskReq", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ id: id, value: value }),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Network response was not ok");
        }
        console.log("Added single task!");
    })
    .catch(error => {
        console.error("Error during the fetch operation:", error);
    });
}
function addSingleTask(){

    let tasktext = (input.value)
    input.value = ""
    httpRequest = new XMLHttpRequest();

    if (!httpRequest) {
        alert("Giving up :( Cannot create an XMLHTTP instance");
        return false;
    }

    httpRequest.open("POST", "addSingleTaskReq");
    httpRequest.send(tasktext)

    console.log("Added single task!")
}
function marktask(task) {
        let coloredButton = document.getElementById("dropdownMenuButton2")
    let currentdate = coloredButton.getAttribute("data-date-id")
    httpRequest = new XMLHttpRequest();
    let data = JSON.stringify({'taskName': task.firstChild.textContent, 'date': currentdate})
    if (!httpRequest) {
        alert("Giving up :( Cannot create an XMLHTTP instance");
        return false;
    }

    httpRequest.open("POST", "ajax");
    httpRequest.setRequestHeader('Content-Type', 'application/json')
    httpRequest.send(data)
}

function addTask(e) {
    e.preventDefault()
    forma = document.getElementById('addTaskForm')
    addForm = new FormData(forma)

    httpRequest = new XMLHttpRequest();

    if (!httpRequest) {
        alert("Giving up :( Cannot create an XMLHTTP instance");
        return false;
    }

    httpRequest.open("POST", "addTaskReq");
    httpRequest.send(addForm)

    $('#addTaskModal').modal('hide')
    console.log("Js form add task!")

    return false

}

function delTask(e) {
    console.log("Deletign item")
    let target = e.parentNode.parentNode
    points -= parseInt(target.getAttribute("data-task-points"))
    progressbar(points)
    let targetID = target.id.toString()
    httpRequest = new XMLHttpRequest();

    if (!httpRequest) {
        alert("Giving up :( Cannot create an XMLHTTP instance");
        return false;
    }

    httpRequest.open("POST", "delTaskReq");
    httpRequest.send(targetID)

    target.remove()

    return false

}

function delregTask() {
    console.log("Deletign regular item")
    httpRequest = new XMLHttpRequest();

    if (!httpRequest) {
        alert("Giving up :( Cannot create an XMLHTTP instance");
        return false;
    }

    httpRequest.open("POST", "delRegTaskReq");
    httpRequest.send(globaltaskid)
    document.getElementById(globaltaskid).remove()

    return false

}


function saveTask(e) {
    e.preventDefault()
    console.log("Saving task")
    forma = document.getElementById('addTaskForm')
    addForm = new FormData(forma)
    addForm.append("id", globaltaskid)

    httpRequest = new XMLHttpRequest();

    if (!httpRequest) {
        alert("Giving up :( Cannot create an XMLHTTP instance");
        return false;
    }

    httpRequest.open("POST", "EditTaskReq");
    httpRequest.send(addForm)

    $('#addTaskModal').modal('hide')
    forma.reset()
    console.log("Js form edit task!")


    return false
}


// Function to fill the form with current values
function fillForm(currentValues) {
    // Iterate over the current values object
    for (let field in currentValues) {
        if (currentValues.hasOwnProperty(field)) {
            // Access form elements and set values
            document.getElementById(field).value = currentValues[field];
        }
    }
}


// Call the fillForm function when the modal is opened or when needed
function editTask(e) {
    console.log("Editing task window")
    console.log(e.target)
    globaltaskid = e.id
    let target = e
    let taskId = target.id.toString()
    let button = document.getElementById("modalbutton")
    let modaltitle = document.getElementById("addTaskModalLabel")
    let modalaction = document.getElementById("addTaskForm")
    modalaction.setAttribute("onsubmit", "saveTask(event)")
    modaltitle.textContent = "Edit Task"
    button.textContent = "Save Changes"

    // AJAX request to get current values from Flask based on task id
    fetch(`/detailsTaskReq/${taskId}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Task not found');
            }
            return response.json();
        })
        .then(data => fillForm(data))
        .catch(error => console.error('Error:', error));
    $('#addTaskModal').modal('show')
    $('#addTaskModal').on('hidden.bs.modal', function (e) {
        let button = document.getElementById("modalbutton")
        let modaltitle = document.getElementById("addTaskModalLabel")
        modalaction.setAttribute("onsubmit", "addTask(event)")
        modaltitle.textContent = "Add Task"
        button.textContent = "Add "
        forma = document.getElementById('addTaskForm')
        forma.reset()
    })


    return false

}