// Helper function to get company logo initials
function getCompanyInitials(companyName) {
    return companyName.split(' ').map(word => word.charAt(0)).join('').substring(0, 2);
}

// Helper function to get campaign badge class
function getCampaignBadgeClass(campaign) {
    const campaignLower = campaign.toLowerCase();
    if (campaignLower.includes('gratis') || campaignLower.includes('rabat')) {
        return 'positive';
    } else if (campaignLower.includes('online') || campaignLower.includes('standard')) {
        return 'standard';
    } else if (campaignLower.includes('kun') || campaignLower.includes('begrænset')) {
        return 'limited';
    }
    return 'standard';
}

// Helper function to get tilvalg icon
function getTilvalgIcon(tilvalg) {
    const tilvalgLower = tilvalg.toLowerCase();
    if (tilvalgLower.includes('kasko')) return '<i class="fas fa-shield-alt"></i>';
    if (tilvalgLower.includes('glasskade')) return '<i class="fas fa-search"></i>';
    if (tilvalgLower.includes('vejhjælp')) return '<i class="fas fa-tools"></i>';
    if (tilvalgLower.includes('rejse')) return '<i class="fas fa-plane"></i>';
    if (tilvalgLower.includes('elbil')) return '<i class="fas fa-charging-station"></i>';
    return '<i class="fas fa-check"></i>';
}

// Load and display bilforsikring data
async function loadBilforsikringData() {
    try {
        const response = await fetch('bilforsikring.json');
        const jsonData = await response.json();
        
        // Handle both old format (array) and new format (object with data property)
        const data = jsonData.data || jsonData;
        
        // Create new card-based layout
        createBilforsikringCards(data);
        
        // Keep table for fallback (hidden)
        const tbody = document.getElementById('bilforsikring-table');
        tbody.innerHTML = '';
        
        data.forEach(item => {
            const row = document.createElement('tr');
            const badgeClass = getCampaignBadgeClass(item.kampagne);
            
            row.innerHTML = `
                <td>
                    <div class="company-name">
                        <div class="company-logo">${getCompanyInitials(item.udbyder)}</div>
                        <strong>${item.udbyder}</strong>
                    </div>
                </td>
                <td>${item.produkt}</td>
                <td class="price">${item.pris_mdr}</td>
                <td>${item.dækning}</td>
                <td>
                    <ul class="tilvalg-list">
                        ${item.tilvalg.map(tilvalg => `<li>${getTilvalgIcon(tilvalg)} ${tilvalg}</li>`).join('')}
                    </ul>
                </td>
                <td><span class="kampagne ${badgeClass}">${item.kampagne}</span></td>
                <td><a href="${item.link}" target="_blank" class="btn-primary">Se tilbud</a></td>
            `;
            tbody.appendChild(row);
        });
        
        // Create mobile cards
        createBilforsikringMobileCards(data);
    } catch (error) {
        console.error('Error loading bilforsikring data:', error);
    }
}

// Helper function to get car brand logo
function getCarBrandLogo(brand) {
    const brandLower = brand.toLowerCase();
    if (brandLower === 'tesla') return '<i class="fas fa-bolt"></i>';
    if (brandLower === 'volkswagen') return '<i class="fas fa-car"></i>';
    if (brandLower === 'kia') return '<i class="fas fa-battery-full"></i>';
    if (brandLower === 'toyota') return '<i class="fas fa-leaf"></i>';
    return '<i class="fas fa-car-side"></i>';
}

// Load and display leasing data
async function loadLeasingData() {
    try {
        const response = await fetch('leasing.json');
        const jsonData = await response.json();
        
        // Handle both old format (array) and new format (object with data property)
        const data = jsonData.data || jsonData;
        
        // Create new card-based layout
        createLeasingCards(data);
        
        // Keep table for fallback (hidden)
        const tbody = document.getElementById('leasing-table');
        tbody.innerHTML = '';
        
        data.forEach(item => {
            const row = document.createElement('tr');
            const badgeClass = getCampaignBadgeClass(item.kampagne);
            
            row.innerHTML = `
                <td>
                    <div class="company-name">
                        <div class="company-logo">${getCarBrandLogo(item.mærke)}</div>
                        <strong>${item.mærke}</strong>
                    </div>
                </td>
                <td>${item.model}</td>
                <td class="price">${item.pris_mdr}</td>
                <td>${item.udbetaling}</td>
                <td>${item.løbetid}</td>
                <td><span class="kampagne ${badgeClass}">${item.kampagne}</span></td>
                <td><a href="${item.link}" target="_blank" class="btn-primary">Se tilbud</a></td>
            `;
            tbody.appendChild(row);
        });
        
        // Create mobile cards
        createLeasingMobileCards(data);
    } catch (error) {
        console.error('Error loading leasing data:', error);
    }
}

