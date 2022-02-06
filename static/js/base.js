"use strict";

function submitForm(element) {
    const saveButton = element;
    const modalFooterDiv = element.parentElement;
    const modalContentDiv = element.parentElement.parentElement;
    const form = element.parentElement.parentElement.querySelector('.modal-body form');

    form.submit();
}
