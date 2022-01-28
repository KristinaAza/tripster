//  Adding a category

document.querySelector("#add-category").addEventListener("submit", evt => {
    evt.preventDefault();

    document.querySelector("#add-category").setAttribute("style", "display:none;");

    const name = document.querySelector("#name-field").value;
    document.getElementById("add-category").reset();
 
    fetch('/api/category', {
        method: 'POST',
        body: JSON.stringify({name}),
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(responseJson => {
        const categoryAdded = responseJson.categoryAdded;
        const categoryElement = document.createElement("li");
        categoryElement.innerHTML= `<a id="link-${categoryAdded.id}" href="/categories/${categoryAdded.id}">${categoryAdded.name}</a>
                                    <input id="id-field-${categoryAdded.id}" class="form-control" value="${categoryAdded.id}" type="hidden" name="id">
                                    <button id="open-edit-form-${categoryAdded.id}" class="edit-button" onclick="">Edit</button>
                                    <form id="form-${categoryAdded.id}" class="edit-category" style="display:none;" method="POST" action="/category">
                                        <label for="name-field">Name</label>
                                        <input id="name-${categoryAdded.id}-field" class="form-control" type="text" name="name" value="${categoryAdded.id}">
                                        <input type="submit" value="Save" class="btn btn-primary">
                                        <button type="button" onclick="close_form(this)">Cancel</button>
                                    </form>`;

        const element =document.querySelector('#categories');
  
        element.insertBefore(categoryElement, element.childNodes[0] || null);
        document.querySelector(`#name-${categoryAdded.id}-field`).value = `${categoryAdded.name}`
        createEventListenersToEditCategory();
    })
})



//  Editting a category

function edit(saveButton, category_id) {
    const name = saveButton.parentElement.parentElement.querySelector('input').value;
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
        
        document.querySelector(`#link-${category_id}`).innerHTML = `${name}`;
    })
}
