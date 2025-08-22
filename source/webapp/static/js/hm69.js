async function makeRequest(url, method = 'GET', data=null) {
    let headers = {};
    if (method !== 'GET') {
        const csrftoken = getCookie('csrftoken');
        headers['X-CSRFToken'] = csrftoken
    }
    let options = {method: method, headers: headers};
    if (data) {
        options.body = JSON.stringify(data);
    }
    let response = await fetch(url, options)
    let responseData = await response.json();
    if (response.ok) {
        return responseData;
    } else {
        throw new Error(responseData.error)
    }
}

async function onClick(event) {
    event.preventDefault();
    let button = event.currentTarget;
    let action = button.id;
    let a = Number(document.getElementById('A').value);
    let b = Number(document.getElementById('B').value);
    let result = document.getElementById('result');
    let response = await makeRequest('/api/v1/' + action + '/', 'POST', {A: a, B: b});
    if (response.answer !== undefined) {
    result.innerText = response.answer;
    result.style.color = 'green';
    }
    else {
        result.innerText = response.error;
        result.style.color = 'red';
    }
}



function onLoad() {
    let buttons = document.querySelectorAll("button")
    for (let button of buttons) {
        button.addEventListener("click", onClick);
    }
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

window.addEventListener("load", onLoad);