const fromText = document.querySelector(".from-text"),
toText = document.querySelector(".to-text"),
exchageIcon = document.querySelector(".exchange"),
selectTag = document.querySelectorAll("select"),
icons = document.querySelectorAll(".row i");
translateBtn = document.querySelector("button"),

selectTag.forEach((tag, id) => {
    for (let country_code in countries) {
        let selected = id == 0 ? country_code == "sw" ? "selected" : "" : country_code == "lu" ? "selected" : "";
        let option = `<option ${selected} value="${country_code}">${countries[country_code]}</option>`;
        tag.insertAdjacentHTML("beforeend", option);
    }
});

exchageIcon.addEventListener("click", () => {
    let tempText = fromText.value,
    tempLang = selectTag[0].value;
    fromText.value = toText.value;
    toText.value = tempText;
    selectTag[0].value = selectTag[1].value;
    selectTag[1].value = tempLang;
});

fromText.addEventListener("keyup", () => {
    if(!fromText.value) {
        toText.value = "";
    }
});

translateBtn.addEventListener("click", () => {
    // Get input values from HTML elements
    let text = document.getElementById("fromText").value.trim(),
    translateFrom = document.getElementById("selectTag").options[0].value,
    translateTo = document.getElementById("selectTag").options[1].value;
    if (!text) return;
    document.getElementById("toText").setAttribute("placeholder", "Translating...");

    // Build API URL
    let apiUrl = '/translate';  // Change this to your Flask route

    // Prepare data for POST request
    let data = {
        source_text: text,
        translated_text: '',  // You can update this based on your use case
    };

    // Fetch data from the Flask server
    fetch(apiUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("toText").value = data.translated_text;
        document.getElementById("toText").setAttribute("placeholder", "Translation");
    })
    .catch(error => console.error('Error:', error));
});

