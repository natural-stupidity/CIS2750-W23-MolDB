// Michael Sirna
// 1094947
// 2023-09-10
// CIS2750 Assignment 4 Updated 2


// Initialize Stuff
let moleculesList = [];
let elementsList = [];
let saveOrEdit = "";
let svgMode = 1;
$("#filter-list").val("");
$("#modal-filter-list").val("");
updateMoleculeList();
updateElementList();
updateSvgMode();

window.mobileAndTabletCheck = function() {
    let check = false;
    (function(a) { if (/(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|iris|kindle|lge |maemo|midp|mmp|mobile.+firefox|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows ce|xda|xiino|android|ipad|playbook|silk/i.test(a) || /1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-/i.test(a.substr(0, 4))) check = true; })(navigator.userAgent || navigator.vendor || window.opera);
    return check;
};

$(document).ready(function() {
    if (mobileAndTabletCheck()) {
        alert("Hey! You seem to be using a phone or tablet to view this website!\nI won't stop you, but I highly recommend using a PC instead as things might not look right. Thanks!");
    }
});

/* Removes the preloader when the document loads */
$(document).ready(function($) {
    $("#preloader").fadeOut("slow", function() { $(this).remove(); });
});


/* === File Upload Stuff === */
$(".file-upload-wrap").bind("dragover", function() {
    $(".file-upload-wrap").addClass("image-dropping");
});

$(".file-upload-wrap").bind("dragleave", function() {
    $(".file-upload-wrap").removeClass("image-dropping");
});

function readFile(input) {
    let fileName = $("#fileName");
    let inputImage = document.querySelector("input[type=file]").files[0];
    $(".file-select-btn").hide();
    $("#file-upload-btn").show();
    $(".file-upload-wrap").removeClass("image-dropping");
    fileName.innerText = inputImage.name;

    if (input.files && input.files[0]) {

        var reader = new FileReader();
        reader.onload = function() {
            $(".file-upload-wrap").hide();
            $(".file-upload-content").show();
            $(".file-name-input").val(input.files[0].name);
        };

        reader.readAsDataURL(input.files[0]);

    } else {
        removeUpload();
    }
}

$("#file-upload-form").on("submit", function(e) {
    e.preventDefault();
    $("#file-upload-btn").prop("disabled", true);
    $("#remove-upload").prop("disabled", true);
    $("#file-upload-btn").html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Upload SDF`);

    let formData = new FormData(this);
    const fr = new FileReader();
    fr.onload = () => {
        data = {
            "file": fr.result,
            "molecule-name": formData.get("molecule-name")
        }

        $.ajax({
            type: "POST",
            url: "/add-molecule",
            data: JSON.stringify(data),
            processData: false,
            contentType: false,

            statusCode: {
                200: function(response) {
                    showMolecule(response, formData.get("molecule-name"));
                    notify("success", "Molecule was uploaded successfully!");
                },
                406: function() {
                    notify("error", "File is not valid .sdf!");
                },
                409: function() {
                    notify("error", `Molecule "${formData.get("molecule-name")}" already exists in the database!`);
                }
            }
        }).always(function() {
            $("#file-upload-btn").prop("disabled", false);
            $("#remove-upload").prop("disabled", false);
            $("#file-upload-btn").html("Upload SDF");
        });
    }
    fr.readAsText(formData.get("file"));
});

$("#remove-upload").on("click", function(e) {
    e.preventDefault();
    removeUpload();
});

function removeUpload() {
    $(".file-upload-box").replaceWith($(".file-upload-box").clone());
    $(".file-upload-content").hide();
    $("#file-upload-btn").hide();
    $(".file-upload-wrap").show();
    $(".file-select-btn").show();
}


/* === Molecule View Stuff === */
function showMolecule(svgResponse, moleculeName) {
    $(".modal").modal("hide");
    $(".svg-box").children().replaceWith(svgResponse);
    $("#home-screen").hide();
    removeUpload();
    updateElementList();
    updateMoleculeList();
    getMoleculeInfo(moleculeName);
    $(".molecule-display").show();
    setSVGbox();
    getRotations(moleculeName);
    resetSliders();
}

function getMoleculeInfo(inputData) {
    $.ajax({
        type: "POST",
        url: "/mol-info.html",
        data: inputData,
        processData: false,
        contentType: false,

        success: function(response) {
            moleculeInfo = JSON.parse(response);
            $("#info-box-mol-name").html(moleculeInfo.name);
            $("#info-box-nomenclature").html(moleculeInfo.nomenString);
            $("#info-box-atom-no").html(moleculeInfo.numAtoms);
            $("#info-box-bond-no").html(moleculeInfo.numBonds);
            legendContent = "";
            for (let i = 0; i < moleculeInfo.elements.length; i++) {
                legendContent += `
                <div class="col" style="min-width: 150px; min-height:200px; max-width: 150px; max-height: 200px; padding: 5px;">
                    <div class="card h-100">
                        <div class="card-header text-center text-nowrapstyle="font-size: ${ 
                            (elementsList[i].number.toString().length + 3 + elementsList[i].name.length + 3 + elementsList[i].symbol.length) > 23 ? "0.9rem" : 
                            (elementsList[i].number.toString().length + 3 + elementsList[i].name.length + 3 + elementsList[i].symbol.length) > 21 ? "1rem" :
                            (elementsList[i].number.toString().length + 3 + elementsList[i].name.length + 3 + elementsList[i].symbol.length) > 18 ? "1.2rem" : "1.25rem"
                        }">
                            <h5 class="card-title" style="font-size: ${ $("#element-card-header-" + moleculeInfo.elements[i][1]).width() / 12}"><b>${moleculeInfo.elements[i][0] == 0 ? "? (" + moleculeInfo.elements[i][1] + ")" : moleculeInfo.elements[i][2]}</b></h5>
                        </div>
                        <img id="ae-card-img-preview" class="card-img">
                            <svg class="w-100 h-100 m-auto">
                                <radialGradient id="${moleculeInfo.elements[i][2]}-legend" cx="-50%" cy="-50%" r="220%" fx="20%" fy="20%">
                                    <stop offset="0%" stop-color="#${moleculeInfo.elements[i][3]}"/>
                                    <stop offset="50%" stop-color="#${moleculeInfo.elements[i][4]}"/>
                                    <stop offset="100%" stop-color="#${moleculeInfo.elements[i][5]}"/>
                                </radialGradient>
                                <circle cx="50%" cy="50%" r="${moleculeInfo.elements[i][6]}" fill="url(#${moleculeInfo.elements[i][2]}-legend)"/>
                            </svg>
                        </img>
                    </div>
                </div>`
            }
            $("#molecule-legend").html(legendContent);
            $("#mol-info-loading").hide();
            $("#legend-loading").hide();
            $("#molecule-info-edit-button").attr("name", moleculeInfo.name);
            $("#molecule-info-edit-button").show();
            $("#mol-info-table").show();
            $("#molecule-legend").show();
        },
        error: function() {
            notify("error", "Failed to retrieve molecule info.");
        }
    });
}

$("#remove-molecule").on("click", function() {
    removeMolecule();
});

function removeMolecule() {
    $(".molecule-display").hide();
    rotationData = {};
    resetSliders();
    $(".svg-box").children().replaceWith("<svg></svg>");
    $("#molecule-info-edit-button").hide();
    $("#mol-info-table").hide();
    $("molecule-legend").hide();
    $("#rotation-options-div").hide();
    $("#mol-info-loading").show();
    $("legend-loading").show();
    $("#rotation-options-loading").show();
    $("#home-screen").show();
}


/* === Molecules List Stuff === */
$(document).on("click", ".view-molecule", function() {
    let button = $(this);
    let name = $(this).attr("name");
    if (confirm(`Would you like to view the molecule "${name}?"`)) {
        button.prop("disabled", true);
        button.html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> View`);

        $.ajax({
            type: "POST",
            url: "/view-molecule",
            data: name,

            statusCode: {
                200: function(response) {
                    showMolecule(response, name);
                }
            }
        }).always(function() {
            button.prop("disabled", false);
            button.html(`<i class="bi bi-search"></i> View `);
        });
    }
});

