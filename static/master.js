const log = function() {
    console.log(...arguments)
}

const ajax = function(method, path, data, reseponseCallback) {
    var r = new XMLHttpRequest()
    // 设置请求方法和请求地址
    r.open(method, path, true)
    // 设置发送的数据的格式
    r.setRequestHeader('Content-Type', 'application/json')
    // 注册响应函数
    r.onreadystatechange = function() {
        if(r.readyState === 4) {
            reseponseCallback(r.response)
        }
    }
    // 发送请求
    r.send(data)
}

const insertText = function(text) {
    const show = document.querySelector('.show')
    show.innerText = text
}

const query = function() {
    const textarea = document.querySelector('#id-textarea-input')
    const song = textarea.value
    const data = JSON.stringify({song: song})
    ajax(
        'POST',
        '/query',
        data,
        insertText
    )
}

const bindEvent = function() {
    const button = document.querySelector('#id-button-query')
    button.onclick = query
}

const main = function() {
    log('hello')
    bindEvent()
}

main()
