// Adding item

document.querySelector("#open-add-form").addEventListener("click", () => {   
    document.querySelector("#add-category").setAttribute("style", "visibility:visible;");
})


function render_item_id(element, id) {
    element.parentElement.insertAdjacentHTML('beforeend', `<div>${id}</div>`);
}
