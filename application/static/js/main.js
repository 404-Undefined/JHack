$(document).ready(function () {
  $(window).scroll(function () {
    if ($(window).scrollTop() >= 20) {
      $(".navbar").css("background-color", "#222");
    } else {
      $(".navbar").css("background-color", "transparent");
    }
  });
});
// WYSIWYG editor
CKEDITOR.replace("editor1");
CKEDITOR.replace("editor2");

function add() {
  event.preventDefault();
  if ($("#total_chq").val() < 4) {
    var index = parseInt($("#total_chq").val()) + 1;
    $("#member_" + index).show();
    $("#total_chq").val(index);
  }
}
function remove() {
  event.preventDefault();
  var last_no = $("#total_chq").val();
  if (last_no > 1) {
    $("#member_" + last_no).hide();
    $("#total_chq").val(last_no - 1);
  }
}

let x = 0.01;
let y = 0;
let z = 0;

let a = 10;
let b = 28;
let c = 8.0 / 3.0;

let angleX = 0;
let angleY = 0;
let angleZ = 0;

let points = new Array();

function setup() {
  var clientHeight = document.getElementById("portal_header").clientHeight;
  var clientWidth = document.getElementById("portal_header").clientWidth;

  var cnv = createCanvas(clientWidth, clientHeight, WEBGL);
  cnv.parent("portal_header");

  colorMode(RGB, 255, 255, 255, 1);
}

function draw() {
  background(0);

  let dt = 0.01;
  let dx = a * (y - x) * dt;
  let dy = (x * (b - z) - y) * dt;
  let dz = (x * y - c * z) * dt;
  x = x + dx;
  y = y + dy;
  z = z + dz;

  points.push(new p5.Vector(x, y, z));

  translate(0, 0, 200);
  let camX = map(mouseX, 0, width, -400, 400);
  let camY = map(mouseY, 0, height, -400, 400);

  rotateY(angleX);
  rotateX(angleY);
  rotateZ(angleZ);
  angleX += 0.01;
  angleY += 0.005;
  angleZ += 0.005;

  //camera(camX, camY, height / 2.0 / tan((PI * 30.0) / 180.0), 0, 0, 0, 0, 1, 0);

  scale(3);
  stroke(255);
  noFill();
  strokeWeight(2);

  let hu = 0;
  beginShape();

  for (let v of points) {
    stroke(hu, 255, 255);
    vertex(v.x, v.y, v.z);
    hu += 1;
    if (hu > 255) {
      hu = 0;
    }
  }
  endShape();

  //println(x,y,z);
}

// function add(){
//   if($('#total_chq').val() < 4){
//     var new_chq_no = parseInt($('#total_chq').val())+1;
//     var new_input='<div class="form-field" id="input-container' + new_chq_no + '""><div class="form-group"><input type="text" name="firstname' + new_chq_no + '" class="form-control"></div><div class="form-group"><input type="text" name="lastname ' + new_chq_no + '" class="form-control"></div></div>'
//     $('#member_container').append(new_input);
//     $('#total_chq').val(new_chq_no)
//   }
// }
// function remove(){
//   var last_chq_no = $('#total_chq').val();
//   if(last_chq_no>1){
//     $('#input-container'+last_chq_no).remove();
//     $('#total_chq').val(last_chq_no-1);
//   }
// }
