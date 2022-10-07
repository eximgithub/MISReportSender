function $(message_template, params) {
    console.log("Begin javascript build message function ")
    console.log(params)
    var result = message_template
    for (let i = 0; i < params.length; i++) {
        var row = params[i]
        result = result.replace('{param0}', row[0]).replace('{param1}', row[1]).replace('{param2}', row[2]);
    }
    console.log("End javascript build message function ")
    return result
}