$(document).on("click", ".edit-molecule", function() {
    let button = $(this);
    let input = prompt("Please enter the new name for the molecule:", $(this).attr("name"));
    if (input != null && input != "") {
        button.prop("disabled", true);
        button.html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Edit Name`);
        let newMoleculeData = {
            oldName: $(this).attr("name"),
            newName: input
        }

        $.ajax({
            type: "POST",
            url: "/edit-molecule",
            data: JSON.stringify(newMoleculeData),

            statusCode: {
                200: function() {
                    updateMoleculeList();
                    $("#info-box-mol-name").html(input);
                    notify("success", "Molecule's name was edited successfully!");
                },
                409: function() {
                    notify("error", `Molecule "${input}" already exists in the database!`);
                },
            }
        }).always(function() {
            button.prop("disabled", false);
            button.html(`<i class="bi bi-pencil"></i> Edit Name `);
        });;
    }
});

$(document).on("click", ".delete-molecule", function() {
    let button = $(this);
    let name = button.attr("name");
    if (confirm(`Are you sure you want to delete the molecule "${name}"?`)) {
        button.prop("disabled", true);
        button.html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Delete`);
        $.ajax({
            type: "POST",
            url: "/delete-molecule",
            data: name,

            success: function() {
                updateMoleculeList();
                notify("success", `Molecule "${name}" was deleted successfully!`);
            },
            error: function() {
                notify("error", `Failed to delete molecule "${name}"`);
            }

        }).always(function() {
            button.prop("disabled", false);
            button.html(`<i class="bi bi-trash"></i> Delete `);
        });
    }
});


