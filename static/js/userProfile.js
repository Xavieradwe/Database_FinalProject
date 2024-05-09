document.addEventListener("DOMContentLoaded", function() {
    // updateProfile();
});


function updateProfile() {
    const formData = new FormData(document.getElementById('profileForm'));
    // console.log(formData.get('username'));
    const csrftoken = document.cookie.split(';').find(row => row.startsWith('csrftoken=')).split('=')[1];

    fetch('/api/update_profile/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken
        },
        body: formData,
    })

    .then(response => response.json())
    .then(data => {
        // console.log('sadasdsa');
        if (data.success) {
            alert("Profile updated successfully!");
            window.location.reload();
        } else {
            alert("Failed to update profile: " + data.message);
        }
    })
    .catch(error => console.error('Error:', error));
}
