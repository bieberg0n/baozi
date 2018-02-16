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

const prevDeal = function(song, resp) {
    const songStr = song.replace(/。/g, '。<br />')
    // log('tailYuns,', resp, resp['tail_yuns'], resp.tail_yuns)
    const tailYunsRev = resp.tail_yuns.reverse()
    const songPZArr = resp.song_pz

    var songPZ = []
    for (let i in songPZArr) {
        songPZ.push(songPZArr[i])
        if (i % 2 === 0) {
            songPZ.push('，')
        } else {
            songPZ.push('。')
            songPZ.push('（' + String(tailYunsRev.pop()) + '）')
            songPZ.push('<br />')
        }
    }
    songPZ = songPZ.join('')

    if (resp.err.length === 0) {
        var err = 'Check pass.'
    } else {
        var err = resp.err.join('<br />')
    }
    // log(songStr)
    // log(songPZ)
    // log(resp.err)
    return [songStr, songPZ, err]
}

const insertText = function(song, resp) {
    const res = JSON.parse(resp)
    // log('resp,', res)
    const [songStr, songPZ, err] = prevDeal(song, res)
    // log(songStr)
    // log(songPZ)
    // log(err)
    const show = document.querySelector('.show')
    show.innerHTML = ''
    const html = `
        <div class="song">${songStr}</div>
        <div class="song">${songPZ}</div>
        <div class="err">${err}</div>
        `
    show.insertAdjacentHTML('beforeEnd', html)
}

const query = function() {
    const textarea = document.querySelector('#id-textarea-input')
    const song = textarea.value
    const data = JSON.stringify({song: song})
    ajax(
        'POST',
        '/query',
        data,
        resp => insertText(song, resp)
    )
}

const bindEvent = function() {
    const button = document.querySelector('#id-button-query')
    button.onclick = query
}

const main = function() {
    log('hello')
    bindEvent()

    // const song = '床前明月光，疑是地上霜。举头望明月，低头思故乡。'
    // const resp = {
    //     song_pz: ['平平平仄平', '平仄仄仄平', '仄平中平仄', '平平中仄平'],
    //     tail_yuns: [['七阳平声'], ['七阳平声']],
    //     err: [
    //         'rule1 error: 句内 偶数字（2、4、6）之间平仄未相反. line 2',
    //         'rule1 error: 句内 偶数字（2、4、6）之间平仄未相反. line 3',
    //         'rule2-1 error: 同一联的出句和对句，偶数字平仄未相反. line 1',
    //         'rule2-2 error: 每联间的对句和出句，偶数字平仄不相同. line 2',
    //         'rule2-1 error: 同一联的出句和对句，偶数字平仄未相反. line 3'
    //     ],
    // }
    // insertText(song, resp)
}

main()
