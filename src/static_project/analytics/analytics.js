
analytics = {
    connected: false,
    socket: null,
    updatePeriod: 2000,
    unauthorized: false
}

function updateThread() {
    if(analytics.connected && analytics.socket !== null) {
        // get and send post analytics
        let postExposureDurationsMap = getAndClearPostAnalytics()
        let postExposureDurations = Array.from(postExposureDurationsMap.entries()).map(d => { return {"postId": d[0], "duration": d[1]} })

        analytics.socket.send(JSON.stringify({
            type: "heartbeat",
            postExposures: postExposureDurations
        }))
    }

    setTimeout(() => updateThread(), analytics.updatePeriod)
}


function onOpen(event) {
    console.log("Analytics: Connection established, waiting for configuration...")
    analytics.connected = true
}

function onMessage(event) {
    msg = JSON.parse(event.data)

    if(msg.type === "config") {
        analytics.updatePeriod = msg.updatePeriod
        console.log(`Analytics: Received configuration, update period is ${analytics.updatePeriod} ms`)
    } else if(msg.type === "status") {
        console.log(`Analytics: received status: ${msg.status}, message: ${msg.message}`)
        if(msg.status === "unauthorized") {
            console.log("Not logged in, quitting analytics module.")
            analytics.unauthorized = true
        }
    }
}

function onClose(event) {
    console.log(`Analytics: Connection terminated, waiting for reconnect`)
    analytics.connected = false

    initiateReconnect()
}

function onError(event) {
    console.log(`Error from websocket ${error.message}`)
}

function initiateReconnect() {
    if(analytics.unauthorized) {
        console.log("Aborting reconnected.")
        return
    }

    window.setTimeout(() => {
        console.log("Reconnecting to analytics service...")
        initAnalyticsConnection()
    }, 5000)
}


function initAnalyticsConnection() {
    console.log("Analytics: initializing module")

    var protocol = "ws:"
    if(window.location.protocol === "https:") {
        protocol = "wss:"
    }

    let socket = new WebSocket(protocol + window.location.host + "/ws/analytics/")
    analytics.socket = socket
    socket.onopen = (e) => { onOpen(e) }
    socket.onmessage = (e) => { onMessage(e) }
    socket.onclose = (e) => { onClose(e) }
    socket.onerror = (e) => { onError(e) }
}


$(document).ready(() => {
    initAnalyticsConnection()
    updateThread()
})