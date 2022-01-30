function edit(saveButton, template_id) {
    const name = saveButton.parentElement.parentElement.querySelector('#name-field').value;
    
    fetch('/api/edit_template', {
        method: 'POST',
        body: JSON.stringify({template_id, name}),
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(responseJson => {
        const name = responseJson.name;
      
        document.querySelector('h2').innerHTML = `${name} Template`;
        document.querySelector('title').innerText = `${name} Template`;
        document.querySelector('nav .active').innerText = `${name} Template`;
    })
}

function deleteTemplateItem(element, template_id, item_id) {
    fetch('/api/template_items/delete', {
        method: 'POST',
        body: JSON.stringify({template_id, item_id}),
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(responseJson => {
        
        console.log(responseJson.status);

        const templateItemElement = element.parentElement;
        templateItemElement.remove();
    })
}