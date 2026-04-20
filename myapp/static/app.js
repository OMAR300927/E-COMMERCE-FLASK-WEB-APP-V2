const searchbar = document.querySelector('.search-bar');
let filteredProducts = [];

searchbar.addEventListener('keyup', (e) => {
    const value = e.target.value.toLowerCase();

    const items = document.getElementsByTagName('li');
    
    Array.from(items).forEach(function(item){
        const text = item.innerText.toLowerCase();

        // استخراج الاسم من النص
        const match = text.match(/product name:\s*(.*)/i);
        const name = match ? match[1].split('\n')[0] : '';

        if (name.includes(value)) {
            item.style.display = '';
        } else {
            item.style.display = 'none';
        }
    });

});