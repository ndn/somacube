
var scenes = [];
var page = 0;

$(function () {

    for (var i = 0; i < 9; i++) {
        $("#content").append("<div class='thumbnail' id='t" + i + "' />");
        var scene = new Scene($("#t" + i))
        scene.draw_problem(i);
        scene.render();
        scenes.push(scene);
    }

    $(".thumbnail").click(goToFullscreen);
    $(".thumbnail").mouseover(hoverBegin);
    $(".thumbnail").mouseout(hoverEnd);

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
    for (var i = 0; i < 9; i++) {
        var div = $("#t" + i);
        div.removeClass("thumbnail");
        if ($(this).attr('id') == div.attr('id')) {
            div.addClass("thumbnail_big");
            scenes[i].startAnimation();
            scenes[i].resize(div.width(), div.height());
        } else {
            div.addClass("thumbnail_invisible");
        }
    }

    $(".thumbnail_big").click(goToGallery);
}

function goToGallery() {
    for (var i = 0; i < 9; i++) {
        var div = $("#t" + i);
        div.removeClass("thumbnail_invisible");
        div.removeClass("thumbnail_big");
        div.addClass("thumbnail");
        if ($(this).attr('id') == div.attr('id')) {
            scenes[i].stopAnimation();
            scenes[i].resize(div.width(), div.height());
        }
    }

    $(".thumbnail").click(goToFullscreen);
    $(".thumbnail").mouseover(hoverBegin);
    $(".thumbnail").mouseout(hoverEnd);
}

function hoverBegin() {
    for (var i = 0; i < 9; i++) {
        var div = $("#t" + i);
        if ($(this).attr('id') == div.attr('id')) {
            scenes[i].startAnimation();
        }
    }
}

function hoverEnd() {
    for (var i = 0; i < 9; i++) {
        var div = $("#t" + i);
        if ($(this).attr('id') == div.attr('id')) {
            scenes[i].stopAnimation();
        }
    }
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