// Add JSON-LD structured data for FAQ
function addFAQStructuredData() {
    const faqData = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": "Hvad koster bilforsikring i Danmark?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "Prisen på bilforsikring varierer afhængigt af bilens værdi, din køreerfaring og valgte dækning. Basis ansvarforsikring starter typisk fra 400 kr. om måneden, mens fuld kasko kan koste 800-1500 kr. om måneden."
                }
            },
            {
                "@type": "Question",
                "name": "Hvad er forskellen mellem privatleasing og erhvervsleasing?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "Privatleasing er til private personer, mens erhvervsleasing er til virksomheder. Erhvervsleasing kan ofte være billigere på grund af skattefordele, men kræver at bilen bruges til erhvervsformål."
                }
            },
            {
                "@type": "Question",
                "name": "Kan jeg lease en elbil uden udbetaling?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "Ja, mange leasingudbydere tilbyder leasing uden udbetaling, især for elbiler. Dette kan dog betyde en højere månedlig ydelse sammenlignet med leasing med udbetaling."
                }
            }
        ]
    };
    
    const script = document.createElement('script');
    script.type = 'application/ld+json';
    script.textContent = JSON.stringify(faqData);
    document.head.appendChild(script);
}

// FAQ Accordion functionality
function initializeFAQ() {
    const faqCards = document.querySelectorAll('.faq-card');
    
    if (faqCards.length === 0) {
        return;
    }
    
    faqCards.forEach((card, index) => {
        const header = card.querySelector('.faq-header');
        
        if (!header) {
            return;
        }
        
        // Clear any existing event listeners
        const newHeader = header.cloneNode(true);
        header.parentNode.replaceChild(newHeader, header);
        
        newHeader.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            const currentCard = this.parentElement;
            const isActive = currentCard.classList.contains('active');
            
            // Close all FAQ cards
            faqCards.forEach((faqCard, i) => {
                faqCard.classList.remove('active');
            });
            
            // Open clicked card if it wasn't active
            if (!isActive) {
                currentCard.classList.add('active');
            }
        });
    });
}

