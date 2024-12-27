function downloadCertificate() {
    const form = document.createElement('form');
    form.method = 'POST';
    form.action = '/events/workshops/verify/{{ cid }}/download';  // Pass the cid in the URL

    // Add hidden input field for cid (if you want to pass it explicitly)
    const cidInput = document.createElement('input');
    cidInput.type = 'hidden';
    cidInput.name = 'cid';  // Match the parameter in the route
    cidInput.value = '{{ cid }}';  // This should be passed from the backend

    form.appendChild(cidInput);
    document.body.appendChild(form);
    form.submit();
}