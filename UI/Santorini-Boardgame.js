const rectSide = 110; // 120
const buildingWidth = rectSide / 3;
const buildingHeight = rectSide / 4;

const xStart = - rectSide * 2;
const yStart = - rectSide * 2;
const widthViewBox = 5 * rectSide;
const heightViewBox = 5 * rectSide;
const width = 5 * rectSide;
const height = 5 * rectSide;
const viewBox = xStart + " " + yStart + " " + width + " " + height;

const svgns = "http://www.w3.org/2000/svg";

alphaArray = ['A', 'B', 'C', 'D', 'E'];

boardState = null;

playerPos = {
    'R1': null,
    'R2': null,
    'B1': null,
    'B2': null
};

selectedFigure = null;

function boardFromHttpRequest(res) {
    boardRes = res['board']
    ix = 0
    boardState = []
    for (const iProperty in boardRes) {
        jx = 0
        row = []
        for (const jProperty in boardRes[iProperty]) {
            if (boardRes[iProperty][jProperty][1] != null) {
                playerPos[boardRes[iProperty][jProperty][1]] = [jx, ix]
            }

            row.push(boardRes[iProperty][jProperty][0])
            jx++;
        }
        boardState.push(row)
        ix++;
    }
}


function mapperAlpha(alpha) {
    switch (alpha) {
        case 'A':
            return 0;
        case 'B':
            return 1;
        case 'C':
            return 2;
        case 'D':
            return 3;
        case 'E':
            return 4;
    }
}

function deleteElems(class_name) {
    const elemsToDelete = canvas.getElementsByClassName(class_name);
    const elemsToDeleteLen = elemsToDelete.length;

    for (let i = 0; i < elemsToDeleteLen; i++) {
        const elemToDelete = elemsToDelete[0];
        elemToDelete.parentElement.removeChild(elemToDelete);
    }
}


function shadePossibleMoves(canvas, positions) {
    const elemsToDelete = canvas.getElementsByClassName("choice");
    const elemsToDeleteBuild = canvas.getElementsByClassName("build");

    const elemsToDeleteLen = elemsToDelete.length;
    if (elemsToDeleteLen > 0 || elemsToDeleteBuild.length > 0) {
        deleteElems("choice")
    } else {
        for (let i = 0; i < positions.length; i++) {
            position = [positions[i][1] - 1, mapperAlpha(positions[i][0])]
            xStartRect = xStart + position[0] * rectSide
            yStartRect = yStart + position[1] * rectSide
            var rect = document.createElementNS(svgns, 'rect');
            rect.setAttributeNS(null, 'x', xStartRect);
            rect.setAttributeNS(null, 'y', yStartRect);
            rect.setAttributeNS(null, 'height', rectSide);
            rect.setAttributeNS(null, 'width', rectSide);
            rect.setAttributeNS(null, 'style', "fill:rgba(0, 0, 0, 0.3); cursor: pointer;");
            rect.setAttributeNS(null, 'ixX', position[1]);
            rect.setAttributeNS(null, 'ixY', position[0]);
            rect.setAttributeNS(null, 'class', "choice");
            rect.addEventListener('click',
                    function() {
                        var xmlHttp = new XMLHttpRequest();
                        xmlHttp.open( "GET", 'http://127.0.0.1:8000/api/move?xOrig=' + playerPos[selectedFigure][1] + '&yOrig=' + playerPos[selectedFigure][0] +'&xTarget=' + this.getAttribute('ixX') + '&yTarget=' + this.getAttribute('ixY'), false ); // false for synchronous request
                        xmlHttp.send( null);
                        
                        const response = JSON.parse(xmlHttp.responseText)
                        drawCanvas(response);
                        checkIfFinished(canvas, response);

                    }, false);
            canvas.appendChild(rect);
        }
    }
}

function checkIfFinished(canvas, response) {
    if (response.hasOwnProperty("move")) {
        document.getElementById("move").innerHTML = response['move']
    }

    if (response.hasOwnProperty("build")) {
        document.getElementById("build").innerHTML = response['build']
    }

    if (response.hasOwnProperty("result")) {
        document.getElementById("result").innerHTML = response['result']
        // Finish game
        var rect = document.createElementNS(svgns, 'rect');
        rect.setAttributeNS(null, 'x', -heightViewBox);
        rect.setAttributeNS(null, 'y', -widthViewBox);
        rect.setAttributeNS(null, 'height', 2 * heightViewBox);
        rect.setAttributeNS(null, 'width', 2 * widthViewBox);
        rect.setAttributeNS(null, 'style', "fill:" + response['winner'] + "; cursor: pointer;");
        rect.setAttributeNS(null, 'class', "build");
        rect.addEventListener('click', function () {
            init();
        })

        canvas.appendChild(rect);

    }

    if (response.hasOwnProperty("reason")) {
        document.getElementById("reason").innerHTML = response['reason']
    }

}

