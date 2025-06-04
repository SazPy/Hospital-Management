// Theme toggle functionality
document.addEventListener('DOMContentLoaded', () => {
    // Get saved theme from localStorage or default to light
    const currentTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', currentTheme);

    // Update button icon based on current theme
    updateThemeToggleButton(currentTheme);

    // Add click handler to theme toggle buttons
    document.querySelectorAll('.theme-toggle').forEach(button => {
        button.addEventListener('click', () => {
            const currentTheme = document.documentElement.getAttribute('data-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            
            // Update theme
            document.documentElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            
            // Update button icon
            updateThemeToggleButton(newTheme);
        });
    });
});

// Update theme toggle button icon and text
function updateThemeToggleButton(theme) {
    document.querySelectorAll('.theme-toggle').forEach(button => {
        const icon = button.querySelector('i');
        const text = button.querySelector('span');
        
        if (theme === 'dark') {
            icon.classList.remove('fa-moon');
            icon.classList.add('fa-sun');
            text.textContent = 'Light Mode';
        } else {
            icon.classList.remove('fa-sun');
            icon.classList.add('fa-moon');
            text.textContent = 'Dark Mode';
        }
    });
} 