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
        } else {
            console.error('Login failed:', data.error);
            // Show error message to user
        }
    } catch (error) {
        console.error('Error during login:', error);
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
        } else {
            console.error('Registration failed:', data.error);
            // Show error message to user
        }
    } catch (error) {
        console.error('Error during registration:', error);
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
        } else {
            console.error('Failed to send message:', data.error);
            // Show error message to user
        }
    } catch (error) {
        console.error('Error sending message:', error);
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
        } else {
            console.error('Failed to upload media:', data.error);
            // Show error message to user
        }
    } catch (error) {
        console.error('Error uploading media:', error);
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
        } else {
            console.error('Search failed:', data.error);
            // Show error message to user
        }
    } catch (error) {
        console.error('Error during search:', error);
    }
}