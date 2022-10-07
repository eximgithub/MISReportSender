function $(message_template, params) {
    console.log("Begin javascript build message function ")
    console.log(params)
    var result = message_template
    for (let i = 0; i < params.length; i++) {
        var row = params[i]
        result =
        result
        .replace('{header}', 'NGÀY BÁO CÁO')
        .replace('{ngaybaocao}', row[0])
        .replace('{tongtaisan}', row[1])
        .replace('{tongtaisan_kh}', row[2]
        );
    }
    console.log("End javascript build message function ")
    return result
}