document.getElementById('uploadForm').addEventListener('submit', async function (e) {
    e.preventDefault();
    
    let fileInput = document.getElementById('resumeFile');
    if (fileInput.files.length === 0) {
        alert("Please upload a resume.");
        return;
    }

    let formData = new FormData();
    formData.append("resume", fileInput.files[0]);

    let response = await fetch('/analyze', {
        method: 'POST',
        body: formData
    });

    let result = await response.json();
    document.getElementById('analysisResult').innerHTML = `<p>Resume Score: ${result.score}%</p><p>Missing Keywords: ${result.missing_keywords}</p>`;
});
