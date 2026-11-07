// ABOUT · SELECTED IMAGE PREVIEW | ABOUT · IMAGE SELECTION PREVIEW
(function () {
    "use strict";
    const imageFields = [
        "intro_image",
        "header_background",
        "mission_primary_image",
        "mission_secondary_image",
        "vision_background",
        "vision_image",
        "projects_background"
    ];
    function init() {
        imageFields.forEach(function (field) {
            const input = document.getElementById("id_" + field);
            if (!input || input.dataset.vvAboutPreviewReady === "1") return;
            input.dataset.vvAboutPreviewReady = "1";
            const preview = document.createElement("div");
            preview.className = "vv-about-selected-preview";
            preview.hidden = true;
            input.insertAdjacentElement("afterend", preview);
            let blobUrl = null;
            function clear() {
                preview.replaceChildren();
                preview.hidden = true;
                if (blobUrl) { URL.revokeObjectURL(blobUrl); blobUrl = null; }
            }
            function show(file) {
                clear();
                if (!file || !file.type || !file.type.startsWith("image/")) return;
                blobUrl = URL.createObjectURL(file);
                const image = document.createElement("img");
                image.src = blobUrl;
                image.alt = "Selected image preview";
                image.className = "vv-about-selected-image";
                image.addEventListener("error", clear, { once: true });
                const caption = document.createElement("span");
                caption.textContent = "Selected image (not saved yet): " + file.name;
                preview.append(image, caption);
                preview.hidden = false;
            }
            input.addEventListener("change", function () {
                show(input.files && input.files[0]);
            });
            const clearCheckbox = document.getElementById(field + "-clear_id");
            if (clearCheckbox) clearCheckbox.addEventListener("change", function () {
                if (clearCheckbox.checked) clear();
            });
        });
    }
    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", init, { once: true });
    } else {
        init();
    }
})();