/* === Element List and Adding Elements Stuff === */
$(document).on("click", "#add-element", function() {
    $("#element-card-container").hide();
    resetElementForm();
    $("#ae-element-title").html("Add Element:");
    generateColours();
    $("#ae-element-container").show();
    $("#ae-element-container").css("display", "flex");
    saveOrEdit = "save";
});

$(document).on("click", "#generate-random-colour", function(e) {
    e.preventDefault();
    generateColours();
});

function generateColours() {
    tempColour1 = "#" + Math.floor(Math.random() * 16777215).toString(16);
    colours = [tempColour1, adjust(tempColour1, -90), "#000"];
    $("#input-colour-1").val(colours[0]);
    $("#input-colour-2").val(colours[1]);
    $("#input-colour-3").val(colours[2]);
    $("#gradient-colour-1").attr("stop-color", colours[0]);
    $("#gradient-colour-2").attr("stop-color", colours[1]);
    $("#gradient-colour-3").attr("stop-color", colours[2]);
}

function adjust(color, amount) {
    return "#" + color.replace(/^#/, "").replace(/../g, color => ("0" + Math.min(255, Math.max(0, parseInt(color, 16) + amount)).toString(16)).substr(-2));
}

$("#ae-element-form").change(function() {
    updateCardPreview();
});

function updateCardPreview() {
    newId = $("#input-id").val() != "" ? $("#input-id").val() : "0";
    newName = $("#input-element").val() != "" ? $("#input-element").val() : "Element Name";
    newSymbol = $("#input-symbol").val() != "" ? $("#input-symbol").val() : "Symbol";
    $("#ae-card-title-preview").html(`<b>${ newId }</b> - ${ newName } <b>(${ newSymbol })</b>`);
    $("#gradient-colour-1").attr("stop-color", $("#input-colour-1").val());
    $("#gradient-colour-2").attr("stop-color", $("#input-colour-2").val());
    $("#gradient-colour-3").attr("stop-color", $("#input-colour-3").val());
    newRadius = $("#input-radius").val() > 19 && $("#input-radius").val() < 101 ? $("#input-radius").val() : 40;
    $("#preview-radius").attr("r", newRadius);
}

$("#save-element").on("click", function(e) {
    if ($("#input-id")[0].validity.valid &&
        $("#input-symbol")[0].validity.valid &&
        $("#input-element")[0].validity.valid &&
        $("#input-colour-1")[0].validity.valid &&
        $("#input-colour-2")[0].validity.valid &&
        $("#input-colour-3")[0].validity.valid &&
        $("#input-radius")[0].validity.valid) {

        e.preventDefault();
        $("#save-element").prop("disabled", true);
        $("#save-element").html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Save`);

        let newElementData = {
            oldSymbol: $(this).attr("name"),
            id: $("#input-id").val(),
            symbol: $("#input-symbol").val(),
            element: $("#input-element").val(),
            colour1: $("#input-colour-1").val().replace("#", ""),
            colour2: $("#input-colour-2").val().replace("#", ""),
            colour3: $("#input-colour-3").val().replace("#", ""),
            radius: $("#input-radius").val()
        }

        let postRequestUrl = "";
        let successMessage = "";
        if (saveOrEdit == "save") {
            postRequestUrl = "/add-element";
            successMessage = `Element "` + newElementData["symbol"] + `" was added successfully!`;
        } else {
            postRequestUrl = "/edit-element";
            successMessage = `Element "` + newElementData["symbol"] + `" was edited successfully!`;
        }
        $.ajax({
            type: "POST",
            url: postRequestUrl,
            data: JSON.stringify(newElementData),

            statusCode: {
                200: function() {
                    updateElementList();
                    resetElementForm();
                    $("#ae-element-container").hide();
                    $("#element-card-container").show();
                    notify("success", successMessage);
                },
                409: function(response) {
                    notify("error", "Element with the " + response.responseText + " already exists in the database!");
                },
            }
        }).always(function() {
            $("#save-element").prop("disabled", false);
            $("#save-element").html("Save");
        });;
    }
});

$(document).on("click", "#edit-element", function() {
    let elementIndex = 0;
    for (let i = 0; i < elementsList.length; i++) {
        if (elementsList[i].symbol == $(this).attr("name")) {
            elementIndex = i;
            break;
        }
    }

    $("#element-card-container").hide();
    $("#ae-element-title").html("Edit Element:");
    $("#input-id").val(elementsList[elementIndex].number);
    $("#input-symbol").val(elementsList[elementIndex].symbol);
    $("#input-element").val(elementsList[elementIndex].name);
    $("#input-colour-1").val("#" + elementsList[elementIndex].c1);
    $("#input-colour-2").val("#" + elementsList[elementIndex].c2);
    $("#input-colour-3").val("#" + elementsList[elementIndex].c3);
    $("#input-radius").val(elementsList[elementIndex].r);
    $("#save-element").attr("name", elementsList[elementIndex].symbol);
    updateCardPreview();
    $("#ae-element-container").show();
    $("#ae-element-container").css("display", "flex");
    saveOrEdit = "edit";
});

$(document).on("click", "#delete-element", function() {
    let button = $(this);
    let name = button.attr("name");
    if (confirm(`Are you sure you want to delete element "${name}"?`)) {
        button.prop("disabled", true);
        button.html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Delete`);
        $.ajax({
            type: "POST",
            url: "/delete-element",
            data: name,

            success: function() {
                updateMoleculeList();
                updateElementList();
                $("#add-element").show();
                notify("success", `Element "${name}" was deleted successfully!`)
            },
            error: function() {
                notify("error", `Failed to deleted element "${name}"`)
            }

        }).always(function() {
            button.prop("disabled", false);
            button.html(`<i class="bi bi-trash"></i> Delete `);
        });
    }
});

