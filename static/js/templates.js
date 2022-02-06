"use strict";

function deleteTemplate(element, template_id) {
    fetch('/api/templates/delete', {
        method: 'POST',
        body: JSON.stringify({template_id}),
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(responseJson => {
        const templateElement = element.parentElement;
        templateElement.remove();
    })
}