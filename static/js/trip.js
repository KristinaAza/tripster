function openAddForm(element) {
    element.parentElement.querySelector('.add-item').setAttribute("style", "display:block;");
}

function changeChecked(element, id) {
    let checkedStatus;

    fetch('/api/trip_item', {
        method: 'POST',
        body: JSON.stringify({id}),
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(responseJson => {
        checkedStatus = responseJson.checkedStatus;
        const parent = element.parentElement;
        const style = checkedStatus ? "text-decoration:line-through; display:inline;" : "text-decoration:none; display:inline;";
        parent.querySelector('span').setAttribute("style", style);
        
        if (style === "text-decoration:line-through; display:inline;") {
            parent.querySelector('span').classList.add('hide');
            element.classList.add('hide');
        } else {
            parent.querySelector('span').classList.remove('hide');
            element.classList.remove('hide');
        }
        console.log("changeChecked is done running")
    })
}

function toggle(button) {
    const text = button.innerText;
    button.innerText = text === "Show All Items" ? "Hide checked out items" : "Show All Items";

    const items_to_hide = document.querySelectorAll(".hide");
    for (const item of items_to_hide) {
        item.style.display = (item.style.display === "inline") ? "none" : "inline";
    }
}
