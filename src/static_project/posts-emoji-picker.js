
postsEmojiPicker = {
    visible: false,
    container: null,
    inputFieldTarget: null
}

const CREATE_POST_EMOJI_PICKER_HEIGHT_OFFSET = 40

function togglePostsEmojiPickerVisibility(x, y) {
    console.log("Toggeling post emoji picker")

    if(postsEmojiPicker.container == null) {
        console.log("Emoji picker not yet created, aborting toggle")
        return
    }

    if(postsEmojiPicker.visible) {
        postsEmojiPicker.visible = false

        postsEmojiPicker.container.style.display = "none"
    } else {
        postsEmojiPicker.visible = true
        postsEmojiPicker.container.style.display = "block"

        postsEmojiPicker.container.style.left = `${x - (postsEmojiPicker.container.getBoundingClientRect().width / 2)}px`
        postsEmojiPicker.container.style.top = `${y + CREATE_POST_EMOJI_PICKER_HEIGHT_OFFSET}px`
    }

    console.log("Emoji picker now visibility: " + postsEmojiPicker.visible)
}

function hidePostsEmojiPicker() {
    if(postsEmojiPicker.visible) {
        togglePostsEmojiPickerVisibility(0, 0)
    }
}

function createPostsEmojiPicker() {
    console.log("Creating posts emoji picker")

    let postContentTextfield = document.getElementById("id_content")

    let pickerContainer = document.createElement("div")
    let picker = document.createElement("emoji-picker")
    pickerContainer.appendChild(picker)

    postsEmojiPicker.container = pickerContainer

    window.addEventListener("mousedown", e => {
        // hidePostsEmojiPicker()
        //TODO, alternatively do via message field
    })

    let toggleButton = document.getElementById("reaction-drawer-button-create-post")
    toggleButton.addEventListener("mousedown", e => {
        togglePostsEmojiPickerVisibility(e.clientX, e.clientY)
        postsEmojiPicker.inputFieldTarget = postContentTextfield
        e.preventDefault()
    })

    let commentToggleButtons = document.querySelectorAll(".reaction-drawer-button-create-comment")
    commentToggleButtons.forEach((toggleButton) => {
        toggleButton.addEventListener("mousedown", e => {
            let inputField = toggleButton.parentElement.parentElement.querySelector("#id_body")
            togglePostsEmojiPickerVisibility(e.clientX, e.clientY)
            postsEmojiPicker.inputFieldTarget = inputField
            e.preventDefault()
        })
    })

    picker.addEventListener("emoji-click", e => {
        togglePostsEmojiPickerVisibility(0, 0)
        postsEmojiPicker.inputFieldTarget.value += e.detail.unicode
    })

    window.setTimeout(() => {
        picker.classList.add("light")

        pickerContainer.style.display = "none"
        parent.document.body.appendChild(pickerContainer)

        pickerContainer.style.position = "fixed"

    }, 1000)
}

$(document).ready(() => {
    createPostsEmojiPicker()
})