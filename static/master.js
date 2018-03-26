const errType = function(errs) {
    if (errs.length === 0) {
        return '0'
    } else if (errs[0] === 'Check error') {
        return '5'
    } else {
        const et = ['', '', '', '', '']
        for (let err of errs) {
            et[err[4]] = err[4]
        }
        return et.join('')
    }
}

const prevDeal = function(song, resp) {
    const songStr = song.replace(/([^。])\n/g, '$1\n<br />').replace(/。/g, '。<br />')
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

    const et = errType(resp.err)
    if (resp.err.length === 0) {
        var err = 'Check pass.'
    } else {
        var err = resp.err.join('<br />')
    }
    return [songStr, songPZ, et, err]
}

const controlSong = function(songDiv, status) {
    if (status === 'show') {
        songDiv.classList.value = 'showsong'
    } else {
        songDiv.classList.value = 'showsong hided'
    }
}

const controlSongs = function() {
    const sp = showPermission()
    const songs = document.querySelectorAll('.showsong')
    for (var song of songs) {
        const et = song.dataset.errtype
        if ((sp === 'all') || (sp === et)) {
            controlSong(song, 'show')
        } else {
            controlSong(song, 'hide')
        }
    }
}

const insertSong = function(song, result, showDiv) {
    const [songStr, songPZ, et, err] = prevDeal(song, result)
    const html = `
    <div class="showsong" data-errtype=${et}>
        <div class="song">${songStr}</div>
        <div class="song">${songPZ}</div>
        <div class="err">${err}</div>
    </div>
    `
    showDiv.insertAdjacentHTML('beforeEnd', html)
}

const insertSongs = function(songs, resp) {
    const results = JSON.parse(resp)
    const showDiv = document.querySelector('.showarea')
    showDiv.innerHTML = ''
    songs.forEach((song, i) => insertSong(song, results[i], showDiv))
}

const song_without_title = function(songStr) {
    const re = /[。，]/
    const song = songStr.split('\n').filter(s => re.test(s))
    // log(song)
    return song.join('\n')
}

const query = function() {
    const textarea = document.querySelector('#id-textarea-input')
    const songs_with_title = textarea.value
        .split('\n\n')
        .filter(song => song != '')
    const songs = songs_with_title.map(song_without_title)

    const data = songs.map(function(song){
        return {song: song}
    })
    const dataStr = JSON.stringify(data)
    ajax(
        'POST',
        '/query',
        dataStr,
        resp => insertSongs(songs_with_title, resp)
    )
}

const showYun = function(resp, x, y) {
    const yunArr = JSON.parse(resp)
    const yunStr = yunArr.map(yun => '[' + yun.toString() + ']').join(' ')
    const yunDiv = document.querySelector('.yun')
    yunDiv.innerText = yunStr
    yunDiv.style.left = String(x) + 'px'
    yunDiv.style.top = String(y-35) + 'px'
}

const bindEvent = function() {
    const button = document.querySelector('#id-button-query')
    button.onclick = query

    const selection = document.getSelection()
    window.onmouseup = function(e) {
        const x = e.clientX
        const y = e.clientY + scrollTop()
        const _keyword = selection.getRangeAt(0).toString()
        const keyword = _keyword.replace(/[。， \n\r]/g, '').split('')
        const data = JSON.stringify({keyword: keyword})
        ajax(
            'POST',
            '/yun',
            data,
            resp => showYun(resp, x, y)
        )
    }

    const checkboxArr = document.querySelectorAll('input')
    checkboxArr.forEach(box => box.onchange = controlSongs)
}

const main = function() {
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
