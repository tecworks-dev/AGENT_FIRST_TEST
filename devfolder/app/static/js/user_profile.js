
/**
 * user_profile.js
 * JavaScript file for user profile functionality
 * This file handles user profile-related operations and UI interactions
 */

// Import utility functions if needed
import { displayErrorToUser, reportErrorToServer } from './error_handling.js';
import { formatDate } from './utils.js';

// User Profile class
class UserProfile {
    constructor() {
        this.initEventListeners();
    }

    initEventListeners() {
        // Add event listeners for profile-related actions
        document.getElementById('update-profile-form').addEventListener('submit', this.updateProfile.bind(this));
        document.getElementById('change-password-form').addEventListener('submit', this.changePassword.bind(this));
        document.getElementById('delete-account-btn').addEventListener('click', this.confirmDeleteAccount.bind(this));
    }

    async updateProfile(event) {
        event.preventDefault();
        const form = event.target;
        const formData = new FormData(form);

        try {
            const response = await fetch('/api/user/update-profile', {
                method: 'POST',
                body: formData
            });

            if (response.ok) {
                const result = await response.json();
                this.displaySuccessMessage('Profile updated successfully');
                this.updateProfileUI(result);
            } else {
                throw new Error('Failed to update profile');
            }
        } catch (error) {
            displayErrorToUser('Error updating profile. Please try again.');
            reportErrorToServer(error);
        }
    }

    async changePassword(event) {
        event.preventDefault();
        const form = event.target;
        const formData = new FormData(form);

        try {
            const response = await fetch('/api/user/change-password', {
                method: 'POST',
                body: formData
            });

            if (response.ok) {
                this.displaySuccessMessage('Password changed successfully');
                form.reset();
            } else {
                throw new Error('Failed to change password');
            }
        } catch (error) {
            displayErrorToUser('Error changing password. Please try again.');
            reportErrorToServer(error);
        }
    }

    confirmDeleteAccount() {
        if (confirm('Are you sure you want to delete your account? This action cannot be undone.')) {
            this.deleteAccount();
        }
    }

    async deleteAccount() {
        try {
            const response = await fetch('/api/user/delete-account', {
                method: 'POST'
            });

            if (response.ok) {
                window.location.href = '/logout';
            } else {
                throw new Error('Failed to delete account');
            }
        } catch (error) {
            displayErrorToUser('Error deleting account. Please try again.');
            reportErrorToServer(error);
        }
    }

    displaySuccessMessage(message) {
        const successAlert = document.createElement('div');
        successAlert.className = 'alert alert-success';
        successAlert.textContent = message;
        document.querySelector('.profile-container').prepend(successAlert);
        setTimeout(() => successAlert.remove(), 5000);
    }

    updateProfileUI(userData) {
        document.getElementById('profile-username').textContent = userData.username;
        document.getElementById('profile-email').textContent = userData.email;
        document.getElementById('profile-joined-date').textContent = formatDate(userData.created_at);
    }

    async loadUserProjects() {
        try {
            const response = await fetch('/api/user/projects');
            if (response.ok) {
                const projects = await response.json();
                this.displayUserProjects(projects);
            } else {
                throw new Error('Failed to load user projects');
            }
        } catch (error) {
            displayErrorToUser('Error loading user projects. Please try again.');
            reportErrorToServer(error);
        }
    }

    displayUserProjects(projects) {
        const projectList = document.getElementById('user-projects-list');
        projectList.innerHTML = '';
        projects.forEach(project => {
            const projectElement = document.createElement('div');
            projectElement.className = 'project-item';
            projectElement.innerHTML = `
                <h3>${project.name}</h3>
                <p>${project.description}</p>
                <p>Created: ${formatDate(project.created_at)}</p>
                <a href="/project/${project.id}" class="btn btn-primary">View Project</a>
            `;
            projectList.appendChild(projectElement);
        });
    }
}

// Initialize the UserProfile functionality when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', () => {
    const userProfile = new UserProfile();
    userProfile.loadUserProjects();
});

// If using modules, export the UserProfile class
export { UserProfile };
