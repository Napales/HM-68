async function makeCommentRequest(url, method = 'GET') {
    let response = await fetch(url, {"method": method})
    if (response.ok) {
        return await response.json();
    } else {
        let error = await response.json()
        throw new Error(error.message)
    }
}

async function onCommentClick(event) {
    event.preventDefault();
    let a = event.currentTarget;
    let url = a.href;
    let response = await makeCommentRequest(url);
    let span = a.parentElement.querySelector('.comment-likes');
    span.innerText = response.likes_count;
    console.log(response)

    let icon = a.querySelector('i');
    if (response.like) {
        icon.classList.remove('bi-heart');
        icon.classList.add('bi-heart-fill');
    } else {
        icon.classList.remove('bi-heart-fill');
        icon.classList.add('bi-heart');
    }
}

function onCommentLoad() {
    let links = document.querySelectorAll("[data-js='comment-like']")
    for (let link of links) {
        link.addEventListener("click", onCommentClick);
    }
}

window.addEventListener("load", onCommentLoad)
