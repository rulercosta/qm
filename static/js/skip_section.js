// Select the "View All" link and the next section
const viewAllLink = document.getElementById('view-all-btn');

// Add click event listener to the "View All" link
viewAllLink.addEventListener('click', (event) => {
    // Prevent default anchor link behavior (jumping to the section)
    event.preventDefault();

    // Smooth scroll to the next section
    const nextSection = document.getElementById('cs-contact-549'); // Replace with the ID of the section you want to scroll to
    nextSection.scrollIntoView({
        behavior: 'smooth', // Ensures smooth scrolling
        block: 'start' // Scrolls to the top of the next section
    });
});
