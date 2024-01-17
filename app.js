function drawArt(program, canvas) {
var ctx = canvas.getContext("2d");

// Set the globalAlpha to control transparency (0.0 fully transparent, 1.0 fully opaque)
ctx.globalAlpha = 0.5;

// Draw a half-transparent line
ctx.beginPath();
ctx.moveTo(50, 50);
ctx.lineTo(350, 50);
ctx.lineWidth = 5;
ctx.strokeStyle = "#00F"; // Blue color
ctx.stroke();
};