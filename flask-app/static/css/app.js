document.addEventListener('DOMContentLoaded', () => {
    // Dark Mode Logic
    const toggleBtn = document.getElementById('themeToggle');
    const currentTheme = localStorage.getItem('theme') || 'light';
    
    if (currentTheme === 'dark') {
        document.documentElement.setAttribute('data-theme', 'dark');
    }

    toggleBtn.addEventListener('click', () => {
        let theme = document.documentElement.getAttribute('data-theme');
        let newTheme = theme === 'dark' ? 'light' : 'dark';
        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
    });

    // Modal Logic
    const modal = document.getElementById('mapModal');
    const iframe = document.getElementById('mapIframe');
    const closeBtn = document.querySelector('.close-modal');

    document.querySelectorAll('.map-link').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const lat = link.getAttribute('data-lat');
            const lon = link.getAttribute('data-lon');
            // Use Google Maps Embed URL
            iframe.src = `https://maps.google.com/maps?q=${lat},${lon}&z=14&output=embed`;
            modal.style.display = 'block';
        });
    });

    closeBtn.onclick = () => {
        modal.style.display = 'none';
        iframe.src = '';
    };

    window.onclick = (event) => {
        if (event.target == modal) closeBtn.onclick();
    };
});