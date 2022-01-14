document.querySelector("#open-form").addEventListener("click", () => {   
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
        categoryElement.innerHTML= `<a href="/categories/${categoryAdded.id}">${categoryAdded.name}</a>`;
        document.querySelector('#categories').append(categoryElement);
    })
})