// Smooth scrolling for anchor links
function initializeSmoothScrolling() {
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    
    anchorLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = link.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Initialize page
document.addEventListener('DOMContentLoaded', function() {
    loadBilforsikringData();
    loadLeasingData();
    addFAQStructuredData();
    
    // Initialize FAQ with a small delay to ensure DOM is fully ready
    setTimeout(() => {
        initializeFAQ();
    }, 100);
    
    initializeSmoothScrolling();
    initializeMobileMenu();
    initializeMobileCards();
});

// Mobile menu functionality
function initializeMobileMenu() {
    const hamburger = document.getElementById('nav-hamburger');
    const navMenu = document.getElementById('nav-menu');
    
    if (hamburger && navMenu) {
        hamburger.addEventListener('click', function() {
            hamburger.classList.toggle('active');
            navMenu.classList.toggle('active');
        });
        
        // Close menu when clicking on a link
        const navLinks = navMenu.querySelectorAll('a');
        navLinks.forEach(link => {
            link.addEventListener('click', function() {
                hamburger.classList.remove('active');
                navMenu.classList.remove('active');
            });
        });
        
        // Close menu when clicking outside
        document.addEventListener('click', function(e) {
            if (!hamburger.contains(e.target) && !navMenu.contains(e.target)) {
                hamburger.classList.remove('active');
                navMenu.classList.remove('active');
            }
        });
    }
}

// Mobile cards functionality
function initializeMobileCards() {
    // This function will be called after data is loaded
    // It will create mobile cards based on the loaded data
}

// Function to create mobile cards for bilforsikring
function createBilforsikringMobileCards(data) {
    const container = document.querySelector('.comparison-section .container');
    if (!container) return;
    
    let mobileCardsHTML = '<div class="mobile-cards">';
    
    data.forEach(item => {
        const tilvalgHTML = item.tilvalg.map(tilvalg => 
            `<span class="tilvalg-item">${getTilvalgIcon(tilvalg)} ${tilvalg}</span>`
        ).join('');
        
        mobileCardsHTML += `
            <div class="mobile-card">
                <div class="mobile-card-header">
                    <div class="company-logo">${item.udbyder.charAt(0)}</div>
                    <div>
                        <h3>${item.udbyder}</h3>
                        <p>${item.produkt}</p>
                    </div>
                </div>
                <div class="mobile-card-body">
                    <div class="mobile-card-row">
                        <span class="mobile-card-label">Pris/måned</span>
                        <span class="mobile-card-value price">${item.pris_mdr}</span>
                    </div>
                    <div class="mobile-card-row">
                        <span class="mobile-card-label">Dækning</span>
                        <span class="mobile-card-value">${item.dækning}</span>
                    </div>
                    <div class="mobile-card-row">
                        <span class="mobile-card-label">Tilvalg</span>
                        <span class="mobile-card-value">${tilvalgHTML}</span>
                    </div>
                    ${item.kampagne ? `
                    <div class="mobile-card-row">
                        <span class="mobile-card-label">Kampagne</span>
                        <span class="mobile-card-value">
                            <span class="kampagne ${getKampagneType(item.kampagne)}">${item.kampagne}</span>
                        </span>
                    </div>
                    ` : ''}
                    <div class="mobile-card-cta">
                        <a href="${item.link}" class="btn-primary" target="_blank" rel="noopener">
                            Se tilbud <i class="fas fa-arrow-right"></i>
                        </a>
                    </div>
                </div>
            </div>
        `;
    });
    
    mobileCardsHTML += '</div>';
    
    // Insert mobile cards after trust bar
    const trustBar = container.querySelector('.trust-bar');
    if (trustBar) {
        trustBar.insertAdjacentHTML('afterend', mobileCardsHTML);
    }
}

// Function to create mobile cards for leasing
function createLeasingMobileCards(data) {
    const container = document.querySelector('.comparison-section .container');
    if (!container) return;
    
    let mobileCardsHTML = '<div class="mobile-cards">';
    
    data.forEach(item => {
        mobileCardsHTML += `
            <div class="mobile-card">
                <div class="mobile-card-header">
                    <div class="company-logo">${getCarBrandLogo(item.mærke)}</div>
                    <div>
                        <h3>${item.mærke} ${item.model}</h3>
                        <p>Privatleasing</p>
                    </div>
                </div>
                <div class="mobile-card-body">
                    <div class="mobile-card-row">
                        <span class="mobile-card-label">Pris/måned</span>
                        <span class="mobile-card-value price">${item.pris_mdr}</span>
                    </div>
                    <div class="mobile-card-row">
                        <span class="mobile-card-label">Udbetaling</span>
                        <span class="mobile-card-value">${item.udbetaling}</span>
                    </div>
                    <div class="mobile-card-row">
                        <span class="mobile-card-label">Løbetid</span>
                        <span class="mobile-card-value">${item.løbetid}</span>
                    </div>
                    ${item.kampagne ? `
                    <div class="mobile-card-row">
                        <span class="mobile-card-label">Kampagne</span>
                        <span class="mobile-card-value">
                            <span class="kampagne ${getKampagneType(item.kampagne)}">${item.kampagne}</span>
                        </span>
                    </div>
                    ` : ''}
                    <div class="mobile-card-cta">
                        <a href="${item.link}" class="btn-primary" target="_blank" rel="noopener">
                            Se tilbud <i class="fas fa-arrow-right"></i>
                        </a>
                    </div>
                </div>
            </div>
        `;
    });
    
    mobileCardsHTML += '</div>';
    
    // Insert mobile cards after trust bar
    const trustBar = container.querySelector('.trust-bar');
    if (trustBar) {
        trustBar.insertAdjacentHTML('afterend', mobileCardsHTML);
    }
}

// Helper function to get campaign type
function getKampagneType(kampagne) {
    const kampagneLower = kampagne.toLowerCase();
    if (kampagneLower.includes('gratis') || kampagneLower.includes('gratis')) return 'positive';
    if (kampagneLower.includes('rabat') || kampagneLower.includes('rabat')) return 'standard';
    if (kampagneLower.includes('halv') || kampagneLower.includes('halv')) return 'limited';
    return 'standard';
}

// Function to create new card-based layout for bilforsikring
function createBilforsikringCards(data) {
    const container = document.querySelector('#bilforsikring .container');
    if (!container) return;
    
    // Remove existing cards container if it exists
    const existingCards = container.querySelector('.cards-container');
    if (existingCards) {
        existingCards.remove();
    }
    
    let cardsHTML = '<div class="cards-container">';
    
    data.forEach(item => {
        const badgeClass = getCampaignBadgeClass(item.kampagne);
        const tilvalgHTML = item.tilvalg.map(tilvalg => 
            `<div class="card-feature">${getTilvalgIcon(tilvalg)} ${tilvalg}</div>`
        ).join('');
        
        cardsHTML += `
            <div class="comparison-card">
                ${item.kampagne ? `<div class="card-banner">${item.kampagne}</div>` : ''}
                <div class="card-header">
                    <div class="card-company-logo">${getCompanyInitials(item.udbyder)}</div>
                    <div class="card-company-info">
                        <h3>${item.udbyder}</h3>
                        <p>${item.produkt}</p>
                    </div>
                    <div class="card-rating">
                        <div class="rating-badge">5</div>
                        <div class="rating-stars">
                            <i class="fas fa-star"></i>
                            <i class="fas fa-star"></i>
                            <i class="fas fa-star"></i>
                            <i class="fas fa-star"></i>
                            <i class="fas fa-star"></i>
                        </div>
                    </div>
                </div>
                <div class="card-body">
                    <div class="card-minimum-price">Mindstepris ${item.pris_mdr}</div>
                    <div class="card-details">
                        <div class="card-detail-row">
                            <span class="card-detail-label">Pris måned</span>
                            <span class="card-detail-value price">${item.pris_mdr}</span>
                        </div>
                        <div class="card-detail-row">
                            <span class="card-detail-label">Dækning</span>
                            <span class="card-detail-value">${item.dækning}</span>
                        </div>
                    </div>
                    <div class="card-features">
                        ${tilvalgHTML}
                    </div>
                    <div class="card-cta">
                        <a href="${item.link}" target="_blank" class="btn-primary">Se Tilbud</a>
                    </div>
                </div>
            </div>
        `;
    });
    
    cardsHTML += '</div>';
    
    // Insert cards after trust bar
    const trustBar = container.querySelector('.trust-bar');
    if (trustBar) {
        trustBar.insertAdjacentHTML('afterend', cardsHTML);
    }
}

// Function to create new card-based layout for leasing
function createLeasingCards(data) {
    const container = document.querySelector('#leasing .container');
    if (!container) return;
    
    // Remove existing cards container if it exists
    const existingCards = container.querySelector('.cards-container');
    if (existingCards) {
        existingCards.remove();
    }
    
    let cardsHTML = '<div class="cards-container">';
    
    data.forEach(item => {
        const badgeClass = getCampaignBadgeClass(item.kampagne);
        
        cardsHTML += `
            <div class="comparison-card">
                ${item.kampagne ? `<div class="card-banner">${item.kampagne}</div>` : ''}
                <div class="card-header">
                    <div class="card-company-logo">${getCarBrandLogo(item.mærke)}</div>
                    <div class="card-company-info">
                        <h3>${item.mærke}</h3>
                        <p>${item.model}</p>
                    </div>
                    <div class="card-rating">
                        <div class="rating-badge">5</div>
                        <div class="rating-stars">
                            <i class="fas fa-star"></i>
                            <i class="fas fa-star"></i>
                            <i class="fas fa-star"></i>
                            <i class="fas fa-star"></i>
                            <i class="fas fa-star"></i>
                        </div>
                    </div>
                </div>
                <div class="card-body">
                    <div class="card-minimum-price">Mindstepris ${item.pris_mdr}</div>
                    <div class="card-details">
                        <div class="card-detail-row">
                            <span class="card-detail-label">Pris måned</span>
                            <span class="card-detail-value price">${item.pris_mdr}</span>
                        </div>
                        <div class="card-detail-row">
                            <span class="card-detail-label">Udbetaling</span>
                            <span class="card-detail-value">${item.udbetaling}</span>
                        </div>
                        <div class="card-detail-row">
                            <span class="card-detail-label">Løbetid</span>
                            <span class="card-detail-value">${item.løbetid}</span>
                        </div>
                    </div>
                    <div class="card-features">
                        <div class="card-feature">
                            <i class="fas fa-check"></i>
                            Oprettelse 0,-
                        </div>
                        <div class="card-feature">
                            <i class="fas fa-check"></i>
                            Ingen binding
                        </div>
                    </div>
                    <div class="card-cta">
                        <a href="${item.link}" target="_blank" class="btn-primary">Se Tilbud</a>
                    </div>
                </div>
            </div>
        `;
    });
    
    cardsHTML += '</div>';
    
    // Insert cards after trust bar
    const trustBar = container.querySelector('.trust-bar');
    if (trustBar) {
        trustBar.insertAdjacentHTML('afterend', cardsHTML);
    }
}