$("#cancel-element").on("click", function(e) {
    e.preventDefault();
    resetElementForm();
    saveOrEdit = "";
    $("#ae-element-container").hide();
    $("#element-card-container").show();
});

function resetElementForm() {
    $("#input-id").val("");
    $("#input-symbol").val("");
    $("#input-element").val("");
    $("#ae-card-title-preview").html("<b>0</b> - Element Name <b>(Symbol)</b>")
    $("#input-radius").val(40);
    $("#preview-radius").attr("r", 40);
    $("#save-element").attr("name", "null")
}


/* === Settings Modal Stuff === */
function updateSvgMode() {
    $.ajax({
        type: "POST",
        url: "/get-svg-mode",

        success: function(response) {
            svgMode = parseInt(response);
            cardId = "#svg-mode-card-" + svgMode;
            cardBody = cardId + "-body"
            $(".border-primary").removeClass("border-primary");
            $(".card-glow").removeClass("card-glow");
            $(".text-primary").removeClass("text-primary");
            $("#selected-card-footer").remove();
            $(cardId).addClass("border-primary");
            $(cardId).addClass("card-glow");
            $(cardBody).addClass("text-primary");
            $(cardId).append(`<div id="selected-card-footer" class="card-footer bg-transparent border-primary text-primary text-center fw-bold">Selected!</div>`);
            removeMolecule();
        }
    });
}

