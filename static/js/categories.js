"use strict";

function editCategory(saveButton, category_id) {
    const name = document.querySelector(`#name-${category_id}-field`).value;
    fetch('/api/edit_category', {
        method: 'POST',
        body: JSON.stringify({category_id, name}),
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(responseJson => {
        const name = responseJson.name;
        
        document.querySelector(`#category-${category_id}`).innerHTML = `${name}`;
    })
}


function deleteCategory(element, category_id) {
    fetch('/api/categories/delete', {
        method: 'POST',
        body: JSON.stringify({category_id}),
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(responseJson => {

        console.log(responseJson.status);

        const categoryElement = element.parentElement;
        categoryElement.remove();
    })
}
