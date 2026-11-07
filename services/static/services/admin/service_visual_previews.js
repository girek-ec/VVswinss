// SERVICES · NEW IMAGE PREVIEWS | PREVISUALIZACIÓN ANTES DE GUARDAR
(function () {
    "use strict";
    document.addEventListener("DOMContentLoaded", function () {
        ["category_default_image", "cta_background", "work_method_image", "social_default_image"].forEach(function (field) {
            const input = document.getElementById("id_" + field);
            const preview = document.getElementById("vv-services-preview-" + field);
            if (!input || !preview) return;
            let currentObjectUrl = null;
            let newCard = null;
            function clearNewCard() {
                if (newCard) newCard.remove();
                newCard = null;
                if (currentObjectUrl) URL.revokeObjectURL(currentObjectUrl);
                currentObjectUrl = null;
            }
            input.addEventListener("change", function () {
                clearNewCard();
                if (!input.files || !input.files.length) return;
                const file = input.files[0];
                if (!file.type.startsWith("image/")) return;
                currentObjectUrl = URL.createObjectURL(file);
                newCard = document.createElement("div");
                newCard.style.cssText = "display:inline-flex;flex-direction:column;gap:5px;max-width:240px";
                const image = document.createElement("img");
                image.src = currentObjectUrl;
                image.alt = "New selected image";
                image.style.cssText = "width:220px;height:135px;object-fit:cover;border:2px solid #3a7cad;border-radius:6px";
                const title = document.createElement("strong");
                title.style.fontSize = "12px";
                title.textContent = "Selected image · Not saved yet";
                const filename = document.createElement("span");
                filename.style.cssText = "font-size:11px;color:#777;overflow-wrap:anywhere";
                filename.textContent = file.name;
                newCard.append(image, title, filename);
                preview.insertBefore(newCard, preview.firstChild);
            });
            const clearCheck = document.getElementById(field + "-clear_id");
            if (clearCheck) clearCheck.addEventListener("change", function () {
                if (clearCheck.checked) clearNewCard();
            });
            window.addEventListener("pagehide", clearNewCard, {once: true});
        });
    });
})();
