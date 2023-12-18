
const POST_ANALYTICS_UPDATE_PERIOD_MS = 100

let postAnalytics = {
    exposedDurationByPost: new Map(),
    lastUpdateTimestamp: 0
}


// based on https://stackoverflow.com/questions/123999/how-can-i-tell-if-a-dom-element-is-visible-in-the-current-viewport
function isElementInViewport (el) {
    if (typeof jQuery === "function" && el instanceof jQuery) {
        el = el[0]
    }
    let rect = el.getBoundingClientRect();
    return (
        rect.top >= 0 &&
        rect.left >= 0 &&
        rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
        rect.right <= (window.innerWidth || document.documentElement.clientWidth)
    )
}
function isElementCenterInViewport (el) {
    if (typeof jQuery === "function" && el instanceof jQuery) {
        el = el[0]
    }
    let rect = el.getBoundingClientRect();
    let center = {
        x: rect.left + rect.right / 2.0,
        y: rect.top + rect.bottom / 2.0
    }
    return (
        center.y >= 0 &&
        center.x >= 0 &&
        center.y <= (window.innerHeight || document.documentElement.clientHeight) &&
        center.x <= (window.innerWidth || document.documentElement.clientWidth)
    )
}



function updatePostAnalytics() {
    let visiblePosts = []

    document.querySelectorAll(".post-card").forEach(postCard => {
        let id = postCard.querySelector(".post-id-field")
        let content = postCard.querySelector(".post-content")
        let image = postCard.querySelector(".post-image")

        if(isElementInViewport(content) || isElementInViewport(image)) {
            visiblePosts.push(parseInt(id.textContent))
        }
    })

    let timeDelta = new Date().getTime() - postAnalytics.lastUpdateTimestamp
    postAnalytics.lastUpdateTimestamp += timeDelta

    if(document.hasFocus()) {
        visiblePosts.forEach(postId => {
            if(! postAnalytics.exposedDurationByPost.has(postId)) {
                postAnalytics.exposedDurationByPost.set(postId, 0)
            }

            postAnalytics.exposedDurationByPost.set(postId, postAnalytics.exposedDurationByPost.get(postId) + timeDelta)
        })
    }

    // console.log(postAnalytics.exposedDurationByPost)

    setTimeout(() => updatePostAnalytics(), POST_ANALYTICS_UPDATE_PERIOD_MS)
}

function getAndClearPostAnalytics() {
    let res = new Map(postAnalytics.exposedDurationByPost)
    postAnalytics.exposedDurationByPost.clear()
    return res
}

function initPostAnalytics() {
    postAnalytics.lastUpdateTimestamp = new Date().getTime() + 2000
    setTimeout(() => updatePostAnalytics(), 2000)
}

$(document).ready(() => {
    initPostAnalytics()
})