$(".clickable-card").on("click", function(e) {
    e.preventDefault();
    let newMode = parseInt($(this).attr("name"));
    let modeChange = "";
    if (newMode == 1) modeChange = "New Nightmare Mode";
    if (newMode == 2) modeChange = "Old Nightmare Mode";
    if (newMode == 3) modeChange = "Original Mode";
    if (svgMode != newMode && confirm(`Are you sure you want to change the SVG mode to "${modeChange}"?\nIf you are currently viewing a molecule, the view will be closed.`)) {

        $.ajax({
            type: "POST",
            url: "/change-svg-mode",
            data: $(this).attr("name"),

            success: function() {
                removeMolecule();
                updateSvgMode();
                updateMoleculeList();
                notify("success", "SVG Mode was changed successfully!");
            },
            error: function() {
                notify("error", "Failed to change the SVG Mode");
            }
        });
    }
});

$("#reset-elements").on("click", function(e) {
    settingsDeleteButtons(e, $(this), "reset the elements list", "/reset-elements", "Elements list was reset successfully!", "Failed to reset the elements list.");
});

$("#delete-all-elements").on("click", function(e) {
    settingsDeleteButtons(e, $(this), "delete all stored elements", "/delete-all-elements", "Elements list was deleted successfully!", "Failed to delete the elements list.");
});

$("#delete-all-molecules").on("click", function(e) {
    settingsDeleteButtons(e, $(this), "delete all stored molecules", "/delete-all-molecules", "Molecules list was deleted successfully!", "Failed to delete the molecules list.");
});

