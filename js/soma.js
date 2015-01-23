
var scenes = [];
var current_scene = -1;
var page = 0;

var sad_colours = [ "#ff3b30", "#1d62f0", "#ffcd02", "#4cd964", "#ff9500", "#ef4db6", "#d6cec3" ];
var part_mask = [ true, true, true, true, true, true, true ];
var transparency_mask = [ false, false, false, false, false, false, false ];

$(function () {

    for (var i = 0; i < 9; i++) {
        $("#partBrowser").before("<div class='thumbnail' id='t" + i + "' />");
        var scene = new Scene($("#t" + i))
        scene.draw_problem(i);
        scene.render();
        scenes.push(scene);
    }

    $(".thumbnail").click(goToFullscreen);
    $(".thumbnail").mouseover(hoverSceneBegin);
    $(".thumbnail").mouseout(hoverSceneEnd);

    for (var i = 0; i < 7; i++) {
        $("#partBrowser").append("<div class='buttonPart' id='p" + i + "' style='background: " + sad_colours[i] + "' />");
        var div = $("#p" + i);
        div.click(togglePart);
        div.mouseover(hoverPartBegin);
        div.mouseout(hoverPartEnd);
    }

    document.addEventListener('keyup', onKeyUp, false);
});

function drawNextPage() {
    page += 1;
    if (page * 9 < problems.length) {
        for (var i = 0; i < 9; i++) {
            scenes[i].draw_problem(page * 9 + i);
        }
    }
}

function drawPrevPage() {
    if (page > 0) {
        page -= 1;
        for (var i = 0; i < 9; i++) {
            scenes[i].draw_problem(page * 9 + i);
        }
    }
}

function goToFullscreen() {
    resetMasks();

    for (var i = 0; i < 9; i++) {
        var div = $("#t" + i);
        div.removeClass("thumbnail");
        if ($(this).attr('id') == div.attr('id')) {
            div.addClass("thumbnail_big");
            scenes[i].draw_solution(page * 9 + i, part_mask, transparency_mask);
            scenes[i].startAnimation();
            scenes[i].resize(div.width(), div.height());
            current_scene = i;
        } else {
            div.addClass("thumbnail_invisible");
        }
    }

    $(".thumbnail_big").click(goToGallery);
}

function goToGallery() {
    resetMasks();

    for (var i = 0; i < 9; i++) {
        var div = $("#t" + i);
        div.removeClass("thumbnail_invisible");
        div.removeClass("thumbnail_big");
        div.addClass("thumbnail");
        if ($(this).attr('id') == div.attr('id')) {
            scenes[i].draw_problem(page * 9 + i);
            scenes[i].stopAnimation();
            scenes[i].resize(div.width(), div.height());
        }
    }
    current_scene = -1;

    $(".thumbnail").click(goToFullscreen);
    $(".thumbnail").mouseover(hoverSceneBegin);
    $(".thumbnail").mouseout(hoverSceneEnd);
}

function hoverSceneBegin() {
    if (current_scene >= 0)
        return;

    var i = getIndexFromId(this);
    scenes[i].startAnimation();
}

function hoverSceneEnd() {
    if (current_scene >= 0)
        return;

    var i = getIndexFromId(this);
    scenes[i].stopAnimation();
}

function togglePart() {
    if (current_scene < 0)
        return;

    var i = getIndexFromId(this);

    part_mask[i] = !part_mask[i];

    if (part_mask[i]) {
        // TODO: Set opacity
    } else {
        // TODO: Set opacity
    }

    scenes[current_scene].draw_solution(page * 9 + current_scene, part_mask, transparency_mask);
}

function hoverPartBegin() {
    if (current_scene < 0)
        return;

    var i = getIndexFromId(this);
    transparency_mask[i] = true;
    scenes[current_scene].draw_solution(page * 9 + current_scene, part_mask, transparency_mask);
}

function hoverPartEnd() {
    if (current_scene < 0)
        return;

    var i = getIndexFromId(this);
    transparency_mask[i] = false;
    scenes[current_scene].draw_solution(page * 9 + current_scene, part_mask, transparency_mask);
}

function resetMasks() {
    for (var i = 0; i < 8; i++) {
        part_mask[i] = true;
        transparency_mask[i] = false;
    }
}

function getIndexFromId(obj) {
    return $(obj).attr("id")[1];
}

function onKeyUp(event) {
    switch (event.keyCode) {
        case 37: // left
            drawPrevPage();
            break;
        case 39: // right
            drawNextPage();
            break;
        default:
            return;
    }
}

