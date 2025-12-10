document.addEventListener('DOMContentLoaded', () => {
    console.log('Portfolio loaded.');

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });

    // Content Loading Logic
    const loadContent = async (category) => {
        const container = document.getElementById('content-container');
        if (!container) return;

        try {
            let fetchUrl = 'content/data.json';
            const location = window.location.pathname;

            if (location.includes('/poems/') || location.includes('/prose/') || location.includes('/quotes/')) {
                fetchUrl = '../content/data.json';
            }

            const response = await fetch(fetchUrl);
            if (!response.ok) throw new Error('Failed to load content');
            const data = await response.json();

            const items = data[category];
            if (!items) return;

            container.innerHTML = ''; // Clear loading state

            items.forEach(item => {
                const article = document.createElement('article');
                article.className = `content-item ${category === 'prose' ? 'prose-item' : ''}`;

                const bodyClass = category === 'prose' ? 'prose-body' : 'poem-body';

                article.innerHTML = `
                    <h2>${item.title}</h2>
                    <div class="${bodyClass}">
                        ${item.body}
                    </div>
                `;
                container.appendChild(article);
            });

        } catch (error) {
            console.error('Error loading content:', error);
            container.innerHTML = '<p>Error loading content. Please check console.</p>';
        }
    };

    const loadFeatured = async () => {
        const container = document.getElementById('featured-grid');
        if (!container) return;

        try {
            const response = await fetch('content/data.json');
            const data = await response.json();

            container.innerHTML = '';

            // prose
            if (data.prose && data.prose.length > 0) {
                const p = data.prose[0];
                const snippet = p.body.replace(/<[^>]*>?/gm, '').substring(0, 100) + '...';
                container.innerHTML += createFeaturedCard('Latest Prose', p.title, snippet, 'prose/');
            }

            // poems (latest 2)
            if (data.poems && data.poems.length > 0) {
                const latestPoems = data.poems.slice(-2).reverse();
                latestPoems.forEach(p => {
                    const snippet = p.body.replace(/<[^>]*>?/gm, '').substring(0, 100) + '...';
                    container.innerHTML += createFeaturedCard('Poem', p.title, snippet, 'poems/');
                });
            }

        } catch (e) {
            console.error(e);
        }
    };

    const createFeaturedCard = (type, title, snippet, link) => {
        return `
            <article class="content-item">
                <span class="card-meta">${type}</span>
                <h3>${title}</h3>
                <p>${snippet}</p>
                <a href="${link}">Read ${type} &rarr;</a>
            </article>
        `;
    };

    // Router-ish logic
    if (window.location.pathname.includes('/poems/')) {
        loadContent('poems');
    } else if (window.location.pathname.includes('/prose/')) {
        loadContent('prose');
    } else if (window.location.pathname.includes('/quotes/')) {
        loadContent('quotes');
    } else {
        loadFeatured();
    }
});
