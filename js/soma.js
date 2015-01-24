
var scenes = [];
var currentScene = -1;
var page = 0;

var part_mask = [ true, true, true, true, true, true, true ];
var transparency_mask = [ false, false, false, false, false, false, false ];

$(function () {
    $("#count").text("page " + (page + 1) + " / " + Math.ceil(problems.length / 9));

    for (var i = 0; i < 9; i++) {
        $("#navigation").before("<div class='scene scene_small' id='t" + i + "' />");
        var scene = new Scene($("#t" + i))
        scene.draw_problem(i);
        scene.render();
        scenes.push(scene);
    }

    $("#navigation").append("<div id='previousButton' />");
    for (var i = 0; i < 7; i++) {
        $("#navigation").append("<div class='partButton invisible' id='p" + i + "' style='background: #" + colours[i].toString(16) + "' />");
    }
    $("#navigation").append("<div id='nextButton' />");

    $(".scene")
        .click(clickScene)
        .mouseover(hoverSceneBegin)
        .mouseout(hoverSceneEnd);

    $(".partButton")
        .click(togglePart)
        .mouseover(hoverPartBegin)
        .mouseout(hoverPartEnd);

    $("#previousButton").click(previous);
    $("#nextButton").click(next);

    $("#about_link").click(clickAbout);

    document.addEventListener('keyup', onKeyUp, false);
});

function clickScene() {
    var i = getIndexFromId(this);
    var div = $("#t" + i);
    toggleScene(i, div);
}

function toggleScene(i, div) {
    resetMasks();

    if (currentScene < 0) {
        $(".scene").removeClass("scene_small");
        $(".scene").addClass("disappear");

        div.removeClass("disappear");
        div.addClass("scene_big");

        scenes[i].draw_solution(page * 9 + i, part_mask, transparency_mask);
        scenes[i].startAnimation();
        scenes[i].resize(div.width(), div.height());
        currentScene = i;

        $(".partButton").removeClass("invisible");
        $("#count").text("problem " + (page * 9 + currentScene + 1) + " / " + problems.length);
    } else {
        $(".scene").removeClass("disappear");
        $(".scene").removeClass("scene_big");
        $(".scene").addClass("scene_small");

        for (var j = 0; j < 9; j++) {
            scenes[j].draw_problem(page * 9 + j);
            scenes[j].stopAnimation();
            scenes[j].resize(div.width(), div.height());
        }

        $(".partButton").addClass("invisible");

        currentScene = -1;

        $("#count").text("page " + (page + 1) + " / " + Math.ceil(problems.length / 9));
    }
}

function hoverSceneBegin() {
    if (currentScene >= 0)
        return;

    var i = getIndexFromId(this);
    scenes[i].startAnimation();
}

function hoverSceneEnd() {
    if (currentScene >= 0)
        return;

    var i = getIndexFromId(this);
    scenes[i].stopAnimation();
}

function togglePart() {
    if (currentScene < 0)
        return;

    var i = getIndexFromId(this);

    part_mask[i] = !part_mask[i];

    if (part_mask[i]) {
        $("#p" + i).css("opacity", 1.0);
    } else {
        $("#p" + i).css("opacity", 0.4);
    }

    scenes[currentScene].draw_solution(page * 9 + currentScene, part_mask, transparency_mask);
}

function hoverPartBegin() {
    if (currentScene < 0)
        return;

    var i = getIndexFromId(this);
    transparency_mask[i] = true;
    scenes[currentScene].draw_solution(page * 9 + currentScene, part_mask, transparency_mask);
}

function hoverPartEnd() {
    if (currentScene < 0)
        return;

    var i = getIndexFromId(this);
    transparency_mask[i] = false;
    scenes[currentScene].draw_solution(page * 9 + currentScene, part_mask, transparency_mask);
}

function resetMasks() {
    for (var i = 0; i < 8; i++) {
        part_mask[i] = true;
        transparency_mask[i] = false;
    }
}

function getIndexFromId(obj) {
    return parseInt($(obj).attr("id")[1]);
}

function next() {
    if (currentScene < 0) {
        if ((page + 1) * 9 < problems.length) {
            page += 1;
            for (var i = 0; i < 9; i++) {
                scenes[i].draw_problem(page * 9 + i);
            }
        }
        $("#count").text("page " + (page + 1) + " / " + Math.ceil(problems.length / 9));
    } else {
        var i = currentScene;
        var new_i = i + 1;
        if (page * 9 + new_i < problems.length) {
            if (new_i > 8) {
                new_i = 0;
                page += 1;
            }
            toggleScene(i, $("#t" + i));
            toggleScene(new_i, $("#t" + new_i));
        }
    }
}

function previous() {
    if (currentScene < 0) {
        if (page > 0) {
            page -= 1;
            for (var i = 0; i < 9; i++) {
                scenes[i].draw_problem(page * 9 + i);
            }
        }
        $("#count").text("page " + (page + 1) + " / " + Math.ceil(problems.length / 9));
    } else {
        var i = currentScene;
        var new_i = i - 1;
        if (page * 9 + new_i >= 0) {
            if (new_i < 0) {
                new_i = 8;
                page -= 1;
            }
            toggleScene(i, $("#t" + i));
            toggleScene(new_i, $("#t" + new_i));
        }
    }
}

function onKeyUp(event) {
    switch (event.keyCode) {
        case 37:
            previous();
            break;
        case 39:
            next();
            break;
        default:
            return;
    }
}

function clickAbout() {
    var div = $("#about_box");
    if (div.hasClass("disappear")) {
        $("#about_link").text("hide about");
        div.removeClass("disappear");
    } else {
        $("#about_link").text("about");
        div.addClass("disappear");
    }
}

