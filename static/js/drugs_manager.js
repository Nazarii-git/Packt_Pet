let lists = document.getElementsByClassName("list-group-item")
let rightbox = document.getElementById("right")
let leftbox = document.getElementById("left")
let selected


for (let list of lists) {
    list.addEventListener("dragstart", function (e) {
        selected = e.target
        rightbox.style.borderStyle = "dotted"
    })
    rightbox.addEventListener("dragover", function (e) {
        e.preventDefault()
    })
    rightbox.addEventListener("drop", function (e) {
        if (selected !== null) {
            let newItem = selected.cloneNode(true)
            newItem.getElementsByClassName("rounded-pill")[0].style.display = "none"
            rightbox.appendChild(newItem)
            selected.getElementsByClassName("rounded-pill")[0].textContent--
            marktask(newItem)
            points += parseInt(newItem.getAttribute("data-task-points"))
            progressbar(points)
        }
        selected = null
        rightbox.style.borderStyle = "none"
    })
    leftbox.addEventListener("dragover", function (e) {
        e.preventDefault()
    })
    leftbox.addEventListener("drop", function (e) {
        if (selected !== null) {
            leftbox.appendChild(selected)
        }
        selected = null

    })

}