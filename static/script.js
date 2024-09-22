document.getElementById('upload').addEventListener('change', function() {
    const file = this.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(event) {
            document.getElementById('preview').src = event.target.result;
        };
        reader.readAsDataURL(file);
    }
});

document.getElementById('n-samples').addEventListener('input', function() {
    document.getElementById('sampleValue').innerText = this.value;
});

document.getElementById('uploadForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const formData = new FormData();
    formData.append('image', document.getElementById('upload').files[0]);
    formData.append('edge_detector', document.getElementById('edge-detector').value);
    formData.append('sampler', document.getElementById('sampling').value);
    formData.append('renderer', document.getElementById('render').value);
    formData.append('n_samples', document.getElementById('n-samples').value);

    fetch('/convert', {
        method: 'POST',
        body: formData
    })
    .then(response => response.blob())
    .then(blob => {
        const url = URL.createObjectURL(blob);
        document.getElementById('result').src = url;
    });
});
