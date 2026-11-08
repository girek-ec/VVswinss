// CONTACT · IMMEDIATE IMAGE PREVIEWS | VISTAS PREVIAS ANTES DE GUARDAR
(function () {
    "use strict";
    document.addEventListener("DOMContentLoaded", function () {
        ["header_background", "main_image"].forEach(function (field) {
            const input = document.getElementById("id_" + field);
            const container = document.getElementById("vv-contact-preview-" + field);
            if (!input || !container) return;
            let temporaryUrl = null;
            let previewNode = null;

            function clearTemporary() {
                if (previewNode) previewNode.remove();
                previewNode = null;
                if (temporaryUrl) URL.revokeObjectURL(temporaryUrl);
                temporaryUrl = null;
            }

            input.addEventListener("change", function () {
                clearTemporary();
                const file = input.files && input.files[0];
                if (!file || !file.type.startsWith("image/")) return;
                temporaryUrl = URL.createObjectURL(file);
                previewNode = document.createElement("div");
                previewNode.style.cssText = "display:inline-flex;flex-direction:column;gap:5px;max-width:235px";
                const image = document.createElement("img");
                image.src = temporaryUrl;
                image.alt = "Selected image preview";
                image.style.cssText = "display:block;width:220px;height:140px;object-fit:cover;border:2px solid #2563eb;border-radius:7px;background:#f3f4f6";
                const title = document.createElement("strong");
                title.textContent = "Selected image · Not saved";
                title.style.fontSize = "12px";
                const filename = document.createElement("span");
                filename.textContent = file.name;
                filename.style.cssText = "font-size:11px;color:#667085;overflow-wrap:anywhere";
                previewNode.append(image, title, filename);
                container.prepend(previewNode);
            });
            window.addEventListener("pagehide", clearTemporary, {once: true});
        });
    });
})();
