/* VISUAL FONT AWESOME ICON PICKER | ENGLISH ONLY */
(function () {
    "use strict";
    function norm(text) {
        var s = String(text || "").toLowerCase();
        if (s.normalize) s = s.normalize("NFD").replace(/[\u0300-\u036f]/g, "");
        return s.trim();
    }
    function start(root) {
        if (root.dataset.vvFaReady === "1" || root.closest(".empty-form")) return;
        var field = root.querySelector("[data-vv-fa-value]");
        var preview = root.querySelector("[data-vv-fa-preview]");
        var current = root.querySelector("[data-vv-fa-current]");
        var toggle = root.querySelector("[data-vv-fa-toggle]");
        var panel = root.querySelector("[data-vv-fa-panel]");
        var search = root.querySelector("[data-vv-fa-search]");
        var filters = Array.from(root.querySelectorAll("[data-vv-fa-category]"));
        var options = Array.from(root.querySelectorAll("[data-vv-fa-option]"));
        var empty = root.querySelector("[data-vv-fa-empty]");
        var clear = root.querySelector("[data-vv-fa-clear]");
        if (!field || !preview || !current || !toggle || !panel || !search) return;
        root.dataset.vvFaReady = "1";
        var category = "all";
        function refresh() {
            var value = field.value.trim();
            preview.className = value || "fa-solid fa-icons";
            current.textContent = value || "None";
            options.forEach(function (button) {
                var active = button.dataset.vvFaIcon === value;
                button.classList.toggle("is-selected", active);
                button.setAttribute("aria-pressed", active ? "true" : "false");
            });
        }
        function filter() {
            var text = norm(search.value), shown = 0;
            options.forEach(function (button) {
                var groupOk = category === "all" || button.dataset.vvFaGroup === category;
                var textOk = !text || norm(button.dataset.vvFaTerms).indexOf(text) !== -1;
                var show = groupOk && textOk;
                button.hidden = !show;
                if (show) shown++;
            });
            if (empty) empty.hidden = shown > 0;
        }
        function open(state) {
            panel.hidden = !state;
            toggle.setAttribute("aria-expanded", state ? "true" : "false");
            toggle.textContent = state ? "Close" : "Choose icon";
            if (state) { filter(); search.focus(); }
        }
        toggle.addEventListener("click", function () { open(panel.hidden); });
        search.addEventListener("input", filter);
        search.addEventListener("keydown", function (event) {
            if (event.key !== "Enter") return;
            event.preventDefault();
            var first = options.find(function (button) { return !button.hidden; });
            if (first) first.click();
        });
        filters.forEach(function (button) {
            button.addEventListener("click", function () {
                category = button.dataset.vvFaCategory;
                filters.forEach(function (other) {
                    var active = other === button;
                    other.classList.toggle("is-active", active);
                    other.setAttribute("aria-pressed", active ? "true" : "false");
                });
                filter();
            });
        });
        options.forEach(function (button) {
            button.addEventListener("click", function () {
                field.value = button.dataset.vvFaIcon;
                field.dispatchEvent(new Event("input", { bubbles: true }));
                field.dispatchEvent(new Event("change", { bubbles: true }));
                refresh();
                open(false);
            });
        });
        field.addEventListener("input", refresh);
        field.addEventListener("change", refresh);
        if (clear) clear.addEventListener("click", function () {
            field.value = "";
            field.dispatchEvent(new Event("input", { bubbles: true }));
            field.dispatchEvent(new Event("change", { bubbles: true }));
            refresh();
            open(false);
        });
        refresh();
    }
    function scan(target) {
        if (!target) return;
        if (target.matches && target.matches("[data-vv-fa-picker]")) start(target);
        if (target.querySelectorAll) target.querySelectorAll("[data-vv-fa-picker]").forEach(start);
    }
    function boot() {
        scan(document);
        document.addEventListener("formset:added", function (event) { scan(event.target); });
        if (typeof MutationObserver !== "undefined") {
            var observer = new MutationObserver(function (changes) {
                changes.forEach(function (change) {
                    change.addedNodes.forEach(function (node) { if (node.nodeType === 1) scan(node); });
                });
            });
            observer.observe(document.body, { childList: true, subtree: true });
        }
    }
    if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot);
    else boot();
})();
