//  Adding a category

document.querySelector("#open-add-form").addEventListener("click", () => {   
    document.querySelector("#add-category").setAttribute("style", "visibility:visible;");
})

document.querySelector("#add-category").addEventListener("submit", evt => {
    evt.preventDefault();

    document.querySelector("#add-category").setAttribute("style", "visibility:hidden;");

    const name = document.querySelector("#name-field").value;
    document.getElementById("add-category").reset();
    // document.getElementById("add-category").value = ''; doesn't clear the input box

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
        categoryElement.innerHTML= `<a id="link-${categoryAdded.id}" href="/categories/${categoryAdded.id}">${categoryAdded.name}</a><input id="id-field-${categoryAdded.id}" class="form-control" value="${categoryAdded.id}" type="hidden" name="id"> <button id="open-edit-form-${categoryAdded.id}" class="edit-button" onclick="">Edit</button> <form id="form-${categoryAdded.id}" class="edit-category" style="visibility:hidden;" method="POST" action="/category"> <label for="name-field">Name</label> <input id="name-${categoryAdded.id}-field" class="form-control" type="text" name="name" placeholder="${categoryAdded.id}" value="${categoryAdded.id}"> <input type="submit" value="Save" class="btn btn-primary"> </form>`;
        document.querySelector('#categories').append(categoryElement);
        document.querySelector(`#name-${categoryAdded.id}-field`).value = `${categoryAdded.name}`
        createEventListenersToEditCategory();
    })
})


// TODO: Find a different way to pass category id from html page to js 


//  Editting a category

function createEventListenersToEditCategory() {
    const editButtons = document.querySelectorAll(".edit-button");
    console.log(editButtons);

    for (const editButton of editButtons) {

        const id = editButton.id[editButton.id.length - 1];

        editButton.addEventListener("click", () => {   
            document.querySelector(`#form-${id}`).setAttribute("style", "visibility:visible;");
        })
    }

    const editForms = document.querySelectorAll(".edit-category");

    for (const form of editForms) {

        form.addEventListener("submit", evt => {
            evt.preventDefault();
            
            const id = form.id[form.id.length - 1];
            // const id = document.querySelector(`#id-field-${id}`).value;

            document.querySelector(`#form-${id}`).setAttribute("style", "visibility:hidden;");
            
            
            const name = document.querySelector(`#name-${id}-field`).value;
            // document.getElementById(`#form-${id}`).reset();
            
            fetch('/api/edit_category', {
                method: 'POST',
                body: JSON.stringify({id, name}),
                headers: {
                    'Content-Type': 'application/json',
                },
            })
            .then(response => response.json())
            .then(responseJson => {
                const name = responseJson.name;
                
                document.querySelector(`#link-${id}`).innerHTML = `${name}`;
            })
        })
    }
}

createEventListenersToEditCategory();