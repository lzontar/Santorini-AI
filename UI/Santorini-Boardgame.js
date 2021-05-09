const rectSide = 120;
const buildingWidth = rectSide / 3;
const buildingHeight = rectSide / 4;

const xStart = - rectSide * 2;
const yStart = - rectSide * 2;
const widthViewBox = 4 * rectSide;
const heightViewBox = 4 * rectSide;
const width = 4 * rectSide;
const height = 4 * rectSide;
const viewBox = xStart + " " + yStart + " " + width + " " + height;

const svgns = "http://www.w3.org/2000/svg";

boardState = initialState();

player1Pos = [[0, 1], [2, 2]]
player2Pos = [[2, 1], [3, 3]]

console.log(boardState)


function drawCanvas() {
    var canvas = document.getElementById("canvas");
    canvas.setAttribute("viewBox", viewBox);
    canvas.setAttribute("width", widthViewBox);
    canvas.setAttribute("height", heightViewBox);


    yStartRect = yStart
    for (let i = 0; i < boardState.length; i++) {
        xStartRect = xStart
        for (let j = 0; j < boardState[i].length; j++) {
            var rect = document.createElementNS(svgns, 'rect');
            rect.setAttributeNS(null, 'x', xStartRect);
            rect.setAttributeNS(null, 'y', yStartRect);
            rect.setAttributeNS(null, 'height', rectSide);
            rect.setAttributeNS(null, 'width', rectSide);
            rect.setAttributeNS(null, 'style', "stroke-width:3;stroke:#FFFBE6;fill:#6B9855;");
            rect.setAttributeNS(null, 'ixX', i);
            rect.setAttributeNS(null, 'ixY', j);

            rect.addEventListener('click',
                function() {


                    var xmlHttp = new XMLHttpRequest();
                    xmlHttp.open( "GET", 'http://127.0.0.1:8000/api/', false ); // false for synchronous request
                    xmlHttp.send( null );
                    xmlHttp.responseText;
                    console.log(xmlHttp)
                    console.log(this.getAttribute('ixX'), this.getAttribute('ixY'))
                }, false);

            canvas.appendChild(rect);

            if (boardState[i][j] > 0) {
                for (let k = 0; k < Math.min(boardState[i][j], 3); k++) {
                    var rectLevel = document.createElementNS(svgns, 'rect');

                    rectLevel.setAttributeNS(null, 'x', xStartRect + buildingWidth);
                    rectLevel.setAttributeNS(null, 'y', yStartRect - 1.5 + (3 - k) * buildingHeight);
                    rectLevel.setAttributeNS(null, 'height', buildingHeight);
                    rectLevel.setAttributeNS(null, 'width', buildingWidth);
                    rectLevel.setAttributeNS(null, 'style', "stroke-width:1;stroke:#74564C;fill:#FFFBE6;");

                    canvas.appendChild(rectLevel);
                }
            }

            if (boardState[i][j] == 4) {
                var circle = document.createElementNS(svgns, 'circle');

                circle.setAttributeNS(null, 'cx', xStartRect + (3 / 2) * buildingWidth);
                circle.setAttributeNS(null, 'cy', yStartRect + buildingHeight - 5);
                circle.setAttributeNS(null, 'r', 10);
                circle.setAttributeNS(null, 'style', 'stroke: #2C397D; stroke-width: 1px; fill:#2C397D;' );

                canvas.appendChild(circle);
            }
            xStartRect += rectSide
        }
        yStartRect += rectSide
    }

    var player11 = document.createElementNS(svgns, 'circle');

    player11.setAttributeNS(null, 'cx', xStart + (player1Pos[0][0] + 1 / 2) * rectSide);
    player11.setAttributeNS(null, 'cy', yStart + (player1Pos[0][1] + 1 / 2) * rectSide);
    player11.setAttributeNS(null, 'r', 20);
    player11.setAttributeNS(null, 'style', "fill:rgba(222, 146, 168, 0.7);stroke:#98556b;stroke-width:3");

    canvas.appendChild(player11);

    var player12 = document.createElementNS(svgns, 'circle');

    player12.setAttributeNS(null, 'cx', xStart + (player1Pos[1][0] + 1 / 2) * rectSide);
    player12.setAttributeNS(null, 'cy', yStart + (player1Pos[1][1] + 1 / 2) * rectSide);
    player12.setAttributeNS(null, 'r', 20);
    player12.setAttributeNS(null, 'style', "fill:rgba(222, 146, 168, 0.7);stroke:#98556b;stroke-width:3");

    canvas.appendChild(player12);

    var player21 = document.createElementNS(svgns, 'circle');

    player21.setAttributeNS(null, 'cx', xStart + (player2Pos[0][0] + 1 / 2) * rectSide);
    player21.setAttributeNS(null, 'cy', yStart + (player2Pos[0][1] + 1 / 2) * rectSide);
    player21.setAttributeNS(null, 'r', 20);
    player21.setAttributeNS(null, 'style', "fill:rgba(194, 229, 255, 0.7);stroke:#558198;stroke-width:3");

    canvas.appendChild(player21);

    var player22 = document.createElementNS(svgns, 'circle');

    player22.setAttributeNS(null, 'cx', xStart + (player2Pos[1][0] + 1 / 2) * rectSide);
    player22.setAttributeNS(null, 'cy', yStart + (player2Pos[1][1] + 1 / 2) * rectSide);
    player22.setAttributeNS(null, 'r', 20);
    player22.setAttributeNS(null, 'style', "fill:rgba(194, 229, 255, 0.7);stroke:#558198;stroke-width:3");

    canvas.appendChild(player22);

}

