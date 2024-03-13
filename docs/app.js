function polar_x_function(midx, r, number_of_nails) {
    return function (x){return midx + r*Math.cos(2*Math.PI*(x/number_of_nails))}
}

function polar_y_function(midy, r, number_of_nails) {
    return function (x){return midy + r*Math.sin(2*Math.PI*(x/number_of_nails))}
}

function drawArt(program, speed, canvas) {
    //make canvas a square
    const side_length = Math.min(canvas.width, canvas.height);
    canvas.width = 2000;
    canvas.height = 2000;
    var ctx = canvas.getContext("2d");
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    // Set the globalAlpha to control transparency (0.0 fully transparent, 1.0 fully opaque)
    ctx.globalAlpha = 0.2;
    const radius = 0.47*Math.min(canvas.height, canvas.width);
    const midx = canvas.width / 2;
    const midy = canvas.height / 2;


    const instructions = program.split("\n");
    const number_of_nails = Number(instructions[0]);

    x_coord = polar_x_function(midx, radius, number_of_nails);
    y_coord = polar_y_function(midy, radius, number_of_nails);

    for (var i = 1; i<instructions.length;i++){
        setTimeout((nails) => {
            if (Number(nails[0])>number_of_nails || Number(nails[1])>number_of_nails){
                console.error("Too big number of nails");
            }
            ctx.beginPath();
            ctx.moveTo(x_coord(Number(nails[0])), y_coord(Number(nails[0])));
            ctx.lineTo(x_coord(Number(nails[1])), y_coord(Number(nails[1])));
            ctx.lineWidth = 2;
            ctx.closePath();
            ctx.stroke();
        }, speed*1000*i, instructions[i].split(/\s+/));
    }
};
