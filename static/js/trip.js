function openAddForm(element) {
    element.parentElement.querySelector('.add-item').setAttribute("style", "visibility:visible;");
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
        const style = checkedStatus ? "text-decoration:line-through;" : "text-decoration:none;";
        parent.querySelector('span').setAttribute("style", style);
    })
}


// function toggleStrikethrough(element, id) {
//      const checkedStatus = changeChecked(id);

//      const parent = element.parentElement;
//      const style = checkedStatus ? "text-decoration:line-through;" : "text-decoration:none;";
//      console.log(checkedStatus);
//      console.log(style);
    
//      // const parentStyle = parent.getAttribute('style');
//      // const style = (parentStyle === "text-decoration:line-through;") ? "text-decoration:none;" : "text-decoration:line-through;";
//      parent.setAttribute("style", style);

// }

