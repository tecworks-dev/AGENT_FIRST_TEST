
/**
 * app/static/js/utils.js
 * 
 * This file contains utility functions for the frontend of the AI Software Factory application.
 * It includes helper functions for common tasks, date formatting, and input validation.
 */

// Debug mode flag
const DEBUG = true;

/**
 * Formats a date object into a human-readable string
 * @param {Date} date - The date to format
 * @returns {string} Formatted date string
 */
function formatDate(date) {
    if (DEBUG) console.log('Formatting date:', date);
    const options = { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' };
    return date.toLocaleDateString(undefined, options);
}

/**
 * Validates an email address
 * @param {string} email - The email address to validate
 * @returns {boolean} True if the email is valid, false otherwise
 */
function validateEmail(email) {
    if (DEBUG) console.log('Validating email:', email);
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(String(email).toLowerCase());
}

/**
 * Truncates a string to a specified length and adds ellipsis if necessary
 * @param {string} str - The string to truncate
 * @param {number} maxLength - The maximum length of the string
 * @returns {string} Truncated string
 */
function truncateString(str, maxLength) {
    if (DEBUG) console.log('Truncating string:', str, 'to length:', maxLength);
    if (str.length <= maxLength) return str;
    return str.slice(0, maxLength - 3) + '...';
}

/**
 * Debounces a function call
 * @param {Function} func - The function to debounce
 * @param {number} wait - The number of milliseconds to wait
 * @returns {Function} Debounced function
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Escapes HTML special characters in a string
 * @param {string} unsafe - The unsafe string
 * @returns {string} Escaped safe string
 */
function escapeHtml(unsafe) {
    if (DEBUG) console.log('Escaping HTML:', unsafe);
    return unsafe
         .replace(/&/g, "&amp;")
         .replace(/</g, "&lt;")
         .replace(/>/g, "&gt;")
         .replace(/"/g, "&quot;")
         .replace(/'/g, "&#039;");
}

/**
 * Generates a random ID
 * @returns {string} Random ID
 */
function generateRandomId() {
    if (DEBUG) console.log('Generating random ID');
    return Math.random().toString(36).substr(2, 9);
}

/**
 * Validates a password strength
 * @param {string} password - The password to validate
 * @returns {boolean} True if the password is strong enough, false otherwise
 */
function validatePasswordStrength(password) {
    if (DEBUG) console.log('Validating password strength');
    const minLength = 8;
    const hasUpperCase = /[A-Z]/.test(password);
    const hasLowerCase = /[a-z]/.test(password);
    const hasNumbers = /\d/.test(password);
    const hasNonalphas = /\W/.test(password);
    return password.length >= minLength && hasUpperCase && hasLowerCase && hasNumbers && hasNonalphas;
}

/**
 * Formats a number as currency
 * @param {number} amount - The amount to format
 * @param {string} currencyCode - The currency code (e.g., 'USD')
 * @returns {string} Formatted currency string
 */
function formatCurrency(amount, currencyCode = 'USD') {
    if (DEBUG) console.log('Formatting currency:', amount, currencyCode);
    return new Intl.NumberFormat('en-US', { style: 'currency', currency: currencyCode }).format(amount);
}

/**
 * Converts a string to title case
 * @param {string} str - The string to convert
 * @returns {string} Title cased string
 */
function toTitleCase(str) {
    if (DEBUG) console.log('Converting to title case:', str);
    return str.replace(
        /\w\S*/g,
        function(txt) {
            return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
        }
    );
}

// Export the functions if using a module system
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        formatDate,
        validateEmail,
        truncateString,
        debounce,
        escapeHtml,
        generateRandomId,
        validatePasswordStrength,
        formatCurrency,
        toTitleCase
    };
}
