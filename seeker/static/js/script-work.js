document.addEventListener('DOMContentLoaded', function () {
    // Sample job data (you might fetch this from a server in a real application)
    const jobData = [
      { title: 'Web Developer', company: 'Tech Co.', description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.', id: 1 },
      { title: 'Graphic Designer', company: 'Design Studio', description: 'Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.', id: 2 },
      // Add more job listings as needed
    ];
  
    // Display job listings
    const jobListingsContainer = document.getElementById('jobListings');
    jobData.forEach(job => {
      const jobElement = document.createElement('div');
      jobElement.classList.add('job');
      jobElement.innerHTML = `
        <h2>${job.title}</h2>
        <p>${job.company}</p>
        <p>${job.description}</p>
        <button class="applyBtn" onclick="applyForJob(${job.id})">Apply</button>
      `;
      jobListingsContainer.appendChild(jobElement);
    });
  
    // Function to simulate job application (you might replace this with actual logic)
    window.applyForJob = function (jobId) {
      alert(`Applied for job with ID: ${jobId}`);
    };
  });

  
  // for navigating to login and register page

function navigateToLoginPage() {
    // Set the URL of the target page
    var targetPageUrl = "user-login.html";
  
    // Navigate to the target page
    window.location.href = targetPageUrl;
  }
  
  
  function navigateToSignUpPage() {
    // Set the URL of the target page
    var targetPageUrl = "user-register.html";
  
    // Navigate to the target page
    window.location.href = targetPageUrl;
  }