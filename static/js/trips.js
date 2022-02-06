"use strict";

function deleteTrip(element, trip_id) {
    fetch('/api/trips/delete', {
        method: 'POST',
        body: JSON.stringify({trip_id}),
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(responseJson => {
        const tripElement = element.parentElement;
        tripElement.remove();
    })
}
