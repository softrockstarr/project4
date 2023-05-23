function getCookie(name){
    const value = `; ${document.cookie}`
    const parts = value.split(`; ${name}=`)
    if(parts.length == 2)
        return parts.pop().split(';').shift()
}

function saveEdit(id){
    const textareaContent = document.getElementById(`textarea_${id}`).value
    const content = document.getElementById(`content_${id}`)
    const editModal = document.getElementById(`edit_modal_${id}`)
    fetch(`/edit/${id}`, {
        method: "POST",
        headers: { "Content-type": "application/json", "X-CSRFToken": getCookie("csrftoken")},
        body: JSON.stringify({
            content: textareaContent
        })
    })
    .then(response => response.json())
    .then(result => {
        content.innerHTML = result.data
    
        editModal.classList.remove('show');
        editModal.setAttribute('aria-hidden', 'true');
        editModal.setAttribute('style', 'display: none');
    
        const modalsBackdrops = document.getElementsByClassName('modal-backdrop');

        for(let i=0; i < modalsBackdrops.length; i++) {
            document.body.removeChild(modalsBackdrops[i]);
        }
    })
}

function likePost(id, liked_posts) {
    const button = document.getElementById(`${id}`);
    const isLiked = button.classList.contains('fa-thumbs-down');
    const likeCount = document.getElementById(`likeCount_${id}`);
              
    if (isLiked) {
        fetch(`/unlike/${id}`)
            .then(response => response.json())
            .then(result => {
                button.classList.remove('fa-thumbs-down');
                button.classList.add('fa-thumbs-up');
                // Remove post ID from liked_posts array
                const index = liked_posts.indexOf(id);
                if (index > -1) {
                    liked_posts.splice(index, 1);
                }
                if (likeCount) {
                    const currentCount = parseInt(likeCount.innerText);
                    likeCount.innerText = isNaN(currentCount) ? 0 : currentCount - 1;
                }
            });
    } else {
        fetch(`/like/${id}`)
            .then(response => response.json())
            .then(result => {
                button.classList.remove('fa-thumbs-up');
                button.classList.add('fa-thumbs-down');
                // Add post ID to liked_posts array
                liked_posts.push(id);
                if (likeCount) {
                    const currentCount = parseInt(likeCount.innerText);
                    likeCount.innerText = isNaN(currentCount) ? 1 : currentCount + 1;
                }
            });
    }      
}


