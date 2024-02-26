// JavaScript code for profile picture selection

// Function to handle file input change event
function handleFileInputChange(event) {
    const file = event.target.files[0]; // Get the selected file
    const img = document.getElementById('profile-img'); // Get the profile picture element
    const reader = new FileReader(); // Create a file reader object
  
    // Event listener for file reader onload event
    reader.onload = function(e) {
      img.src = e.target.result; // Set the source of the profile picture to the selected file
    };
  
    // Read the selected file as a data URL
    reader.readAsDataURL(file);
  }
  
  // Add event listener for file input change event
  document.getElementById('file-input').addEventListener('change', handleFileInputChange);
  