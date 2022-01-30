function submitForm(element) {
    const saveButton = element;
    const modalFooterDiv = element.parentElement;
    const modalContentDiv = element.parentElement.parentElement;
    const form = element.parentElement.parentElement.querySelector('.modal-body form');

    form.submit();
}

function deleteItem(element, item_id) {
    fetch('/api/items/delete', {
        method: 'POST',
        body: JSON.stringify({item_id}),
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(responseJson => {
        const itemListElement = element.parentElement;
        itemListElement.remove();
    })
}