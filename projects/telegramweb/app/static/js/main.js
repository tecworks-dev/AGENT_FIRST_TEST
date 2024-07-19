// Main JavaScript file for frontend functionality

document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    const registerForm = document.getElementById('register-form');
    const messageForm = document.getElementById('message-form');
    const mediaUploadForm = document.getElementById('media-upload-form');
    const searchForm = document.getElementById('search-form');

    if (loginForm) loginForm.addEventListener('submit', handleLogin);
    if (registerForm) registerForm.addEventListener('submit', handleRegister);
    if (messageForm) messageForm.addEventListener('submit', handleSendMessage);
    if (mediaUploadForm) mediaUploadForm.addEventListener('submit', handleMediaUpload);
    if (searchForm) searchForm.addEventListener('submit', handleSearch);
});

async function handleLogin(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    try {
        const response = await fetch('/login', {
            method: 'POST',
            body: formData
        });
        const data = await response.json();
        if (response.ok) {
            console.log('Login successful:', data);
            // Redirect or update UI as needed
            window.location.reload(); // Reload the page to update UI
        } else {
            console.error('Login failed:', data.error);
            // Show error message to user
            alert('Login failed: ' + data.error);
        }
    } catch (error) {
        console.error('Error during login:', error);
        alert('An error occurred during login. Please try again.');
    }
}

async function handleRegister(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    try {
        const response = await fetch('/register', {
            method: 'POST',
            body: formData
        });
        const data = await response.json();
        if (response.ok) {
            console.log('Registration successful:', data);
            // Redirect to login or update UI as needed
            alert('Registration successful. Please log in.');
            window.location.reload(); // Reload the page to show login form
        } else {
            console.error('Registration failed:', data.error);
            // Show error message to user
            alert('Registration failed: ' + data.error);
        }
    } catch (error) {
        console.error('Error during registration:', error);
        alert('An error occurred during registration. Please try again.');
    }
}

async function handleSendMessage(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const messageData = {
        receiver_id: parseInt(formData.get('receiver_id')),
        content: formData.get('content')
    };
    try {
        const response = await fetch('/messages', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(messageData)
        });
        const data = await response.json();
        if (response.ok) {
            console.log('Message sent:', data);
            // Clear input field and update message list
            event.target.reset();
            // You might want to add a function to update the message list here
            updateMessageList(data);
        } else {
            console.error('Failed to send message:', data.error);
            // Show error message to user
            alert('Failed to send message: ' + data.error);
        }
    } catch (error) {
        console.error('Error sending message:', error);
        alert('An error occurred while sending the message. Please try again.');
    }
}

async function handleMediaUpload(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    try {
        const response = await fetch('/media', {
            method: 'POST',
            body: formData
        });
        const data = await response.json();
        if (response.ok) {
            console.log('Media uploaded:', data);
            // Update UI to show uploaded media
            alert('Media uploaded successfully!');
        } else {
            console.error('Failed to upload media:', data.error);
            // Show error message to user
            alert('Failed to upload media: ' + data.error);
        }
    } catch (error) {
        console.error('Error uploading media:', error);
        alert('An error occurred while uploading media. Please try again.');
    }
}

async function handleSearch(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const query = formData.get('query');
    try {
        const response = await fetch(`/search?query=${encodeURIComponent(query)}`, {
            method: 'GET'
        });
        const data = await response.json();
        if (response.ok) {
            console.log('Search results:', data);
            // Display search results in UI
            displaySearchResults(data);
        } else {
            console.error('Search failed:', data.error);
            // Show error message to user
            alert('Search failed: ' + data.error);
        }
    } catch (error) {
        console.error('Error during search:', error);
        alert('An error occurred during search. Please try again.');
    }
}

function loadUsers() {
    fetch('/users')
        .then(response => response.json())
        .then(users => {
            const userList = document.getElementById('user-list');
            userList.innerHTML = '';
            users.forEach(user => {
                const li = document.createElement('li');
                li.textContent = user.username;
                li.dataset.userId = user.id;
                li.addEventListener('click', () => selectUser(user.id, user.username));
                userList.appendChild(li);
            });
        })
        .catch(error => console.error('Error loading users:', error));
}

function selectUser(userId, username) {
    const receiverIdInput = document.getElementById('receiver-id');
    receiverIdInput.value = userId;
    alert(`Selected user: ${username}`);
}

function updateMessageList(message) {
    const messageList = document.getElementById('message-list');
    const messageElement = document.createElement('div');
    messageElement.textContent = `${message.content} (Sent to: ${message.receiver_id})`;
    messageList.appendChild(messageElement);
}

function displaySearchResults(results) {
    const searchResults = document.getElementById('search-results');
    searchResults.innerHTML = '';
    results.forEach(result => {
        const resultElement = document.createElement('div');
        resultElement.textContent = result.content;
        searchResults.appendChild(resultElement);
    });
}

document.addEventListener('DOMContentLoaded', loadUsers);