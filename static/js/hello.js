document.getElementById('folder').addEventListener('change', function(e) {
    const files = e.target.files;
    const submitBtn = document.getElementById('submitBtn');
    const fileInfo = document.getElementById('fileInfo');
    
    if (files.length > 0) {
        submitBtn.style.display = 'inline-block';
        fileInfo.textContent = `${files.length} file(s) selected`;
        
        // Add animation to submit button
        submitBtn.classList.add('animate__animated', 'animate__pulse');
        setTimeout(() => {
            submitBtn.classList.remove('animate__animated', 'animate__pulse');
        }, 1000);
    } else {
        submitBtn.style.display = 'none';
        fileInfo.textContent = 'No files selected';
    }
});
