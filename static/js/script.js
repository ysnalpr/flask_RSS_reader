document.getElementById('searchBar').addEventListener('input', function(e) {
    let query = e.target.value.toLowerCase();
    let newsItems = document.querySelectorAll('.card');
    
    newsItems.forEach(item => {
        let title = item.querySelector('.card-title').textContent.toLowerCase();
        let description = item.querySelector('.card-text').textContent.toLowerCase();

        if (title.includes(query) || description.includes(query)) {
            item.style.display = 'block';
        } else {
            item.style.display = 'none';
        }
    });
});
