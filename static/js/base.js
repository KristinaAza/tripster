// A functon that is called on "click" event of "Cancel" button for closing the form

function close_form(element) {
    element.parentElement.setAttribute("style", "display:none;");
}

function submitForm(element) {
    const saveButton = element;
    const modalFooterDiv = element.parentElement;
    const modalContentDiv = element.parentElement.parentElement;
    const form = element.parentElement.parentElement.querySelector('.modal-body form');

    form.submit();
}
