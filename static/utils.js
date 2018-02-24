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

const showPermission = function() {
    const checkboxArr = document.querySelectorAll('input')
    const spArr = []
    checkboxArr.forEach(function(box, i){
        if (box.checked) {
            spArr.push(String(i))
        }
    })
    const sp = spArr.join('')
    if (sp === '') {
        return 'all'
    } else {
        return sp
    }
}

const scrollTop = function() {
    return window.pageYOffset
        || document.documentElement.scrollTop
        || document.body.scrollTop
        || 0
}
