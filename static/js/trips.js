// Adding event listener to "Add new trip" button for opening the form

document.querySelector("#open-add-form").addEventListener("click", () => {   
    document.querySelector("#add-trip").setAttribute("style", "visibility:visible;");
})
