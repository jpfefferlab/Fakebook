
function onChatDrawerUserClicked(userId) {
    var iframe = window.frameElement
    if(iframe !== null) {
        parent.chatWithUserRequested(userId)
    }
}

function applyFilter(searchString) {
    let usersList = document.getElementById("users-list")
    usersList.querySelectorAll(".user-section").forEach(userSection => {
        let username = userSection.querySelector(".username").textContent
        userSection.style.display = (username.toLowerCase().includes(searchString.toLowerCase())) ? "block" : "none"
    })
}

window.onload = (e) => {

    // hide toggle button in parent if chat is disabled
    if(document.getElementById("user-list-not-shown-indicator") !== null) {
        parent.document.body.querySelector("#chat-drawer-toggle-button").style.display = "none"
    }

    let filterTextfield = document.getElementById("filter-textfield");
    if(filterTextfield !== null) {
        filterTextfield.addEventListener("input", e => {
            applyFilter(filterTextfield.value)
        }, false)
    } else {
        console.log("filter-textfield not found, chat drawer search inactive")
    }
}