var chatManager = {
    chatWindows: [],
    chatDrawer: null
}

const SESSION_STORAGE_KEY = "chat-manager-open-conversations"

const CHAT_WINDOW_WIDTH = 300
const CHAT_WINDOW_HEIGHT = 350
const CHAT_WINDOW_SPACING = 30
const CHAT_WINDOWS_MARGIN_RIGHT = 20

const CHAT_DRAWER_WINDOW_WIDTH = 350
const CHAT_DRAWER_WINDOW_HEIGHT = 510
const CHAT_DRAWER_Y_OFFSET = 40

// <div style="left: 0px; border: 0px none; height: 370px; position: fixed; width: 270px; overflow: hidden; bottom: -67px;">
//     <div style="overflow: hidden;">
//     </div>
//     <iframe src="http://weather.gc.ca/wxlink/wxlink.html?cityCode=on-162&amp;lang=e" scrolling="no" style="height: 300px; border: 0px none; width: 165px; margin-bottom: 0px; margin-left: 24px;">
//     </iframe>
// </div>
// </div>


function createChatIframe(otherUserId) {
    let container = document.createElement("div");
    container.style.right = `${CHAT_WINDOWS_MARGIN_RIGHT}px`
    container.style.bottom = "0px"
    container.style.border = "0px none"
    container.style.width = `${CHAT_WINDOW_WIDTH}px`
    container.style.height = `${CHAT_WINDOW_HEIGHT}px`
    container.style.position = "fixed"
    container.style.overflowX = "hidden"
    container.style.overflowY = "hidden"

    container.style.backgroundColor = "rgb(240, 242, 245)"

    let iframe = document.createElement("iframe");
    iframe.setAttribute("src", `${window.location.origin}/chat/?profile_pk=${otherUserId}`)
    iframe.style.width = "100%"
    iframe.style.height = "100%"
    iframe.style.overflow = "hidden"
    iframe.style.border = "0"  // iframe.frameBorder is deprecated, use this instead

    iframe.onload = () => {
        iframe.contentWindow.iframeContainerDiv = container // set reference for child iframe to use for aligning the emoji picker
    }

    container.appendChild(iframe)
    document.body.appendChild(container)


    chatManager.chatWindows.push({
        iframe: iframe,
        container: container,
        otherUserId: otherUserId
    })

    updateSessionStorage()
    alignChatWindows()
}

function closeChatWindow(iframe) {
    let chatWindow = chatManager.chatWindows.find((w) => w.iframe === iframe)
    if(chatWindow !== undefined) {
        chatWindow.container.removeChild(chatWindow.iframe)
        document.body.removeChild(chatWindow.container)

        chatManager.chatWindows.splice(chatManager.chatWindows.indexOf(chatWindow), 1)
        updateSessionStorage()
        alignChatWindows()
    }
}

function alignChatWindows() {
    for(var i = 0;i < chatManager.chatWindows.length;i++) {
        var window = chatManager.chatWindows[i]

        var rightOffset = CHAT_WINDOWS_MARGIN_RIGHT + i * (CHAT_WINDOW_WIDTH + CHAT_WINDOW_SPACING)

        window.container.style.right = `${rightOffset}px`
    }
}

function updateSessionStorage() {
    sessionStorage.setItem(SESSION_STORAGE_KEY, JSON.stringify(chatManager.chatWindows.map((it) => it.otherUserId)))
}

function loadSessionStorage() {
    let item = sessionStorage.getItem(SESSION_STORAGE_KEY)
    if(item != null) {
        console.log("Reopening chat windows")
        JSON.parse(item).forEach((otherUserId) => createChatIframe(otherUserId))
    } else {
        console.log("No chat session storage found, no windows restored")
    }
}

function createDrawerIframe() {
    let container = document.createElement("div");
    container.style.top = "100px"
    container.style.left = "10px"
    container.style.border = "0px none"
    container.style.width = `${CHAT_DRAWER_WINDOW_WIDTH}px`
    container.style.height = `${CHAT_DRAWER_WINDOW_HEIGHT}px`
    container.style.position = "fixed"
    container.style.overflowX = "hidden"
    container.style.overflowY = "hidden"

    container.style.display = "none"
    container.style.backgroundColor = "rgb(240, 242, 245)"

    let iframe = document.createElement("iframe");
    iframe.setAttribute("src", `${window.location.origin}/chat/drawer`)
    iframe.style.width = "100%"
    iframe.style.height = "100%"
    iframe.style.overflow = "hidden"
    iframe.style.border = "0"  // iframe.frameBorder is deprecated, use this instead

    container.appendChild(iframe)
    document.body.appendChild(container)

    chatManager.chatDrawer = {
        iframe: iframe,
        container: container,
    }
}

function chatWithUserRequested(otherUserId) {
    if (! chatManager.chatWindows.some(w => w.otherUserId == otherUserId)) {
        createChatIframe(otherUserId)
    }
    hideChatDrawer()
}

function toggleChatDrawer(posX, posY) { // TODO: currently this uses the position of the mouse event, use the button position instead
    let container = chatManager.chatDrawer.container;

    if(container.style.display === "none") {
        showChatDrawer(posX, posY)
    } else {
        hideChatDrawer()
    }
}

function showChatDrawer(posX, posY) {
    let container = chatManager.chatDrawer.container;
    let toggleIcon = document.querySelector(".fa-facebook-messenger")

    container.style.left = `${posX - CHAT_DRAWER_WINDOW_WIDTH / 2}px`
    container.style.top = `${posY + CHAT_DRAWER_Y_OFFSET}px`

    container.style.display = "block"
    if(toggleIcon != null) {
        toggleIcon.parentNode.classList.add("active")
    }
}

function hideChatDrawer() {
    let container = chatManager.chatDrawer.container;
    let toggleIcon = document.querySelector(".fa-facebook-messenger")

    container.style.display = "none"
    if(toggleIcon != null) {
        toggleIcon.parentNode.classList.remove("active")
    }
}

$(document).ready(() => {

    if(typeof DISABLE_CHAT_MANAGER !== 'undefined' && DISABLE_CHAT_MANAGER === true) {
        console.log("Variable set, disabling chat manager...")
        return
    }

    console.log("Chat manager intialized")

    loadSessionStorage()

    createDrawerIframe()
    window.addEventListener("mousedown", e => hideChatDrawer())
})