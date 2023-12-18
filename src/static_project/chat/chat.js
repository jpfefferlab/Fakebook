
// ---------------------------
// Frontend
// ---------------------------

chat = {

}

function getIframeBoundingRect() {
    return iframeContainerDiv.getBoundingClientRect() // set by chat manager
}

function createEmojiPicker() {
    let toggleButton = document.getElementById("reaction-drawer-button")
    let messageTextfield = document.getElementById("message-textfield")

    let pickerContainer = document.createElement("div")
    let picker = document.createElement("emoji-picker")

    pickerContainer.appendChild(picker)

    toggleButton.addEventListener("click", e => {
        if(pickerContainer.style.display === "none") {
            // show and set position
            pickerContainer.style.display = "block"

            let boundingRect = getIframeBoundingRect()

            pickerContainer.style.left = `${boundingRect.x}px`
            pickerContainer.style.top = `${boundingRect.y - 105}px`
        } else {
            pickerContainer.style.display = "none"
        }
    })

    messageTextfield.addEventListener("click", e => {
        pickerContainer.style.display = "none"
    })

    picker.addEventListener("emoji-click", e => {
        pickerContainer.style.display = "none"
        messageTextfield.value += e.detail.unicode
    })

    setTimeout(() => {
        picker.classList.add("light")  // don't use css as this will be added to the parent of the iframe

        pickerContainer.style.display = "none"
        parent.document.body.appendChild(pickerContainer)


        pickerContainer.style.position = "fixed"
        // position is set on show to adjust for resize

    }, 1000)  // need to wait till the picker is loaded, can also use the MutationObserver, but this would complicate this code quite a lot
}

function removeAllChildNodes(node) {
    while(node.firstChild) {
        node.removeChild(node.firstChild)
    }
}

function requestWindowClose() {
    var iframe = window.frameElement
    if(iframe !== null) {
        parent.closeChatWindow(iframe)
    }
}

function formatDate(timestamp) {
    var locale = navigator.languages[0]
    if(locale.length === 0){
        locale = 'en-us'
    }
    let date = new Date(timestamp * 1000)
    let dayOfWeek = date.toLocaleString(locale, {  weekday: 'short' })
    let month = date.toLocaleString(locale, {  month: 'short' })
    return `${dayOfWeek}, ${month} ${date.getDate()} | ${date.getHours() < 10 ? "0" : ""}${date.getHours()}:${date.getMinutes() < 10 ? "0" : ""}${date.getMinutes()}`
}

function addMessageBubble(msg) {
    profileImageDiv = document.createElement("div")
    profileImageDiv.classList.add(msg.own_message ? "message-profile-image-own" : "message-profile-image-other")

    profileImage = document.createElement("img")
    profileImage.classList.add("ui", "avatar", "image")
    // profileImage.src = "/media/avatar_default.png"
    profileImage.src = msg.own_message ? own_avatar_image_url : other_avatar_image_url

    profileImageDiv.appendChild(profileImage)


    messageBubble = document.createElement("div")
    messageBubble.classList.add(msg.own_message ? "message-bubble-own" : "message-bubble-other")
    messageBubble.textContent = msg.content


    messageTimestamp = document.createElement("p")
    messageTimestamp.classList.add("message-timestamp")
    messageTimestamp.textContent = formatDate(msg.timestamp)

    message = document.createElement("div")
    message.classList.add("message")

    if(msg.own_message) {
        message.appendChild(messageBubble)
        message.appendChild(profileImageDiv)
        message.appendChild(messageTimestamp)
    } else {
        message.appendChild(profileImageDiv)
        message.appendChild(messageBubble)
        message.appendChild(messageTimestamp)
    }

    // if(chat.lastMessageAuthorSelf === msg.own_message) {
    //     profileImageDiv.style.visibility = "hidden"
    //     messageTimestamp.style.display = "none"
    // }  TODO: should this be done?

    messagesView = document.getElementById("messages-view")
    messagesView.appendChild(message)
    messagesView.scroll(0, messagesView.scrollHeight)

    // messageDiv = document.createElement("div")
    // messageDiv.textContent = msg.source_user_id + ": " + msg.content
    //
    // if(msg.own_message) {
    //     messageDiv.style.color = "blue"
    // }
    //
    // document.getElementById("messages-view").appendChild(messageDiv)

    chat.lastMessageAuthorSelf = msg.own_message
}

function clearAllMessages() {
    removeAllChildNodes(document.getElementById("messages-view"))
}



// ---------------------------
// WebSocket
// ---------------------------

function sendMessage(msg) {
    if(chat.socket !== null) {
        chat.socket.send(JSON.stringify({
            "type": "send_message",
            "content": msg
        }))
    }
}

function requestAllMessages() {
    clearAllMessages()
    chat.lastMessageAuthorSelf = null

    chat.socket.send(JSON.stringify({
        "type": "request_all_messages"
    }))
}

function onOpen(event) {
    console.log("Chat connection established, requesting previous messages...")

    document.getElementById("reconnecting-indicator").style.display = "none"

    requestAllMessages(chat.socket)
}

function onClose(event) {
    console.log(`Chat connection terminated, waiting for reconnect`)

    initiateReconnect()
}

function onError(error) {
    console.log(`Error from websocket ${error.message}`)
}

function initiateReconnect() {
    document.getElementById("reconnecting-indicator").style.display = "inline-block"

    window.setTimeout(() => {
        console.log("Reconnecting to chat...")
        initChat()
    }, 5000)
}

function onMessage(event) {
    // console.log(`Mesage received: ${event.data}`)
    msg = JSON.parse(event.data)

    if(msg.type === "message") {
        addMessageBubble(msg)
    }
}



// ---------------------------
// Init
// ---------------------------

function initChat() {
    console.log("Initializing chat")

    var protocol = "ws:"
    if(window.location.protocol === "https:") {
        protocol = "wss:"
    }

    let socket = new WebSocket(protocol + window.location.host + "/ws/chat/" + chat_slug + "/") // set by django in the html template
    chat.socket = socket
    socket.onopen = (e) => { onOpen(e) }
    socket.onmessage = (e) => { onMessage(e) }
    socket.onclose = (e) => { onClose(e) }
    socket.onerror = (e) => { onError(e) }
}

window.onload = (e) => {
    createEmojiPicker()
    initChat()

    document.getElementById("close-button").onclick = () => {
        requestWindowClose()
    }

    document.getElementById("message-textfield").addEventListener("keydown", (e) => {
        if(e.which === 13) {
            sendMessage(document.getElementById("message-textfield").value)
            document.getElementById("message-textfield").value = ""
        }
    })

    window.addEventListener("mousedown", e => {
        let iframe = window.frameElement;
        if(iframe !== null) {
            parent.hideChatDrawer()
        }
    })
}
