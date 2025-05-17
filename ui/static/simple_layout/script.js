import { initializeToggleButtons } from './toggleButton.js';
import {sendMessage, handleTextareaInput } from './textareaHandler.js';
import { handleFileUpload } from './fileUploadHandler.js';
import { fetchDocuments } from './docManager.js';

console.log("Script loaded");
fetchDocuments();
// Initialize toggle buttons
initializeToggleButtons();

// Get textarea element and handle input
const textarea = document.getElementById('userInput');
handleTextareaInput(textarea);

// Handle file upload
handleFileUpload();
