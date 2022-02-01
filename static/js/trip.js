
function edit(saveButton, trip_id) {
    const name = saveButton.parentElement.parentElement.querySelector('#name-field').value;
    const date = saveButton.parentElement.parentElement.querySelector('#date-field').value;

    fetch('/api/edit_trip', {
        method: 'POST',
        body: JSON.stringify({trip_id, name, date}),
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(responseJson => {
        const name = responseJson.name;
        let tripDate = new Date(responseJson.trip_date);
        tripDate = tripDate.toISOString().split('T')[0];

        document.querySelector('h2 span').innerHTML = `${name} Trip ${tripDate}`;
        document.querySelector('title').innerText = `${name} Trip`;
        document.querySelector('nav .active').innerText = `${name} Trip`;

    })
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
            parent.querySelector('#delete').classList.add('hide');
            parent.querySelector('#edit').classList.add('hide');
            parent.querySelector('#delete').setAttribute('disabled', '');
            parent.querySelector('#edit').setAttribute('disabled', '');
        
        
        } else {
            parent.querySelector('span').classList.remove('hide');
            element.classList.remove('hide');
            parent.querySelector('#delete').classList.remove('hide');
            parent.querySelector('#edit').classList.remove('hide');
            parent.querySelector('#delete').removeAttribute('disabled');
            parent.querySelector('#edit').removeAttribute('disabled');
        }
    })
}

function toggle(checkbox) { 
    const items_to_hide = document.querySelectorAll(".hide");
    for (const item of items_to_hide) {
        item.style.display = (item.style.display === "inline") ? "none" : "inline";
    }
}

function deleteTripItem(element, trip_item_id) {
    fetch('/api/trip_items/delete', {
        method: 'POST',
        body: JSON.stringify({trip_item_id}),
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(responseJson => {
        
        console.log(responseJson.status);

        const tripItemElement = element.parentElement;
        tripItemElement.remove();
    })
}

function send_email(send_email_button, trip_id) {

    const email = document.querySelector("#email-field").value;

    fetch('/api/trips/send_email', {
        method: 'POST',
        body: JSON.stringify({trip_id, email}),
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(responseJson => {
        
        console.log(responseJson.status);
    })   
}