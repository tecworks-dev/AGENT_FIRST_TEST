
// Entry point for React application
import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';

// Enable strict mode for additional checks and warnings
ReactDOM.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
  document.getElementById('root')
);

// Hot Module Replacement (HMR) - Remove this snippet to remove HMR.
// Learn more: https://www.snowpack.dev/concepts/hot-module-replacement
if (import.meta.hot) {
  import.meta.hot.accept();
}

// Log a message to confirm the application has started
console.log('React application started');
