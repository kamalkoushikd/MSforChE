document.addEventListener("DOMContentLoaded", function () {
    function displayCard(element) {
        const elementsData = JSON.parse(document.getElementById("elements-data").textContent);

        const atomicNumber = parseInt(element.getAttribute("data-number"));

        // Find the element in the `elements` list (which is globally available)
        const elementData = elements.find(el => el.atomic_number === atomicNumber);

        if (elementData) {
            document.getElementById("card-name").innerText = elementData.name;
            document.getElementById("card-symbol").innerText = elementData.symbol;
            document.getElementById("card-number").innerText = elementData.atomic_number;
            document.getElementById("card-mass").innerText = elementData.atomic_mass;
            document.getElementById("card-mpt").innerText = elementData.melting_point || "N/A";
            document.getElementById("card-bpt").innerText = elementData.boiling_point || "N/A";
            document.getElementById("card-en").innerText = elementData.electronegativity || "N/A";
            document.getElementById("card-ar").innerText = elementData.atomic_radius || "N/A";
            document.getElementById("card-ec").innerText = elementData.electronic_configuration || "N/A";

            document.getElementById("element-card").classList.remove("hidden");
        }
    }

    function closeCard() {
        document.getElementById("element-card").classList.add("hidden");
    }

    // Expose displayCard and closeCard globally so they can be accessed from inline HTML
    window.displayCard = displayCard;
    window.closeCard = closeCard;
});
