
var BLOCKSIZE = 90;

function Scene(div) {
    this.div = div;

    this.mesh = null;
    this.paused = true;

    this.renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
    this.renderer.setSize(div.width(), div.height());

    div.append(this.renderer.domElement);

    this.scene = new THREE.Scene();

    this.camera = new THREE.PerspectiveCamera(90, 1, 1, 1000);
    this.camera.position.y = 200;

    var light = new THREE.HemisphereLight(0xcccccc, 0xffffff, 1.1);
    this.scene.add(light);
}

Scene.prototype.draw_problem = function(index) {
    if (this.mesh != null) {
        this.scene.remove(this.mesh);
        this.mesh = null;
    }
    if (index < problems.length) {
        var shape = problems[index];
        this.mesh = draw_shape(shape, center(shape), 0xffffff);
        this.scene.add(this.mesh);
    }
    this.render();
}

Scene.prototype.draw_solution = function(index) {
    var colours = [ 0xff3b30, 0x1d62f0, 0xffcd02, 0x4cd964, 0xff9500, 0xef4db6, 0xd6cec3 ];
    var new_mesh = new THREE.Mesh();
    var offset = center(problems[index]);

    for (var i = 0; i < solutions[index].length; i++) {
        new_mesh.add(draw_shape(solutions[index][i], offset, colours[i]));
    }
    this.scene.remove(this.mesh);
    this.mesh = new_mesh;
    this.scene.add(this.mesh);
}

Scene.prototype.render = function() {
    if (!this.paused)
        /*
         * Patch I didn't bother to understand.
         * http://stackoverflow.com/questions/6065169/requestanimationframe-with-this-keyword
         */
        requestAnimationFrame(this.render.bind(this));

    var timer = Date.now() * 0.0005;

    this.camera.position.x = Math.cos(timer) * 600;
    this.camera.position.z = Math.sin(timer) * 600;
    this.camera.lookAt(this.scene.position);

    this.renderer.render(this.scene, this.camera);
}

Scene.prototype.resize = function(width, height) {
    this.renderer.setSize(width, height);
    if (this.paused)
        this.render();
}

Scene.prototype.startAnimation = function() {
    if (this.paused) {
        this.paused = false;
        this.render();
    }
}

Scene.prototype.stopAnimation = function() {
    this.paused = true;
}


function draw_shape(shape, offset, colour) {
    var mesh = new THREE.Mesh();
    for (var i = 0; i < shape.length; i++) {
        var geometry = new THREE.BoxGeometry(BLOCKSIZE-1, BLOCKSIZE-1, BLOCKSIZE-1);
        var material = new THREE.MeshBasicMaterial({ color: colour });
        var tmp = new THREE.Mesh(geometry, material);
        tmp.position.x = shape[i][0] * BLOCKSIZE - offset[0];
        tmp.position.y = shape[i][1] * BLOCKSIZE - offset[1];
        tmp.position.z = shape[i][2] * BLOCKSIZE - offset[2];
        mesh.add(tmp)
        var outline = new THREE.EdgesHelper(tmp, 0x000000);
        outline.material.linewidth = 2;
        mesh.add(outline);
    }
    return mesh;
}

function center(shape) {
    var x = 0, y = 0, z = 0;
    for (var i = 0; i < shape.length; i++) {
        x = Math.max(shape[i][0] + 1, x);
        z = Math.max(shape[i][1] + 1, z);
        y = Math.max(shape[i][2] + 1, y);
    }

    x = (x / 2.0) * BLOCKSIZE - (BLOCKSIZE / 2.0);
    z = (z / 2.0) * BLOCKSIZE - (BLOCKSIZE / 2.0);
    y = (y / 2.0) * BLOCKSIZE - (BLOCKSIZE / 2.0);

    return [ x, z, y ];
}
