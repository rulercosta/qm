const viewAllLink = document.getElementById('view-all-btn');

viewAllLink.addEventListener('click', (event) => {
    event.preventDefault();

    const nextSection = document.getElementById('cs-contact-549'); 
    nextSection.scrollIntoView({
        behavior: 'smooth', 
        block: 'start' 
    });
});
