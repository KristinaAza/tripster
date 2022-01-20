// Adding template

document.querySelector("#open-add-form").addEventListener("click", () => {   
    document.querySelector("#add-template").setAttribute("style", "visibility:visible;");
})

function openAddForm(element) {
    element.parentElement.querySelector('.create-trip').setAttribute("style", "visibility:visible;");
}