function polar_x_function(midx, r, number_of_nails) {
    return function (x){return midx + r*Math.cos(2*Math.PI*(x/number_of_nails))}
}

function polar_y_function(midy, r, number_of_nails) {
    return function (x){return midy + r*Math.sin(2*Math.PI*(x/number_of_nails))}
}

function drawArt(program, speed, canvas) {   
    // remove possible remainders
    context.clearRect(0, 0, canvas.width, canvas.height);
    //make canvas a square
    const side_length = Math.min(canvas.width, canvas.height);
    canvas.width = side_length;
    canvas.height = side_length;
    var ctx = canvas.getContext("2d");
    ctx.canvas.width = 10*side_length;
    ctx.canvas.height = 10*side_length;
    // Set the globalAlpha to control transparency (0.0 fully transparent, 1.0 fully opaque)
    ctx.globalAlpha = 0.2;
    const radius = 0.4*Math.min(canvas.height, canvas.width);
    const midx = canvas.width / 2;
    const midy = canvas.height / 2;


    const instructions = program.split("\n");
    const number_of_nails = Number(instructions[0]);

    x_coord = polar_x_function(midx, radius, number_of_nails);
    y_coord = polar_y_function(midy, radius, number_of_nails);

    for (var thread of instructions.slice(1)){
        var nails = thread.split(/\s+/);
        if (Number(nails[0])>number_of_nails || Number(nails[1])>number_of_nails){
            console.error("Too big number of nails");
        }
        ctx.beginPath();
        ctx.moveTo(x_coord(Number(nails[0])), y_coord(Number(nails[0])));
        ctx.lineTo(x_coord(Number(nails[1])), y_coord(Number(nails[1])));
        ctx.lineWidth = 2;
        ctx.closePath();
        ctx.stroke();
        //await setTimeout(parseFloat(speed));
    }
};