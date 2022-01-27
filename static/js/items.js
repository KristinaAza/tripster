// Adding item

// document.querySelector("#open-add-form").addEventListener("click", () => {   
//     document.querySelector("#add-item").setAttribute("style", "visibility:visible;");
// })


// function render_item_id(element, id) {
//     element.parentElement.insertAdjacentHTML('beforeend', `<div>${id}</div>`);
// }

function submitForm(element) {
    const saveButton = element;
    const modalFooterDiv = element.parentElement;
    const modalContentDiv = element.parentElement.parentElement;
    const form = element.parentElement.parentElement.querySelector('.modal-body form');

    form.submit();
}