function initialState() {
    return [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [4, 1, 2, 3]
    ]
}

function refreshGame() {
    boardState = initialState();
    drawCanvas();
}










































// const xStart = -400;
// const yStart = -350;
// const widthViewBox = 1000;
// const heightViewBox = 700;
// const width = 1000;
// const height = 700;
// const viewBox = xStart + " " + yStart + " " + width + " " + height;
// const awayFromCenter = height/3.5
// const radiusCommander = height/30;
// const radiusMessage = height/50;
//
// var sendingDuration; // in seconds
// var changedSpeed = false;
//
// const svgns = "http://www.w3.org/2000/svg";
//
// var lieutenants = [];
// var lieutenantsValues = [];
// var general = null;
// var traitors = [];
// var zvestiTrenutno;
//
// var numberOfTraitors = 1;
//
// var animationIsActive = false;
// var animationIsPaused = false;
//
// var messages = [];
// var travelingMessages = 0;
//
// function drawCanvas() {
//     if(document.getElementById("result"))
//         document.getElementById("result").innerHTML = "";
//
//     var canvas = document.getElementById("canvas");
//     canvas.setAttribute("viewBox", viewBox);
//     canvas.setAttribute("width", widthViewBox);
//     canvas.setAttribute("height", heightViewBox);
//
//     // General circle info
//     const xGeneral = 0;
//     const yGeneral = -awayFromCenter;
//     const idGeneral = 'G';
//     general = {x: xGeneral, y: yGeneral, elHtml: null, id:idGeneral}
//
//     zvestiTrenutno = ['G', 'L1', 'L2', 'L3', 'L4'];
//     document.getElementById("zvesti").innerHTML = "G, L1, L2, L3, L4";
//     document.getElementById("izdajalci").innerHTML = "";
//
//     traitors = [];
//     lieutenants = [];
//     lieutenantsValues = [];
//     // Lieutenant circles info
//     lieutenants.push({x: Math.cos(Math.PI/2 - 3 * Math.PI/5)*awayFromCenter, y: Math.sin(Math.PI/2 - 3 * Math.PI/5)*awayFromCenter, elHtml: null, id:"L1"});
//     lieutenants.push({x: Math.cos(Math.PI/2 - Math.PI/5)*awayFromCenter, y: Math.sin(Math.PI/2 - Math.PI/5)*awayFromCenter, elHtml: null, id:"L2"});
//     lieutenants.push({x: -Math.cos(Math.PI/2 - Math.PI/5)*awayFromCenter, y: Math.sin(Math.PI/2 - Math.PI/5)*awayFromCenter, elHtml: null, id:"L3"});
//     lieutenants.push({x: -Math.cos(Math.PI/2 - 3 * Math.PI/5)*awayFromCenter, y: Math.sin(Math.PI/2 - 3 * Math.PI/5)*awayFromCenter, elHtml: null, id:"L4"});
//
//     // Draw polygon background
//     var polygonPoints = xGeneral + "," + yGeneral;
//     lieutenants.forEach(lieutenant => {
//         polygonPoints += " " + lieutenant.x + "," + lieutenant.y;
//     });
//     var polygon = document.createElementNS(svgns, 'polygon');
//     polygon.setAttributeNS(null, 'points', polygonPoints);
//     polygon.setAttributeNS(null, 'style', "fill:rgba(217, 217, 217, 0.8);");
//     canvas.appendChild(polygon);
//
//     //Draw general's circle
//     general.elHtml = addCommander(canvas, xGeneral, yGeneral, idGeneral);
//
//     // var crown = document.createElementNS(svgns, 'image');
//     // crown.setAttributeNS(null, 'x', xGeneral - 10);
//     // crown.setAttributeNS(null, 'y', yGeneral - 40);
//     // crown.setAttributeNS(null, 'width', 20);
//     // crown.setAttributeNS(null, 'height', 20);
//     // crown.setAttributeNS('http://www.w3.org/1999/xlink', 'href', './libs/fontawesome-free-5.13.0-web/svgs/solid/crown.svg');
//
//     // canvas.appendChild(crown);
//
//     //Draw lieutenant circles
//     lieutenants.forEach(lieutenant => lieutenant.elHtml = addCommander(canvas, lieutenant.x, lieutenant.y, lieutenant.id));
//
//     // Add listener to change traitors
//     document.querySelectorAll(".commander").forEach(x => x.addEventListener('click', toggleTraitor));
//
//     // Set number of traitors on init
//     numberOfTraitors = document.getElementById("nTraitors").value;
//
//     var castle = document.createElementNS(svgns, 'image');
//     castle.setAttributeNS(null, 'x', -50);
//     castle.setAttributeNS(null, 'y', -70);
//     castle.setAttributeNS(null, 'width', 100);
//     castle.setAttributeNS(null, 'height', 100);
//     castle.setAttributeNS('http://www.w3.org/1999/xlink', 'href', './libs/fontawesome-free-5.13.0-web/svgs/brands/fort-awesome.svg');
//
//     canvas.appendChild(castle)
//
//     drawLegend();
// }
//
// function drawLegend() {
//     var canvas = document.getElementById("canvas");
//
//     var extraMargin = width/100;
//
//     var initX = width/2 - width/5 + extraMargin;
//     var initY = -height/2 + radiusCommander + extraMargin;
//
//     var legendTitle = document.createElementNS(svgns, 'text');
//
//     legendTitle.setAttributeNS(null, 'x', initX - extraMargin);
//     legendTitle.setAttributeNS(null, 'y', initY + 1.5 * extraMargin);
//     legendTitle.setAttributeNS(null, 'style', "fill:rgba(30, 30, 30,0.8); font-size: 20px; font-weight: bold;");
//     legendTitle.addEventListener('click', toggleTraitor);
//     legendTitle.innerHTML = "Legenda";
//
//     canvas.appendChild(legendTitle);
//
//     initY += 5 * extraMargin;
//
//     // Loyal commander legend
//     var circleCommanderLoyal = document.createElementNS(svgns, 'circle');
//
//     circleCommanderLoyal.setAttributeNS(null, 'cx', initX + extraMargin);
//     circleCommanderLoyal.setAttributeNS(null, 'cy', initY + extraMargin);
//     circleCommanderLoyal.setAttributeNS(null, 'r', radiusCommander);
//     circleCommanderLoyal.setAttributeNS(null, 'style', "fill:rgba(1,163,217,0.8);stroke:rgba(89, 89, 89, 0.8);stroke-width:3");
//     circleCommanderLoyal.setAttributeNS(null, 'class', "commander");
//
//     var textCommanderLoyal = document.createElementNS(svgns, 'text');
//
//     textCommanderLoyal.setAttributeNS(null, 'x', initX + radiusCommander + 2 * extraMargin);
//     textCommanderLoyal.setAttributeNS(null, 'y', initY + 1.5 * extraMargin);
//     textCommanderLoyal.setAttributeNS(null, 'style', "fill:rgba(30, 30, 30,0.8)");
//     textCommanderLoyal.addEventListener('click', toggleTraitor);
//     textCommanderLoyal.innerHTML = " - zvest poveljnik";
//
//     canvas.appendChild(circleCommanderLoyal);
//     canvas.appendChild(textCommanderLoyal);
//
//     initY += 2* radiusCommander + extraMargin;
//
//     // Traitor commander legend
//     var circleCommanderLoyal = document.createElementNS(svgns, 'circle');
//
//     circleCommanderLoyal.setAttributeNS(null, 'cx', initX + extraMargin);
//     circleCommanderLoyal.setAttributeNS(null, 'cy', initY + extraMargin);
//     circleCommanderLoyal.setAttributeNS(null, 'r', radiusCommander);
//     circleCommanderLoyal.setAttributeNS(null, 'style', "fill:rgba(179, 0, 0,0.8);stroke:rgba(89, 89, 89, 0.8);stroke-width:3");
//     circleCommanderLoyal.setAttributeNS(null, 'class', "commander");
//
//     var textCommanderLoyal = document.createElementNS(svgns, 'text');
//
//     textCommanderLoyal.setAttributeNS(null, 'x', initX + radiusCommander + 2 * extraMargin);
//     textCommanderLoyal.setAttributeNS(null, 'y', initY + 1.5 * extraMargin);
//     textCommanderLoyal.setAttributeNS(null, 'style', "fill:rgba(30, 30, 30,0.8)");
//     textCommanderLoyal.addEventListener('click', toggleTraitor);
//     textCommanderLoyal.innerHTML = " - izdajalski poveljnik";
//
//     canvas.appendChild(circleCommanderLoyal);
//     canvas.appendChild(textCommanderLoyal);
//
//     initY += 2* radiusCommander + extraMargin;
//
//     // Attack message legend
//     var circleCommanderLoyal = document.createElementNS(svgns, 'circle');
//
//     circleCommanderLoyal.setAttributeNS(null, 'cx', initX + extraMargin);
//     circleCommanderLoyal.setAttributeNS(null, 'cy', initY + extraMargin);
//     circleCommanderLoyal.setAttributeNS(null, 'r', radiusMessage);
//     circleCommanderLoyal.setAttributeNS(null, 'style', "fill:rgba(255, 187, 153,0.8);stroke:rgba(255, 119, 51, 0.8);stroke-width:2");
//     circleCommanderLoyal.setAttributeNS(null, 'class', "commander");
//
//     var textCommanderLoyal = document.createElementNS(svgns, 'text');
//
//     textCommanderLoyal.setAttributeNS(null, 'x', initX + radiusMessage + 2 * extraMargin);
//     textCommanderLoyal.setAttributeNS(null, 'y', initY + 1.5 * extraMargin);
//     textCommanderLoyal.setAttributeNS(null, 'style', "fill:rgba(30, 30, 30,0.8)");
//     textCommanderLoyal.addEventListener('click', toggleTraitor);
//     textCommanderLoyal.innerHTML = " - ukaz za napad";
//
//     canvas.appendChild(circleCommanderLoyal);
//     canvas.appendChild(textCommanderLoyal);
//
//     initY += 2* radiusMessage + extraMargin;
//
//     // Attack message legend
//     var circleCommanderLoyal = document.createElementNS(svgns, 'circle');
//
//     circleCommanderLoyal.setAttributeNS(null, 'cx', initX + extraMargin);
//     circleCommanderLoyal.setAttributeNS(null, 'cy', initY + extraMargin);
//     circleCommanderLoyal.setAttributeNS(null, 'r', radiusMessage);
//     circleCommanderLoyal.setAttributeNS(null, 'style',                 circleStyles = "fill:rgba(179, 102, 255,0.8);stroke:rgba(102, 0, 204, 0.8);stroke-width:2"
//     );
//     circleCommanderLoyal.setAttributeNS(null, 'class', "commander");
//
//     var textCommanderLoyal = document.createElementNS(svgns, 'text');
//
//     textCommanderLoyal.setAttributeNS(null, 'x', initX + radiusMessage + 2 * extraMargin);
//     textCommanderLoyal.setAttributeNS(null, 'y', initY + 1.5 * extraMargin);
//     textCommanderLoyal.setAttributeNS(null, 'style', "fill:rgba(30, 30, 30,0.8)");
//     textCommanderLoyal.addEventListener('click', toggleTraitor);
//     textCommanderLoyal.innerHTML = " - ukaz za umik";
//
//     canvas.appendChild(circleCommanderLoyal);
//     canvas.appendChild(textCommanderLoyal);
// }
//
// function addCommander(canvas, x, y, id) {
//     var circle = document.createElementNS(svgns, 'circle');
//
//     circle.setAttributeNS(null, 'id', id);
//     circle.setAttributeNS(null, 'cx', x);
//     circle.setAttributeNS(null, 'cy', y);
//     circle.setAttributeNS(null, 'r', radiusCommander);
//     circle.setAttributeNS(null, 'style', "fill:rgba(1,163,217,0.8);stroke:rgba(89, 89, 89, 0.8);stroke-width:3");
//     circle.setAttributeNS(null, 'class', "commander");
//
//     var text = document.createElementNS(svgns, 'text');
//     text.setAttributeNS(null, 'id', id + '-label');
//     text.setAttributeNS(null, 'x', x - 6 - (id !='G'? 2:0));
//     text.setAttributeNS(null, 'y', y + 6);
//     text.addEventListener('click', toggleTraitor);
//     text.innerHTML = id;
//
//     canvas.appendChild(circle);
//     canvas.appendChild(text);
//
//     return circle;
// }
//
// function toggleTraitor(event) {
//     if (!animationIsActive) {
//         var traitor;
//         var id = event.target.id.split("-")[0];
//         // If we click on the text we have to acquire label a bit differently
//         if (event.target.id.includes("-label")) {
//             traitor = document.getElementById(id);
//         } else {
//             traitor = event.target;
//         }
//
//         if(traitors.includes(traitor)) {
//             // Ce je general, odpri formo za urejanje ukazov
//             if(id == 'G') {
//                 document.getElementById("traitorGeneralOrders").style = "display: none;"
//             }
//             traitor.style = "fill:rgba(1,163,217,0.8);stroke:rgba(89, 89, 89, 0.8);stroke-width:3";
//             var id = traitor.id;
//
//             const index = traitors.indexOf(traitor);
//             if (index > -1) {
//                 traitors.splice(index, 1);
//             }
//
//             // Spremeni vsebino tabele zvestih in izdajalskih poveljnikov
//             // Ponastavi vsebino
//             document.getElementById("izdajalci").innerHTML = "";
//             document.getElementById("zvesti").innerHTML = "";
//             zvestiTrenutno = ['G', 'L1', 'L2', 'L3', 'L4'];
//
//             // Nastavi nove vrednosti izdajalcev in zvestih poveljnikov
//             traitors.forEach((x, i) => {
//                 const ix = zvestiTrenutno.indexOf(x.id);
//                 if (ix > -1) {
//                     zvestiTrenutno.splice(ix, 1);
//                 }
//                 if (i != 0) {
//                     document.getElementById("izdajalci").innerHTML += ", ";
//                 }
//                 document.getElementById("izdajalci").innerHTML += x.id;
//             });
//             zvestiTrenutno.forEach((x, i) => {
//                 if (i != 0) {
//                     document.getElementById("zvesti").innerHTML += ", ";
//                 }
//                 document.getElementById("zvesti").innerHTML += x;
//             });
//
//         } else {
//             if(traitors.length < numberOfTraitors) {
//                 // Ce je general, odpri formo za urejanje ukazov
//                 if(id == 'G') {
//                     document.getElementById("traitorGeneralOrders").style = "display: block;"
//                 }
//                 // Spremeni vsebino tabele zvestih in izdajalskih poveljnikov
//                 // Ponastavi vsebino
//                 document.getElementById("izdajalci").innerHTML = "";
//                 document.getElementById("zvesti").innerHTML = "";
//                 zvestiTrenutno = ['G', 'L1', 'L2', 'L3', 'L4'];
//
//                 traitor.style = "fill:rgba(179, 0, 0,0.8);stroke:rgba(89, 89, 89, 0.8);stroke-width:3";
//                 var id = traitor.id;
//
//                 traitors.push(traitor);
//
//                 // Nastavi nove vrednosti izdajalcev in zvestih poveljnikov
//                 traitors.forEach((x, i) => {
//                     const ix = zvestiTrenutno.indexOf(x.id);
//                     if (ix > -1) {
//                         zvestiTrenutno.splice(ix, 1);
//                     }
//                     if (i != 0) {
//                         document.getElementById("izdajalci").innerHTML += ", ";
//                     }
//                     document.getElementById("izdajalci").innerHTML += x.id;
//                 });
//                 zvestiTrenutno.forEach((x, i) => {
//                     if (i != 0) {
//                         document.getElementById("zvesti").innerHTML += ", ";
//                     }
//                     document.getElementById("zvesti").innerHTML += x;
//                 });
//             }
//         }
//     }
// }
//
// function startAnimationGeneral() {
//     document.getElementById("pauseBtn").style = "visibility:visible;";
//     sendingDuration = document.getElementById("speed").value;
//     lieutenantsValues = [];
//     document.getElementById("result").innerHTML = '';
//
//     document.getElementById("animationBtn").disabled = true;
//     if(!animationIsActive) {
//         animationIsActive = true;
//         const xMessageStart = 0;
//         const yMessageStart = general.y + radiusCommander + radiusMessage;
//
//         const pathsFromGeneral = [];
//
//         pathsFromGeneral.push({src: general.id, dst: lieutenants[0].id, endX: lieutenants[0].x, endY: lieutenants[0].y});
//         pathsFromGeneral.push({src: general.id, dst: lieutenants[1].id, endX: lieutenants[1].x, endY: lieutenants[1].y});
//         pathsFromGeneral.push({src: general.id, dst: lieutenants[2].id, endX: lieutenants[2].x, endY: lieutenants[2].y});
//         pathsFromGeneral.push({src: general.id, dst: lieutenants[3].id, endX: lieutenants[3].x, endY: lieutenants[3].y});
//
//         pathsFromGeneral.forEach((x) => {
//             travelingMessages +=1;
//             const pathID = x.src + '-' + x.dst;
//
//             var circleStyles;
//
//             const selectOrder = document.getElementById("selectOrder" + x.dst);
//
//             if (traitors.includes(general.elHtml) && selectOrder.options[selectOrder.selectedIndex].value == "Umik") {
//                 circleStyles = "fill:rgba(179, 102, 255,0.8);stroke:rgba(102, 0, 204, 0.8);stroke-width:2";
//                 lieutenantsValues.push({src: x.src, dst: x.dst, value: false});
//             } else {
//                 circleStyles = "fill:rgba(255, 187, 153,0.8);stroke:rgba(255, 119, 51, 0.8);stroke-width:2";
//                 lieutenantsValues.push({src: x.src, dst: x.dst, value: true});
//             }
//
//             var message = document.createElementNS(svgns, 'circle');
//             message.setAttributeNS(null, 'id', pathID);
//             message.setAttributeNS(null, 'cx', xMessageStart);
//             message.setAttributeNS(null, 'cy', yMessageStart);
//             message.setAttributeNS(null, 'r', radiusMessage);
//             message.setAttributeNS(null, 'style', circleStyles);
//             message.addEventListener('click', interceptMessageFromGeneral);
//
//             var animateCX = document.createElementNS(svgns, 'animate');
//             animateCX.setAttribute("id", "animX" + pathID);
//             animateCX.setAttribute("attributeType","XML");
//             animateCX.setAttribute("attributeName","cx");
//             animateCX.setAttribute("from", xMessageStart);
//             animateCX.setAttribute("to", x.endX);
//             animateCX.setAttribute("dur", sendingDuration + "s");
//             animateCX.setAttribute("repeatCount","1");
//             animateCX.setAttribute("fill","freeze");
//             animateCX.addEventListener('endEvent', onEndEventFunctionGeneral);
//
//             var animateCY = document.createElementNS(svgns, 'animate');
//             animateCY.setAttribute("id", "animY" + pathID);
//             animateCY.setAttribute("attributeType","XML");
//             animateCY.setAttribute("attributeName","cy");
//             animateCY.setAttribute("from", yMessageStart);
//             animateCY.setAttribute("to", x.endY);
//             animateCY.setAttribute("dur", sendingDuration + "s");
//             animateCY.setAttribute("repeatCount","1");
//             animateCY.setAttribute("fill","freeze");
//             animateCY.addEventListener('endEvent', onEndEventFunctionGeneral);
//
//             message.appendChild(animateCX);
//             message.appendChild(animateCY);
//             canvas.appendChild(message);
//
//             animateCX.beginElement();
//             animateCY.beginElement();
//
//             messages.push(message);
//         });
//     }
// }
//
// function pauseAnimation() {
//     if(!animationIsPaused) {
//         canvas.pauseAnimations();
//         document.getElementById("pauseBtn").innerHTML = "<i class=\"fas fa-play\"></i>";
//         animationIsPaused = true;
//     } else {
//         canvas.unpauseAnimations();
//         document.getElementById("pauseBtn").innerHTML = "<i class=\"fas fa-pause\">";
//         animationIsPaused = false;
//     }
// }
//
//
// var nOfAnimationsCompleted = 0;
// var nMessagesFromGeneral;
// function onEndEventFunctionGeneral() {
//     nOfAnimationsCompleted++;
//     if(nOfAnimationsCompleted == 8 + travelingMessages * 2) {
//         // Reset number of animations for the next animation
//         nOfAnimationsCompleted = 0;
//
//         // Delete messages
//         const length = messages.length;
//         nMessagesFromGeneral = length;
//         for(var i = 0; i < length; i++) {
//             canvas.removeChild(messages[i]);
//         }
//
//         // Execute the other function where lieutenants send their messages
//         startAnimationLieutenants();
//     }
// }
//
// function startAnimationLieutenants() {
//     const pathsFromLieutenants = [];
//
//     lieutenants.forEach((x) => lieutenants.forEach((y) => {
//         var messageReceived = false;
//         for(var i = 0; i < messages.length; i++) {
//             if(messages[i].id == (general.id + '-' + x.id)) {
//                 messageReceived = true;
//             }
//         }
//
//         if (x != y && messageReceived) {
//             pathsFromLieutenants.push({src: x.id, dst: y.id, beginX: x.x, beginY: x.y, endX: y.x, endY: y.y});
//         }
//     }));
//     messages = [];
//
//     travelingMessages = 0;
//     pathsFromLieutenants.forEach((x) => {
//         travelingMessages +=1;
//         const pathID = x.src + '-' + x.dst;
//
//         var circleStyles;
//         const selectOrder = document.getElementById("selectOrder" + x.src);
//         const selectedValue = selectOrder.options[selectOrder.selectedIndex].value;
//         if ((traitors.includes(document.getElementById(x.src)) && (selectedValue == "Napad" || !traitors.includes(general.elHtml))) || (traitors.includes(general.elHtml) && selectedValue == "Umik" && !traitors.includes(document.getElementById(x.src)))) {
//             circleStyles = "fill:rgba(179, 102, 255,0.8);stroke:rgba(102, 0, 204, 0.8);stroke-width:2"
//             lieutenantsValues.push({src: x.src, dst: x.dst, value: false});
//         } else {
//             circleStyles = "fill:rgba(255, 187, 153,0.8);stroke:rgba(255, 119, 51, 0.8);stroke-width:2";
//             lieutenantsValues.push({src: x.src, dst: x.dst, value: true});
//         }
//         var message = document.createElementNS(svgns, 'circle');
//         message.setAttributeNS(null, 'id', pathID);
//         message.setAttributeNS(null, 'cx', x.beginX);
//         message.setAttributeNS(null, 'cy', x.beginY);
//         message.setAttributeNS(null, 'r', radiusMessage);
//         message.setAttributeNS(null, 'style', circleStyles);
//         message.addEventListener('click', interceptMessageFromLieutenant);
//
//         var animateCX = document.createElementNS(svgns, 'animate');
//         animateCX.setAttribute("id", "animX" + pathID);
//         animateCX.setAttribute("attributeType","XML");
//         animateCX.setAttribute("attributeName","cx");
//         animateCX.setAttribute("from", x.beginX);
//         animateCX.setAttribute("to", x.endX);
//         animateCX.setAttribute("dur", sendingDuration + "s");
//         animateCX.setAttribute("repeatCount","1");
//         animateCX.setAttribute("fill","freeze");
//         animateCX.addEventListener('endEvent', onEndEventFunctionLieutenants);
//
//         var animateCY = document.createElementNS(svgns, 'animate');
//         animateCY.setAttribute("id", "animY" + pathID);
//         animateCY.setAttribute("attributeType","XML");
//         animateCY.setAttribute("attributeName","cy");
//         animateCY.setAttribute("from", x.beginY);
//         animateCY.setAttribute("to", x.endY);
//         animateCY.setAttribute("dur", sendingDuration + "s");
//         animateCY.setAttribute("repeatCount","1");
//         animateCY.setAttribute("fill","freeze");
//         animateCY.addEventListener('endEvent', onEndEventFunctionLieutenants);
//
//         message.appendChild(animateCX);
//         message.appendChild(animateCY);
//         canvas.appendChild(message);
//
//         animateCX.beginElement();
//         animateCY.beginElement();
//
//         messages.push(message);
//     });
//     if (changedSpeed) {
//         sendingDuration = document.getElementById("speed").value;
//     }
// }
//
// function onEndEventFunctionLieutenants() {
//     nOfAnimationsCompleted++;
//
//     if(nOfAnimationsCompleted == nMessagesFromGeneral * 3 * 2 +  travelingMessages * 2) {
//         // Reset number of animations for the next animation
//         nOfAnimationsCompleted = 0;
//         travelingMessages = 0;
//
//         // Delete messages
//         const length = messages.length;
//         for(var i = 0; i < length; i++) {
//             canvas.removeChild(messages[i]);
//         }
//
//         messages = [];
//
//         // Show results
//         showResults();
//     }
// }
//
// function changeSpeed(speed) {
//     if (animationIsActive) {
//         changedSpeed = true;
//     } else {
//         sendingDuration = speed;
//     }
// }
//
// function changeNumberOfTraitors(nOfTraitors) {
//     numberOfTraitors = nOfTraitors;
//     if (numberOfTraitors < traitors.length) {
//         var nExtraEls = traitors.length - numberOfTraitors;
//         for (var i = 0; i < nExtraEls; i++) {
//             var el = traitors.shift();
//             el.style = "fill:rgba(1,163,217,0.8);stroke:rgba(89, 89, 89, 0.8);stroke-width:3";
//         }
//     }
// }
//
// var lessAnimations = 0;
// function showResults() {
//     var resultHeader = document.createElement('span');
//     resultHeader.innerHTML = "Rezultati algoritma ($v - napad, \\overline{v} - umik$):"
//     resultHeader.style = "font-weight:bold;";
//     document.getElementById('result').appendChild(resultHeader);
//     MathJax.Hub.Queue(["Typeset", MathJax.Hub, resultHeader]);
//
//     var stNapad = 0;
//     var stUmik = 0;
//     lieutenants.forEach(x => {
//         if(traitors.includes(x.elHtml)) {
//             var result = x.id + " je izdajalec in se umakne"
//             showAction(x, -1);
//             stUmik++;
//         } else {
//             var result = x.id + " vrne vrednost: $majority(";
//             var i = 0;
//
//             var stPozitivnih = 0;
//             var stNegativnih = 0;
//             lieutenantsValues.forEach(y => {
//                 if (x.id == y.dst) {
//                     if (i != 0) {
//                         result += ", "
//                     }
//                     if(y.value) {
//                         result += "v";
//                         stPozitivnih++;
//                     } else {
//                         result += "\\overline{v}";
//                         stNegativnih++;
//                     }
//                     i++;
//                 }
//             })
//             if (stNegativnih == 0 && stPozitivnih == 0) {
//                 result +=") = \\rightarrow$ čaka na ukaz";
//                 lessAnimations += 8;
//             } else {
//                 if (stNegativnih > stPozitivnih) {
//                     stUmik++;
//                 } else {
//                     stNapad++;
//                 }
//                 result += ") = " + (stNegativnih > stPozitivnih ? "\\overline{v} \\rightarrow$ " + x.id + " se umakne" : "v \\rightarrow$ " + x.id + " napade");
//                 showAction(x, zvestiTrenutno.indexOf(x.id) != -1 ? stPozitivnih - stNegativnih : -1);
//             }
//         }
//
//         var text = document.createTextNode(result);
//         var span = document.createElement('li');
//         span.appendChild(text);
//         document.getElementById('result').appendChild(span);
//         MathJax.Hub.Queue(["Typeset", MathJax.Hub, span]);
//     });
//
//     if(traitors.includes(general.elHtml)) {
//         stUmik++;
//     } else {
//         stNapad++;
//     }
//
//     var finalResult;
//     if(stNapad >= 4) {
//         finalResult = "Uspelo ti je zavzeti grad!";
//     } else if (stUmik == 5) {
//         finalResult = "Celotna vojska se je umaknila in preživela.";
//     } else {
//         finalResult = "Del vojske je bil uničen zaradi izdajalcev.";
//     }
//
//     var finalText = document.createTextNode(finalResult);
//     var divResult = document.createElement('div');
//     divResult.classList = ['h2'];
//     divResult.style = "font-style: italic;padding-top:20px;";
//     divResult.appendChild(finalText);
//
//     document.getElementById('result').appendChild(divResult);
//
//     showAction(general, zvestiTrenutno.indexOf('G'));
// }
//
// function showAction(el, result) {
//     const textId = el.id + '-label';
//     const textX = el.x - 6 - (el.id !='G'? 2:0)
//     const textY = el.y + 6;
//
//     if(result >= 0) {
//         var targetX = el.x < 0 ? (el.x + width/18) : (el.x - width/18);
//         var targetY = (el.y / el.x) * targetX
//         if(el.x == 0) {
//             targetX = el.x;
//             targetY = el.y + width/18;
//         }
//         // Attack
//         var animateCX = document.createElementNS(svgns, 'animate');
//         animateCX.setAttribute("attributeType","XML");
//         animateCX.setAttribute("attributeName","cx");
//         animateCX.setAttribute("from", el.x);
//         animateCX.setAttribute("to", targetX);
//         animateCX.setAttribute("dur", sendingDuration + "s");
//         animateCX.setAttribute("repeatCount","1");
//         animateCX.setAttribute("fill","freeze");
//         animateCX.addEventListener('endEvent', onAnimationIsFinished);
//
//         var animateCY = document.createElementNS(svgns, 'animate');
//         animateCY.setAttribute("attributeType","XML");
//         animateCY.setAttribute("attributeName","cy");
//         animateCY.setAttribute("from", el.y);
//         animateCY.setAttribute("to", targetY);
//         animateCY.setAttribute("dur", sendingDuration + "s");
//         animateCY.setAttribute("repeatCount","1");
//         animateCY.setAttribute("fill","freeze");
//         animateCY.addEventListener('endEvent', onAnimationIsFinished);
//
//         el.elHtml.appendChild(animateCX);
//         el.elHtml.appendChild(animateCY);
//
//         animateCX.beginElement();
//         animateCY.beginElement();
//
//         var animateXText = document.createElementNS(svgns, 'animate');
//         animateXText.setAttribute("attributeType","XML");
//         animateXText.setAttribute("attributeName","x");
//         animateXText.setAttribute("from", textX);
//         animateXText.setAttribute("to", targetX - 6 - (el.id !='G'? 2:0));
//         animateXText.setAttribute("dur", sendingDuration + "s");
//         animateXText.setAttribute("repeatCount","1");
//         animateXText.setAttribute("fill","freeze");
//         animateXText.addEventListener('endEvent', onAnimationIsFinished);
//
//         var animateYText = document.createElementNS(svgns, 'animate');
//         animateYText.setAttribute("attributeType","XML");
//         animateYText.setAttribute("attributeName","y");
//         animateYText.setAttribute("from", textY);
//         animateYText.setAttribute("to", targetY + 6);
//         animateYText.setAttribute("dur", sendingDuration + "s");
//         animateYText.setAttribute("repeatCount","1");
//         animateYText.setAttribute("fill","freeze");
//         animateYText.addEventListener('endEvent', onAnimationIsFinished);
//
//         document.getElementById(textId).appendChild(animateXText);
//         document.getElementById(textId).appendChild(animateYText);
//
//         animateXText.beginElement();
//         animateYText.beginElement();
//     } else {
//         var targetX = el.x < 0 ? (el.x - width/18) : (el.x + width/18);
//         var targetY = (el.y / el.x) * targetX
//         if(el.x == 0) {
//             targetX = el.x;
//             targetY = el.y - width/18;
//         }
//
//         // Retreat
//         var animateCX = document.createElementNS(svgns, 'animate');
//         animateCX.setAttribute("attributeType","XML");
//         animateCX.setAttribute("attributeName","cx");
//         animateCX.setAttribute("from", el.x);
//         animateCX.setAttribute("to", targetX);
//         animateCX.setAttribute("dur", sendingDuration + "s");
//         animateCX.setAttribute("repeatCount","1");
//         animateCX.setAttribute("fill","freeze");
//         animateCX.addEventListener('endEvent', onAnimationIsFinished);
//
//         var animateCY = document.createElementNS(svgns, 'animate');
//         animateCY.setAttribute("attributeType","XML");
//         animateCY.setAttribute("attributeName","cy");
//         animateCY.setAttribute("from", el.y);
//         animateCY.setAttribute("to", targetY);
//         animateCY.setAttribute("dur", sendingDuration + "s");
//         animateCY.setAttribute("repeatCount","1");
//         animateCY.setAttribute("fill","freeze");
//         animateCY.addEventListener('endEvent', onAnimationIsFinished);
//
//         el.elHtml.appendChild(animateCX);
//         el.elHtml.appendChild(animateCY);
//
//         var animateXText = document.createElementNS(svgns, 'animate');
//         animateXText.setAttribute("attributeType","XML");
//         animateXText.setAttribute("attributeName","x");
//         animateXText.setAttribute("from", textX);
//         animateXText.setAttribute("to", targetX - 6 - (el.id !='G'? 2:0));
//         animateXText.setAttribute("dur", sendingDuration + "s");
//         animateXText.setAttribute("repeatCount","1");
//         animateXText.setAttribute("fill","freeze");
//         animateXText.addEventListener('endEvent', onAnimationIsFinished);
//
//         var animateYText = document.createElementNS(svgns, 'animate');
//         animateYText.setAttribute("attributeType","XML");
//         animateYText.setAttribute("attributeName","y");
//         animateYText.setAttribute("from", textY);
//         animateYText.setAttribute("to", targetY + 6);
//         animateYText.setAttribute("dur", sendingDuration + "s");
//         animateYText.setAttribute("repeatCount","1");
//         animateYText.setAttribute("fill","freeze");
//         animateYText.addEventListener('endEvent', onAnimationIsFinished);
//
//         document.getElementById(textId).appendChild(animateXText);
//         document.getElementById(textId).appendChild(animateYText);
//
//         animateCX.beginElement();
//         animateCY.beginElement();
//         animateXText.beginElement();
//         animateYText.beginElement();
//     }
// }
//
// function onAnimationIsFinished() {
//     nOfAnimationsCompleted++;
//
//     if (nOfAnimationsCompleted == 40 - lessAnimations) {
//         // Reset number of animations for the next animation
//         nOfAnimationsCompleted = 0;
//
//         document.getElementById("pauseBtn").style = "visibility: hidden;"
//
//         // Animation is not active anymore
//         animationIsActive = false;
//
//         document.getElementById("animationBtn").innerHTML = "Ponastavi animacijo";
//         document.getElementById("animationBtn").onclick = function () {
//             document.getElementById("canvas").innerHTML="";
//             drawCanvas();
//             document.getElementById("animationBtn").innerHTML = "Ukaži napad!";
//             document.getElementById("animationBtn").onclick = startAnimationGeneral;
//             document.getElementById("traitorGeneralOrders").style = "display: none;"
//         };
//
//         document.getElementById("animationBtn").disabled = false;
//     }
// }
//
// function interceptMessageFromGeneral(e) {
//     document.getElementById("canvas").removeChild(e.target);
//     const index = messages.indexOf(e.target);
//     var id = e.target.id.split("-");
//     if (index > -1) {
//         messages.splice(index, 1);
//     }
//     travelingMessages--;
//
//     for(var i = 0; i < lieutenantsValues.length; i++) {
//         if(lieutenantsValues[i].src == id[0] && lieutenantsValues[i].dst == id[1]) {
//             lieutenantsValues.splice(i, 1);
//             i--;
//         }
//     }
//
//     if(travelingMessages == 0) {
//         setTimeout(() => {
//             // Reset number of animations for the next animation
//             nOfAnimationsCompleted = 0;
//             travelingMessages = 0;
//
//             // Delete messages
//             const length = messages.length;
//             for(var i = 0; i < length; i++) {
//                 canvas.removeChild(messages[i]);
//             }
//
//             messages = [];
//
//             // Show results
//             showResults();
//         }, 8/sendingDuration * 1000)
//     }
// }
//
// function interceptMessageFromLieutenant(e) {
//     document.getElementById("canvas").removeChild(e.target);
//     const index = messages.indexOf(e.target);
//     var id = e.target.id.split("-");
//     if (index > -1) {
//         messages.splice(index, 1);
//     }
//     travelingMessages--;
//
//     for(var i = 0; i < lieutenantsValues.length; i++) {
//         if(lieutenantsValues[i].src == id[0] && lieutenantsValues[i].dst == id[1]) {
//             lieutenantsValues.splice(i, 1);
//             i--;
//         }
//     }
//
//     if(travelingMessages == 0) {
//         setTimeout(() => {
//             // Reset number of animations for the next animation
//             nOfAnimationsCompleted = 0;
//             travelingMessages = 0;
//
//             // Delete messages
//             const length = messages.length;
//             for(var i = 0; i < length; i++) {
//                 canvas.removeChild(messages[i]);
//             }
//
//             messages = [];
//
//             // Show results
//             showResults();
//         }, 8/sendingDuration * 500)
//     }
// }
