document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.edit-btn').forEach(button => {
        button.addEventListener('click', function() {
            const post = this.closest('.post-container');
            const content = post.querySelector('.post-content');
            const textarea = post.querySelector('.edit-area');
            const saveButton = post.querySelector('.save-btn');
            
            textarea.value = content.textContent.trim();
            content.classList.add('hidden');
            textarea.classList.remove('hidden');
            this.classList.add('hidden');
            saveButton.classList.remove('hidden');
        });
    });

    document.querySelectorAll('.save-btn').forEach(button => {
        button.addEventListener('click', function() {
            const post = this.closest('.post-container');
            const content = post.querySelector('.post-content');
            const textarea = post.querySelector('.edit-area');
            const editButton = post.querySelector('.edit-btn');

            const newContent = textarea.value.trim();

            fetch(`/update_post/${post.dataset.postId}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': '{{ csrf_token }}'
                },
                body: JSON.stringify({ content: newContent })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    content.textContent = newContent;
                    textarea.classList.add('hidden');
                    content.classList.remove('hidden');
                    button.classList.add('hidden');
                    editButton.classList.remove('hidden');
                } else {
                    console.error('Error updating post:', data.error);
                }
            });
        });
    });
});