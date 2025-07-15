const dropZone = document.getElementById('dropZone');
const fileInput = document.getElementById('fileInput');
const browseBtn = document.querySelector('.browse-btn');
const progressSection = document.getElementById('progressSection');
const resultsSection = document.getElementById('resultsSection');
const errorSection = document.getElementById('errorSection');
const modelSelect = document.getElementById('modelSelect');
const languageSelect = document.getElementById('languageSelect');

let currentTranscriptionId = null;
let pollInterval = null;

browseBtn.addEventListener('click', () => fileInput.click());

fileInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
        handleFile(file);
    }
});

dropZone.addEventListener('click', (e) => {
    if (e.target === browseBtn) return;
    fileInput.click();
});

dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('drag-over');
});

dropZone.addEventListener('dragleave', () => {
    dropZone.classList.remove('drag-over');
});

dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('drag-over');
    
    const file = e.dataTransfer.files[0];
    if (file) {
        handleFile(file);
    }
});

function handleFile(file) {
    const maxSize = 100 * 1024 * 1024; // 100MB
    
    if (file.size > maxSize) {
        showError('File size exceeds 100MB limit');
        return;
    }
    
    const allowedTypes = ['audio/', 'video/mp4', 'video/webm'];
    const isValidType = allowedTypes.some(type => file.type.startsWith(type));
    
    if (!isValidType) {
        showError('Invalid file type. Please upload an audio file.');
        return;
    }
    
    uploadFile(file);
}

async function uploadFile(file) {
    const formData = new FormData();
    formData.append('audio', file);
    formData.append('model', modelSelect.value);
    formData.append('language', languageSelect.value);
    
    hideAll();
    progressSection.classList.remove('hidden');
    
    document.querySelector('.file-name').textContent = file.name;
    document.querySelector('.status').textContent = 'Uploading...';
    
    try {
        const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Upload failed');
        }
        
        currentTranscriptionId = data.transcriptionId;
        startPolling();
        
    } catch (error) {
        showError(error.message);
    }
}

function startPolling() {
    pollInterval = setInterval(checkStatus, 2000);
    checkStatus();
}

async function checkStatus() {
    if (!currentTranscriptionId) return;
    
    try {
        const response = await fetch(`/api/status/${currentTranscriptionId}`);
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Status check failed');
        }
        
        updateProgress(data);
        
        if (data.status === 'completed') {
            clearInterval(pollInterval);
            showResults(data);
        } else if (data.status === 'error') {
            clearInterval(pollInterval);
            showError(data.error || 'Transcription failed');
        }
        
    } catch (error) {
        clearInterval(pollInterval);
        showError(error.message);
    }
}

function updateProgress(data) {
    const progressFill = document.querySelector('.progress-fill');
    const progressText = document.querySelector('.progress-text');
    const status = document.querySelector('.status');
    
    progressFill.style.width = `${data.progress}%`;
    progressText.textContent = `${data.progress}%`;
    
    if (data.status === 'processing') {
        status.textContent = `Processing with ${data.model} model...`;
    }
}

function showResults(data) {
    hideAll();
    resultsSection.classList.remove('hidden');
    
    const transcriptionText = document.querySelector('.transcription-text');
    transcriptionText.textContent = data.text || 'No transcription available';
    
    const downloadBtns = document.querySelectorAll('.download-btn');
    downloadBtns.forEach(btn => {
        btn.onclick = () => downloadTranscription(btn.dataset.format);
    });
}

function downloadTranscription(format) {
    if (!currentTranscriptionId) return;
    
    window.location.href = `/api/download/${currentTranscriptionId}/${format}`;
}

function showError(message) {
    hideAll();
    errorSection.classList.remove('hidden');
    document.querySelector('.error-message').textContent = message;
}

function hideAll() {
    progressSection.classList.add('hidden');
    resultsSection.classList.add('hidden');
    errorSection.classList.add('hidden');
}

document.querySelector('.new-transcription-btn').addEventListener('click', () => {
    currentTranscriptionId = null;
    hideAll();
    fileInput.value = '';
});

document.querySelector('.retry-btn').addEventListener('click', () => {
    currentTranscriptionId = null;
    hideAll();
    fileInput.value = '';
});