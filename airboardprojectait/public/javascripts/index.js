function _(selector){
    return document.querySelector(selector);
}

function setup(){
    let canvas = createCanvas(650,600);
    canvas.parent("#canvas-wrapper");
    background(255);
}

function mouseDragged(){
    let type= "pencil";
    let size = parseInt(_("#pen-size").value);
    let color= _("#pen-color").value;
    fill(color);
    stroke(color);
    if(type == "pencil"){
        strokeWeight(size)
        line(pmouseX=0,pmouseY=0,mouseX=10,mouseY=10);
    }
}

_("#reset-canvas").addEventListener("click",
function(){
    background(255);
});

_("#save-canvas").addEventListener("click",
function(){
    saveCanvas(canvas,"sketch","png");
});

