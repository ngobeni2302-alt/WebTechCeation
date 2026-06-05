const offers = {
    birthday: {
        label: 'Birthday Websites',
        title: 'Birthday Website Folder',
        description: 'Bright, celebratory website previews made for birthdays, milestones, and special memories.',
        images: [
            {
                src: 'assets/images/birthday_website_preview_1775633285058.png',
                alt: 'Birthday website preview',
                title: 'Birthday Celebration'
            },
            {
                src: 'assets/images/portfolio_website_preview_1775633502924.png',
                alt: 'Creative website preview',
                title: 'Creative Event Layout'
            }
        ]
    },
    love: {
        label: 'Love & Anniversary',
        title: 'Love & Anniversary Folder',
        description: 'Elegant website previews for romantic stories, anniversaries, and meaningful moments.',
        images: [
            {
                src: 'assets/images/love_website_preview_1775633355080.png',
                alt: 'Love website preview',
                title: 'Love Story'
            },
            {
                src: 'assets/images/birthday_website_preview_1775633285058.png',
                alt: 'Celebration website preview',
                title: 'Shared Memories'
            }
        ]
    },
    business: {
        label: 'Business Websites',
        title: 'Business Website Folder',
        description: 'Professional website previews for businesses, brands, services, and online presence.',
        images: [
            {
                src: 'assets/images/business_website_preview_1775633462836.png',
                alt: 'Business website preview',
                title: 'Business Landing Page'
            },
            {
                src: 'assets/images/portfolio_website_preview_1775633502924.png',
                alt: 'Portfolio website preview',
                title: 'Professional Profile'
            }
        ]
    },
    more: {
        label: 'Graphic Design',
        title: 'Graphic Design Folder',
        description: 'A focused set of portfolio, brand, and layout visuals for creative graphic design work.',
        images: [
            {
                src: 'assets/images/portfolio_website_preview_1775633502924.png',
                alt: 'Graphic design portfolio preview',
                title: 'Portfolio Design'
            },
            {
                src: 'assets/images/business_website_preview_1775633462836.png',
                alt: 'Graphic design brand preview',
                title: 'Brand Design'
            },
            {
                src: 'assets/images/love_website_preview_1775633355080.png',
                alt: 'Graphic design layout preview',
                title: 'Layout Design'
            }
        ]
    }
};

const params = new URLSearchParams(window.location.search);
const folder = params.get('folder') || 'birthday';
const offer = offers[folder] || offers.birthday;

document.title = `${offer.label} | WEBHub`;
document.getElementById('offerLabel').textContent = offer.label;
document.getElementById('offerTitle').textContent = offer.title;
document.getElementById('offerDescription').textContent = offer.description;

const gallery = document.getElementById('offerGallery');

gallery.innerHTML = offer.images.map((image) => `
    <article class="offer-preview-card">
        <img src="${image.src}" alt="${image.alt}" class="clickable-image">
        <h2>${image.title}</h2>
    </article>
`).join('');
