dojo.require("dojox.gfx");
dojo.require("dojox.gfx.utils");
         
var weight1 = 0.25;
var weight2 = 0.75;
          
dojo.ready(function() {
  var node = dojo.byId("surface");
  var surface = dojox.gfx.createSurface(node, 600, 600);
  surface.whenLoaded(function() {
    var history = [];

    window.surface = surface;
    var pathTest = surface.createPath().setStroke("black");
    var isDrawing = false;
    var lastCoord = [0, 0];
    var path = null;
    var surfaceDom = dojo.query('#surface');
    var startCoord = [0, 0];
                
    function getPoint(e) {
      return [e.layerX-6, e.layerY-6];
    }
                                
    surfaceDom.onmousedown(function(e) {
        isDrawing = true;
        startCoord = getPoint(e);
        lastCoord = startCoord; 
        path = [];
        path = surface.createPath().setStroke({
        width: 4,
        color: "black",
        cap: "round",
        join: "bevel"
      });

      path.moveTo(lastCoord);
    });
      
    dojo.query(document).onmouseup(function(e) {
      isDrawing = false;
      function randomColor() {
        return [
          parseInt(Math.random()*255),
          parseInt(Math.random()*255),
          parseInt(Math.random()*255)
        ];
      }
                
      if(path != null) {
              path.lineTo(startCoord);
              path.setFill({
                      type: "linear",
                      x1: 0,
                      y1: 0,
                      x2: 600,
                      y2: 600,
                      colors: [
                              {offset: 0, color: randomColor()},
                              {offset: 0.25, color: randomColor()},
                              {offset: 0.5, color: randomColor()},
                              {offset: 1, color: randomColor()}
                      ]
              });
              history.push(path);
              console.dir(history);
              path = null;
        }
    });
      
      dojo.query(document).onmousemove(function(e) {
            if(isDrawing) {
              var coord = getPoint(e);
                              
              var avg1 = [
                    (lastCoord[0] * (1-weight1)) + (coord[0] * weight1),
                    (lastCoord[1] * (1-weight1)) + (coord[1] * weight1)
              ];
              var avg2 = [
                    (lastCoord[0] * (1-weight2)) + (coord[0] * weight2),
                    (lastCoord[1] * (1-weight2)) + (coord[1] * weight2)
              ];
              //path.hLineTo(coord[0]);
              //path.vLineTo(coord[1]);
          path.curveTo(avg1, avg2, coord);
          lastCoord = coord;
            }
      });
      
      dojo.query('#undo').onclick(function() {
            var pathToUndo = history.pop();
            console.dir(history);
            if(pathToUndo) {
               pathToUndo.removeShape();
            }
      });
      
      dojo.query('#save').onclick(function(e) {
            var data = surface.rawNode.toDataURL();
            dojo.byId('data-url').value = data;
      });
        
    });
});