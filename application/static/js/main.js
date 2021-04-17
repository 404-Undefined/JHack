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

// CKEDITOR.instances["editor2"].insertHtml("<h2>What does your project do?</h2><h2>What tools/programming languages did you use?</h2><h2>Challenges that you faced</h2><h2>Optional improvements/extensions to your project</h2>");
CKEDITOR.instances["editor2"].setData("What does your project do?  What tools/programming languages did you use? What Challenges did you face?  What are some optional improvements/extensions to your project?")



// function add() {
//   event.preventDefault();
//   if ($("#total_chq").val() < 4) {
//     var index = parseInt($("#total_chq").val()) + 1;
//     $("#member_" + index).show();
//     $("#total_chq").val(index);
//   }
// }
// function remove() {
//   event.preventDefault();
//   var last_no = $("#total_chq").val();
//   if (last_no > 1) {
//     $("#member_" + last_no).hide();
//     $("#total_chq").val(last_no - 1);
//   }
// }

let x = 0.01;
let y = 0;
let z = 0;

let a = 10;
let b = 28;
let c = 8.0 / 3.0;

let n = 0;

let angleX = 0;
let angleY = 0;
let angleZ = 0;

let points = new Array();

function setup() {
  var clientHeight = document.getElementById("portal_h").clientHeight;
  var clientWidth = document.getElementById("portal_h").clientWidth;

  var c = createCanvas(clientWidth, clientHeight);

  var clientHeight = document.getElementById("portal_header").clientHeight;
  var clientWidth = document.getElementById("portal_header").clientWidth;

  var cnv = createCanvas(clientWidth, clientHeight, WEBGL);
  cnv.parent("portal_header");

  colorMode(RGB, 255, 255, 255, 1);
}

function draw() {
  background(0);
  n++;
  if (n < 3000) {
    let dt = 0.01;
    let dx = a * (y - x) * dt;
    let dy = (x * (b - z) - y) * dt;
    let dz = (x * y - c * z) * dt;
    x = x + dx;
    y = y + dy;
    z = z + dz;
  }
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
}

$(".navbar-toggler").click(function () {
  $("nav").toggleClass("bg-dark");
});

// $(".main").css("padding-top", "50px"):