
var scenes = [];
var current_scene = -1;
var page = 0;

var sad_colours = [ "#ff3b30", "#1d62f0", "#ffcd02", "#4cd964", "#ff9500", "#ef4db6", "#d6cec3" ];
var part_mask = [ true, true, true, true, true, true, true ];

$(function () {

    for (var i = 0; i < 9; i++) {
        $("#partBrowser").before("<div class='thumbnail' id='t" + i + "' />");
        var scene = new Scene($("#t" + i))
        scene.draw_problem(i);
        scene.render();
        scenes.push(scene);
    }

    $(".thumbnail").click(goToFullscreen);
    $(".thumbnail").mouseover(hoverBegin);
    $(".thumbnail").mouseout(hoverEnd);

    for (var i = 0; i < 7; i++) {
        $("#partBrowser").append("<div class='buttonPart' id='p" + i + "' style='background: " + sad_colours[i] + "' />");
        $("#p" + i).click(togglePart);
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
    for (var i = 0; i < 9; i++) {
        var div = $("#t" + i);
        div.removeClass("thumbnail");
        if ($(this).attr('id') == div.attr('id')) {
            div.addClass("thumbnail_big");
            scenes[i].draw_solution(page * 9 + i, part_mask);
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
            if (!div.hasClass("thumbnail_big")) {
                scenes[i].stopAnimation();
            }
        }
    }
}

function togglePart() {
    if (current_scene < 0)
        return;

    for (var i = 0; i < 7; i++) {
        var div = $("#p" + i);

        if ($(this).attr('id') == div.attr('id')) {
            part_mask[i] = !part_mask[i];

            if (part_mask[i]) {
                // TODO: Set opacity
            } else {
                // TODO: Set opacity
            }

            scenes[current_scene].draw_solution(page * 9 + current_scene, part_mask);
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

