
/**
 * code_editor.js
 * 
 * This file contains JavaScript code for initializing and managing the code editor functionality.
 * It includes features such as syntax highlighting and auto-completion.
 */

// Initialize CodeMirror instance
let codeEditor;

document.addEventListener('DOMContentLoaded', () => {
    initializeCodeEditor();
    setupAutoCompletion();
});

/**
 * Initialize the CodeMirror editor
 */
function initializeCodeEditor() {
    const codeEditorElement = document.getElementById('code-editor');
    if (!codeEditorElement) {
        console.error('Code editor element not found');
        return;
    }

    codeEditor = CodeMirror.fromTextArea(codeEditorElement, {
        mode: 'python', // Default to Python, can be changed dynamically
        theme: 'monokai',
        lineNumbers: true,
        autoCloseBrackets: true,
        matchBrackets: true,
        indentUnit: 4,
        tabSize: 4,
        indentWithTabs: false,
        foldGutter: true,
        gutters: ['CodeMirror-linenumbers', 'CodeMirror-foldgutter'],
        extraKeys: {
            'Ctrl-Space': 'autocomplete'
        }
    });

    // Set initial size
    codeEditor.setSize(null, '400px');

    // Add change event listener
    codeEditor.on('change', (cm, change) => {
        if (change.origin !== 'setValue') {
            requestCodeCompletion(cm);
        }
    });
}

/**
 * Set up auto-completion for the code editor
 */
function setupAutoCompletion() {
    CodeMirror.commands.autocomplete = (cm) => {
        CodeMirror.showHint(cm, CodeMirror.hint.anyword);
    };
}

/**
 * Request code completion suggestions from the server
 * @param {CodeMirror} cm - CodeMirror instance
 */
function requestCodeCompletion(cm) {
    const cursor = cm.getCursor();
    const line = cm.getLine(cursor.line);
    const lineUptoCursor = line.slice(0, cursor.ch);

    // Only request completion if we're not in the middle of a word
    if (/\w$/.test(lineUptoCursor)) {
        return;
    }

    fetch('/api/code-completion', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            code: cm.getValue(),
            line: cursor.line,
            ch: cursor.ch
        }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.suggestions && data.suggestions.length > 0) {
            cm.showHint({
                hint: function() {
                    return {
                        from: CodeMirror.Pos(cursor.line, cursor.ch),
                        to: CodeMirror.Pos(cursor.line, cursor.ch),
                        list: data.suggestions
                    };
                }
            });
        }
    })
    .catch(error => console.error('Error fetching code completion:', error));
}

/**
 * Change the language mode of the code editor
 * @param {string} language - The language to switch to (e.g., 'python', 'javascript')
 */
function changeEditorLanguage(language) {
    if (codeEditor) {
        codeEditor.setOption('mode', language);
    }
}

/**
 * Get the current content of the code editor
 * @returns {string} The current content of the code editor
 */
function getEditorContent() {
    return codeEditor ? codeEditor.getValue() : '';
}

/**
 * Set the content of the code editor
 * @param {string} content - The content to set in the code editor
 */
function setEditorContent(content) {
    if (codeEditor) {
        codeEditor.setValue(content);
    }
}

// Export functions for use in other modules
export {
    initializeCodeEditor,
    changeEditorLanguage,
    getEditorContent,
    setEditorContent
};