function shadePossibleBuilds(canvas, positions) {
    const elemsToDelete = canvas.getElementsByClassName("build");
    const elemsToDeleteLen = elemsToDelete.length;
    if (elemsToDeleteLen > 0) {
        deleteElems("build")
    } else {
        for (let i = 0; i < positions.length; i++) {
            position = [positions[i][1] - 1, mapperAlpha(positions[i][0])]
            xStartRect = xStart + position[0] * rectSide
            yStartRect = yStart + position[1] * rectSide
            var rect = document.createElementNS(svgns, 'rect');
            rect.setAttributeNS(null, 'x', xStartRect);
            rect.setAttributeNS(null, 'y', yStartRect);
            rect.setAttributeNS(null, 'height', rectSide);
            rect.setAttributeNS(null, 'width', rectSide);
            rect.setAttributeNS(null, 'style', "fill:rgba(0, 255, 0, 0.3); cursor: pointer;");
            rect.setAttributeNS(null, 'ixX', position[1]);
            rect.setAttributeNS(null, 'ixY', position[0]);
            rect.setAttributeNS(null, 'class', "build");
            rect.addEventListener('click',
                    function() {
                        var xmlHttp = new XMLHttpRequest();
                        xmlHttp.open( "GET", 'http://127.0.0.1:8000/api/build?x=' + this.getAttribute('ixX') + '&y=' + this.getAttribute('ixY'), false ); // false for synchronous request
                        xmlHttp.send( null);
                        
                        const response = JSON.parse(xmlHttp.responseText)
                        drawCanvas(response);
                        checkIfFinished(canvas, response);
                    }, false);
            canvas.appendChild(rect);
        }
    }
}

function drawCanvas(res) {
    var canvas = document.getElementById("canvas");
    canvas.setAttribute("viewBox", viewBox);
    canvas.setAttribute("width", widthViewBox);
    canvas.setAttribute("height", heightViewBox);

    deleteElems("choice")
    deleteElems("build")

    boardFromHttpRequest(res)

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

                        // Draw letter
            var iAnnotation = document.createElementNS(svgns, 'text');
            iAnnotation.setAttributeNS(null, 'x', xStartRect + 5);
            iAnnotation.setAttributeNS(null, 'y', yStartRect + rectSide - 5);
            iAnnotation.setAttributeNS(null, 'style', "stroke:#FFFBE6;");

            var textNode = document.createTextNode(alphaArray[i] + (j + 1));
            iAnnotation.appendChild(textNode);

            canvas.appendChild(iAnnotation)

            xStartRect += rectSide
        }
        yStartRect += rectSide
    }
    if (res.hasOwnProperty("availableConstructions"))
        shadePossibleBuilds(canvas, res["availableConstructions"]);


    var player11 = document.createElementNS(svgns, 'circle');
    player11.setAttributeNS(null, 'cx', xStart + (playerPos["R1"][0] + 1 / 2) * rectSide);
    player11.setAttributeNS(null, 'cy', yStart + (playerPos["R1"][1] + 1 / 2) * rectSide);
    player11.setAttributeNS(null, 'r', 20);
    player11.setAttributeNS(null, 'style', "fill:rgba(222, 146, 168, 0.7);stroke:#98556b;stroke-width:3;cursor:pointer;");
    player11.addEventListener('click',
        function() {
            selectedFigure = "R1";

            var xmlHttp = new XMLHttpRequest();
            xmlHttp.open( "GET", 'http://127.0.0.1:8000/api/choose?x=' + playerPos[selectedFigure][1] + '&y=' + playerPos[selectedFigure][0], false ); // false for synchronous request
            xmlHttp.send( null );

            shadePossibleMoves(canvas, JSON.parse(xmlHttp.responseText))
        }, false);

    canvas.appendChild(player11);

    var player12 = document.createElementNS(svgns, 'circle');

    player12.setAttributeNS(null, 'cx', xStart + (playerPos["R2"][0] + 1 / 2) * rectSide);
    player12.setAttributeNS(null, 'cy', yStart + (playerPos["R2"][1] + 1 / 2) * rectSide);
    player12.setAttributeNS(null, 'r', 20);
    player12.setAttributeNS(null, 'style', "fill:rgba(222, 146, 168, 0.7);stroke:#98556b;stroke-width:3;cursor:pointer;");
    player12.addEventListener('click',
        function() {
            selectedFigure = "R2";

            var xmlHttp = new XMLHttpRequest();
            xmlHttp.open( "GET", 'http://127.0.0.1:8000/api/choose?x=' + playerPos[selectedFigure][1] + '&y=' + playerPos[selectedFigure][0], false ); // false for synchronous request
            xmlHttp.send( null );
            shadePossibleMoves(canvas, JSON.parse(xmlHttp.responseText))
        }, false);

    canvas.appendChild(player12);

    var player21 = document.createElementNS(svgns, 'circle');

    player21.setAttributeNS(null, 'cx', xStart + (playerPos["B1"][0] + 1 / 2) * rectSide);
    player21.setAttributeNS(null, 'cy', yStart + (playerPos["B1"][1] + 1 / 2) * rectSide);
    player21.setAttributeNS(null, 'r', 20);
    player21.setAttributeNS(null, 'style', "fill:rgba(194, 229, 255, 0.7);stroke:#558198;stroke-width:3;");

    canvas.appendChild(player21);

    var player22 = document.createElementNS(svgns, 'circle');

    player22.setAttributeNS(null, 'cx', xStart + (playerPos["B2"][0] + 1 / 2) * rectSide);
    player22.setAttributeNS(null, 'cy', yStart + (playerPos["B2"][1] + 1 / 2) * rectSide);
    player22.setAttributeNS(null, 'r', 20);
    player22.setAttributeNS(null, 'style', "fill:rgba(194, 229, 255, 0.7);stroke:#558198;stroke-width:3;");

    canvas.appendChild(player22);

}

function init(alg) {

    boardState = null;

    playerPos = {
        'R1': null,
        'R2': null,
        'B1': null,
        'B2': null
    };

    selectedFigure = null;
    if (alg == null)
        alg = 'Random'

    document.getElementById("dropdownMenuButtonAI").innerText = alg

    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", 'http://127.0.0.1:8000/api/init?alg=' + alg, false ); // false for synchronous request
    xmlHttp.send( null );

    drawCanvas(
        JSON.parse(xmlHttp.responseText)
    );
}