function settingsDeleteButtons(e, button, message, postUrl, successMessage, errorMessage) {
    e.preventDefault();
    if (confirm(`Are you sure you want to ${message}?\nIf you are currently viewing a molecule, the view will be closed.`)) {
        button.prop("disabled", true);
        button.html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> ${button[0].innerText}`);
        $.ajax({
            type: "POST",
            url: postUrl,

            success: function() {
                removeMolecule();
                updateMoleculeList();
                updateElementList();
                notify("success", successMessage);
            },
            error: function() {
                notify("error", errorMessage)
            }

        }).always(function() {
            button.prop("disabled", false);
            button.html(button[0].innerText);
        });
    }
}


/* === Helper functions for Updating Tables === */
function getMoleculeListContent(ml) {
    htmlContent = "";
    currentCardSplit = window.screen.width >= 1320 ? 3 : window.screen.width >= 850 ? 2 : 1;
    for (let i = 0; i < ml.length; i++) {
        if (currentCardSplit != 1 && (i == 0 || (i != 0 && (i + 1) % currentCardSplit == 1))) {
            htmlContent += `<div class="row">\n`;
        }
        let tempDiv = document.createElement("div");
        tempDiv.innerHTML = ml[i].svg;
        document.body.insertAdjacentElement("beforeend", tempDiv);
        let tempSVG = tempDiv.querySelector("svg");
        let bbox = tempSVG.getBBox();
        tempSVG.setAttribute("viewBox", [bbox.x, bbox.y, bbox.width, bbox.height].join(" "));
        url = "data:image/svg+xml;charset=utf-8," + encodeURIComponent(new XMLSerializer().serializeToString(tempSVG));
        tempDiv.remove();

        htmlContent += `
        <div class="col-${12 / currentCardSplit} molecule-card-column">
            <div class="card flex-row flex-wrap h-100">
                <div class="d-flex w-100">
                    <div class="card-header molecule-card-header border-0">
                        <img src="${url}" class="molecule-card-img" alt="Molecule Image Preview">
                    </div>
                    <div class="card-body px-2">
                        <h5 class="card-title fw-bold">${ml[i].name}</h5>
                        <p class="card-text"><b>ID:</b> ${ml[i].id}<br/><b>Number of Atoms:</b> ${ml[i].atom_count}<br/><b>Number of Bonds:</b> ${ml[i].bond_count}</p>
                    </div>
                </div>
                <div class="card-buttons card-footer w-100 text-muted">
                    <button name=${ml[i].name} class="btn btn-primary view-molecule"><i class="bi bi-search"></i> View </button>
                    <button name=${ml[i].name} class="btn btn-warning edit-molecule"><i class="bi bi-pencil"></i> Edit Name </button>
                    <button name=${ml[i].name} class="btn btn-danger delete-molecule"><i class="bi bi-trash"></i> Delete </button>
                </div>
            </div>
        </div>\n`

        if (currentCardSplit != 1 && (i != 0 && (i + 1) % currentCardSplit == 0)) {
            htmlContent += "</div>\n";
        }
    }
    htmlContent += "</div>";
    return htmlContent;
}

$(window).on("resize", function() {
    updateMoleculeList2();
    updateElementList2();
});

$("#filter-list").keyup(function() {
    $("#molecule-card-container").html(filterMoleculeList($("#filter-list").val()));
});

$("#modal-filter-list").keyup(function() {
    $("#modal-molecule-card-container").html(filterMoleculeList($("#modal-filter-list").val()));
});

function filterMoleculeList(value) {
    let filteredMols = moleculesList.filter((mol) => {
        return mol.name.toUpperCase().includes(value.toUpperCase());
    });
    if (filteredMols.length == 0) {
        htmlContent = `<div class="text-center">
                            <p style="font-size:20px; margin-top:20px;">There are no molecules in the database that contain the keyword "${value}"!</p>
                        </div>`;
    } else {
        htmlContent = getMoleculeListContent(filteredMols);
    }
    return htmlContent;
}

function updateMoleculeList() {
    $.ajax({
        type: "GET",
        url: "/molecule-list.html",

        success: function(response) {
            moleculesList = JSON.parse(response);
            updateMoleculeList2(moleculesList);
        },
        error: function() {
            notify("error", "Failed to retrieve the Molecules List data.");
        }
    });
}

function updateMoleculeList2() {
    htmlContent = "";
    if (moleculesList.length == 0) {
        htmlContent = `<div class="text-center">
                            <p style="font-size:20px; margin-top:20px;">There are no molecules in the database!</p>
                            <p style="font-size:20px;">Feel free to add some using the buttons above.</p>
                            <p style="font-size:10px;">...or don't. I'm not the boss of you...</p>
                        </div>`;
        $("#modal-molecule-card-container").html(`<div class="text-center">
                                                        <p style="font-size:20px; margin-top:20px;">There are no molecules in the database!</p>
                                                        <p style="font-size:20px;">Feel free to add some from the home page.</p>
                                                        <p style="font-size:10px;">...or don't. I'm not the boss of you...</p>
                                                    </div>`);
        $("#filter-div").hide();
        $("#modal-filter-div").hide();
    } else {
        htmlContent += getMoleculeListContent(moleculesList);
        $("#filter-div").show();
        $("#modal-filter-div").show();
        $("#modal-molecule-card-container").html(htmlContent);
    }
    $("#molecule-card-container").html(htmlContent);
    $("#filter-list").val("");
    $("#modal-filter-list").val("");
}

function updateElementList() {
    $.ajax({
        type: "GET",
        url: "/element-list.html",

        success: function(response) {
            elementsList = JSON.parse(response);
            updateElementList2();
        },
        error: function() {
            notify("error", "Failed to retrieve the Elements List data.");
        }

    });
}

function updateElementList2() {
    htmlContent = "";
    if (elementsList.length == 0) {
        htmlContent += `<div class="text-center">
                            <p style="font-size:20px; margin-top:20px;">There are no elements in the database!</p>
                            <p style="font-size:20px;">You can add some using the button below!</p>
                        </div>`;
    } else {
        currentCardSplit = window.screen.width >= 1645 ? 5 : window.screen.width >= 1332 ? 4 : window.screen.width >= 1042 ? 3 : window.screen.width >= 800 ? 2 : 1;
        for (let i = 0; i < elementsList.length; i++) {
            if (currentCardSplit != 1 && (i == 0 || (i != 0 && (i + 1) % currentCardSplit == 1))) {
                htmlContent += `<div class="row">\n`;
            }

            htmlContent += `
            <div class="col element-card-col">
                <div class="card h-100">
                    <div class="card-header text-center">
                        <h5 class="card-title text-nowrap" 
                        style="font-size: ${ 
                            (elementsList[i].number.toString().length + 3 + elementsList[i].name.length + 3 + elementsList[i].symbol.length) > 23 ? "0.9rem" : 
                            (elementsList[i].number.toString().length + 3 + elementsList[i].name.length + 3 + elementsList[i].symbol.length) > 21 ? "1rem" :
                            (elementsList[i].number.toString().length + 3 + elementsList[i].name.length + 3 + elementsList[i].symbol.length) > 18 ? "1.2rem" : "1.25rem"
                        }">
                            <b>${elementsList[i].number} ${elementsList[i].number == 0 ? "(Default)" : ""}</b> - 
                            ${elementsList[i].number == 0 ? "?" : elementsList[i].name} 
                            <b>(${elementsList[i].symbol})</b>
                        </h5>
                    </div>
                    <img class="card-img">${elementsList[i].svg}</img>
                    <div class="card-body">
                        <div class="card-buttons d-flex justify-content-evenly">
                            <button type="submit" name=${elementsList[i].symbol} id="edit-element" class="btn btn-warning"><i class="bi bi-pencil"></i> Edit </button>
                            <button type="submit" name=${elementsList[i].symbol} id="delete-element" class="btn btn-danger"><i class="bi bi-trash"></i> Delete </button>
                        </div>
                    </div>
                </div>
            </div>\n`;

            if (currentCardSplit != 1 && (i == elementsList.length - 1 && (i + 1) % currentCardSplit != 0)) {
                htmlContent += `
                    <div class="col">
                        <button id="add-element" class="btn btn-lg add-row-wrap h-100 m-0"><i class="bi bi-plus-circle"></i> Add Element </button>
                    </div>
                `;
                for (let j = 0; j < (currentCardSplit - ((i + 1) % currentCardSplit)) - 1; i++) {
                    htmlContent += `<div class="col"></div>`;
                }
            }

            if (currentCardSplit != 1 && (i != 0 && (i + 1) % currentCardSplit == 0)) {
                htmlContent += "</div>\n";
            }
        }
        htmlContent += "</div>";
    }
    if (elementsList.length % currentCardSplit == 0) {
        htmlContent += `<button id="add-element" class="btn btn-lg add-row-wrap"><i class="bi bi-plus-circle"></i> Add Element </button>`;
    }
    $("#element-card-container").html(htmlContent);
}


/* === Helper function for rotating. Includes Sliders. === */
rotationData = {}

function getRotations(moleculeName) {
    $("#rotation-options-loading").show();
    $("#rotation-options-div").hide();
    $.ajax({
        type: "POST",
        url: "/get-rotations",
        data: moleculeName,

        success: function(response) {
            if (response) {
                rotationData = JSON.parse(response);
                $("#rotation-options-loading").hide();
                $("#rotation-options-div").css("display", "flex");
            }
        },
        error: function() {
            notify("error", "Failed to get the molecule's rotation");
        }

    });
}

function rotateMolecule(dimension, degrees) {
    if (rotationData != null) {
        moleculeName = $(".molecule-name").val();
        $(".svg-box").children().replaceWith(rotationData[dimension][degrees]);
        setSVGbox();
    }
}

async function spinMolecule() {
    if (rotationData != null) {
        $("#spin-molecule").attr("disabled", true);
        $("#reset-rotations").attr("disabled", true);
        $("#x-slider").data("roundSlider").disable();
        $("#y-slider").data("roundSlider").disable();
        $("#z-slider").data("roundSlider").disable();
        moleculeName = $("#molecule-name").attr("name");

        for (let i = 0; i < 360; i++){
            setTimeout(() => {  
                $(".svg-box").children().replaceWith(rotationData["x"][i]);
                setSVGbox();
            }, i * 7.5); 
        }
        await new Promise(r => setTimeout(r, 360 * 7.5));
        for (let i = 0; i < 360; i++){
            setTimeout(() => {  
                $(".svg-box").children().replaceWith(rotationData["y"][i]);
                setSVGbox();
            }, i * 7.5);
        }
        await new Promise(r => setTimeout(r, 360 * 7.5));
        for (let i = 0; i < 360; i++){
            setTimeout(() => {  
                $(".svg-box").children().replaceWith(rotationData["z"][i]);
                setSVGbox();
            }, i * 7.5);
        }

        await new Promise(r => setTimeout(r, 360 * 7.5));

        resetRotations();
        $("#spin-molecule").attr("disabled", false);
        $("#reset-rotations").attr("disabled", false);
        $("#x-slider").data("roundSlider").enable();
        $("#y-slider").data("roundSlider").enable();
        $("#z-slider").data("roundSlider").enable();
    }
}

function resetSliders() {
    $("#x-slider").roundSlider("setValue", 0);
    $("#y-slider").roundSlider("setValue", 0);
    $("#z-slider").roundSlider("setValue", 0);
}

function resetRotations() {
    resetSliders();
    $(".svg-box").children().replaceWith(rotationData["x"][0]);
    setSVGbox();
}

$("#x-slider").roundSlider({
    sliderType: "min-range", handleShape: "round", min: 0, max: 360, step: 1, value: 0, width: 22, radius: 100, startAngle: 0, endAngle: "+360", animation: true, showTooltip: true, editableTooltip: false,
    tooltipFormat: ({ value: val }) => `<div class="slider-content"><span class="slider-text">X = ${val +"°"}</span></div>`,
    update: function(e) {
        $("#y-slider").roundSlider("setValue", 0);
        $("#z-slider").roundSlider("setValue", 0);
        rotateMolecule("x", e.value);
    }
});

$("#y-slider").roundSlider({
    sliderType: "min-range", handleShape: "round", min: 0, max: 360, step: 1, value: 0, width: 22, radius: 100, startAngle: 0, endAngle: "+360", animation: true, showTooltip: true, editableTooltip: false,
    tooltipFormat: ({ value: val }) => `<div class="slider-content"><span class="slider-text">Y = ${val +"°"}</span></div>`,
    update: function(e) {
        $("#x-slider").roundSlider("setValue", 0);
        $("#z-slider").roundSlider("setValue", 0);
        rotateMolecule("y", e.value);
    }
});

$("#z-slider").roundSlider({
    sliderType: "min-range", handleShape: "round", min: 0, max: 360, step: 1, value: 0, width: 22, radius: 100, startAngle: 0, endAngle: "+360", animation: true, showTooltip: true, editableTooltip: false,
    tooltipFormat: ({ value: val }) => `<div class="slider-content"><span class="slider-text">Z = ${val +"°"}</span></div>`,
    update: function(e) {
        $("#x-slider").roundSlider("setValue", 0);
        $("#y-slider").roundSlider("setValue", 0);
        rotateMolecule("z", e.value);
    }
});


/* === Helper functions for SVG === */
function setSVGbox() {
    let svg = document.getElementById("svg-box").querySelector("svg");
    let bbox = svg.getBBox();
    let viewBox = [(bbox.x - (($(".svg-box").width() - bbox.width) / 2)),
        (bbox.y - (($(".svg-box").height() - bbox.height) / 2)),
        $(".svg-box").width(),
        $(".svg-box").height()
    ].join(" ");
    svg.setAttribute("viewBox", viewBox);
    setPanZoom();
}

function setPanZoom() {
    let svg = document.getElementById("svg-box").querySelector("svg");
    svgPanZoom(svg, { zoomEnabled: true, controlIconsEnabled: true, fit: true, center: true });
}



/* === Helper function for notifications === */
function notify(type, message) {
    (() => {

        // Show the notification area before creating a new notification
        $("#notification-area").show();
        let n = document.createElement("div");
        let id = Math.random().toString(36).substring(2, 10);
        n.setAttribute("id", id);
        n.classList.add("notification", type);

        // Set the message
        n.innerHTML = `<h6 class="m-0 fw-600">` + type.toUpperCase() + `:</h6><hr style="margin: 10px 0px; opacity: 1"/><p class="m-0">` + message + `</p>`;
        document.getElementById("notification-area").appendChild(n);

        // Fade in the notification
        setTimeout(() => {
            $(".notification").css("opacity", 1);
            $(".notification").css("left", 0);
        }, 300);

        //This part handles removing the notification from the list
        setTimeout(() => {
            var notifications = document.getElementById("notification-area").getElementsByClassName("notification");
            for (let i = 0; i < notifications.length; i++) {
                if (notifications != null && notifications[i].getAttribute("id") == id) {
                    notifications[i].style.opacity = 0;
                    notifications[i].style.left = 20;
                    setTimeout(() => {
                        notifications[i].remove();
                    }, 400);
                    break;
                }
            }

            // Hide the notification once all notifications are done.
            setTimeout(() => {
                if (notifications.length == 0) {
                    $("#notification-area").hide();
                }
            }, 400);
        }, 5000);
    })();
}