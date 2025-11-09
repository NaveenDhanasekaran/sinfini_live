// Main JavaScript for Sinfini Marketing website

// Mobile menu toggle
function toggleMobileMenu() {
    const mobileMenu = document.getElementById('mobile-menu');
    mobileMenu.classList.toggle('hidden');
}

// Chatbot functionality
let chatbotOpen = false;

function toggleChatbot() {
    const chatWindow = document.getElementById('chatbot-window');
    chatbotOpen = !chatbotOpen;
    
    if (chatbotOpen) {
        chatWindow.classList.remove('hidden');
        loadChatbotSettings();
    } else {
        chatWindow.classList.add('hidden');
    }
}

// Load chatbot settings
async function loadChatbotSettings() {
    try {
        const response = await fetch('/api/chatbot/settings');
        const settings = await response.json();
        
        if (settings.greeting) {
            addChatMessage(settings.greeting, 'bot');
        }
    } catch (error) {
        console.error('Error loading chatbot settings:', error);
    }
}

// Send chat message
async function sendMessage() {
    const input = document.getElementById('chat-input');
    const message = input.value.trim();
    
    if (!message) return;
    
    // Add user message
    addChatMessage(message, 'user');
    input.value = '';
    
    // Show typing indicator
    const typingId = addChatMessage('Typing...', 'bot', true);
    
    try {
        const response = await fetch('/api/chatbot/message', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message })
        });
        
        const data = await response.json();
        
        // Remove typing indicator
        document.getElementById(typingId).remove();
        
        // Add bot response
        addChatMessage(data.response, 'bot');
        
    } catch (error) {
        console.error('Error sending message:', error);
        document.getElementById(typingId).remove();
        addChatMessage('Sorry, I encountered an error. Please try again.', 'bot');
    }
}

// Add message to chat
function addChatMessage(message, sender, isTyping = false) {
    const messagesContainer = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    const messageId = 'msg-' + Date.now();
    
    messageDiv.id = messageId;
    messageDiv.className = `chat-message ${sender}`;
    
    if (sender === 'user') {
        messageDiv.innerHTML = `<div class="message">${message}</div>`;
    } else {
        const messageClass = isTyping ? 'message loading-message' : 'message';
        messageDiv.innerHTML = `<div class="${messageClass}">${isTyping ? '<span class="loading"></span> ' + message : message}</div>`;
    }
    
    messagesContainer.appendChild(messageDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
    
    return messageId;
}

// Handle Enter key in chat input
document.addEventListener('DOMContentLoaded', function() {
    const chatInput = document.getElementById('chat-input');
    if (chatInput) {
        chatInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    }
    
    // Chatbot toggle button
    const chatToggle = document.getElementById('chatbot-toggle');
    if (chatToggle) {
        chatToggle.addEventListener('click', toggleChatbot);
    }
});

// Modal functionality
function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add('show');
        document.body.style.overflow = 'hidden';
    }
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('show');
        document.body.style.overflow = 'auto';
    }
}

// Close modal when clicking outside
document.addEventListener('click', function(e) {
    if (e.target.classList.contains('modal')) {
        e.target.classList.remove('show');
        document.body.style.overflow = 'auto';
    }
});

// Form submission with loading states
function submitForm(formId, endpoint, successCallback) {
    const form = document.getElementById(formId);
    const submitBtn = form.querySelector('button[type="submit"]');
    const originalText = submitBtn.innerHTML;
    
    // Show loading state
    submitBtn.innerHTML = '<span class="loading"></span> Sending...';
    submitBtn.disabled = true;
    
    const formData = new FormData(form);
    
    fetch(endpoint, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            showAlert(data.error, 'error');
        } else {
            showAlert(data.message || 'Success!', 'success');
            if (successCallback) successCallback(data);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showAlert('An error occurred. Please try again.', 'error');
    })
    .finally(() => {
        // Reset button
        submitBtn.innerHTML = originalText;
        submitBtn.disabled = false;
    });
}

// Show alert messages
function showAlert(message, type = 'success') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} fixed top-4 right-4 z-50 max-w-sm`;
    alertDiv.innerHTML = `
        <div class="flex justify-between items-center">
            <span>${message}</span>
            <button onclick="this.parentElement.parentElement.remove()" class="ml-4 text-lg">&times;</button>
        </div>
    `;
    
    document.body.appendChild(alertDiv);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (alertDiv.parentElement) {
            alertDiv.remove();
        }
    }, 5000);
}

// Smooth scrolling for anchor links
document.addEventListener('DOMContentLoaded', function() {
    const links = document.querySelectorAll('a[href^="#"]');
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
});

// Image lazy loading
function lazyLoadImages() {
    const images = document.querySelectorAll('img[data-src]');
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
}

// Initialize lazy loading when DOM is ready
document.addEventListener('DOMContentLoaded', lazyLoadImages);

// Product modal functionality
function openProductModal(productId) {
    fetch(`/api/products/${productId}`)
        .then(response => response.json())
        .then(product => {
            const modal = document.getElementById('product-modal');
            const modalContent = modal.querySelector('.modal-content');
            
            modalContent.innerHTML = `
                <div class="flex justify-between items-center mb-4">
                    <h2 class="text-2xl font-bold text-navy-800">${product.name}</h2>
                    <button onclick="closeModal('product-modal')" class="text-gray-500 hover:text-gray-700">
                        <i class="fas fa-times text-xl"></i>
                    </button>
                </div>
                ${product.image_url ? `<img src="${product.image_url}" alt="${product.name}" class="w-full h-64 object-cover rounded-lg mb-4">` : ''}
                <div class="mb-4">
                    <span class="bg-gold-100 text-gold-800 px-3 py-1 rounded-full text-sm font-medium">${product.category}</span>
                </div>
                <p class="text-gray-600 leading-relaxed">${product.description}</p>
                <div class="mt-6 flex space-x-4">
                    <button onclick="closeModal('product-modal')" class="flex-1 bg-gray-200 hover:bg-gray-300 text-gray-800 py-2 px-4 rounded-lg transition-colors">
                        Close
                    </button>
                    <a href="/contact" class="flex-1 btn-primary text-center">
                        Get Quote
                    </a>
                </div>
            `;
            
            openModal('product-modal');
        })
        .catch(error => {
            console.error('Error loading product:', error);
            showAlert('Error loading product details', 'error');
        });
}

// Gallery lightbox
function openGalleryLightbox(mediaUrl, mediaType, title) {
    const modal = document.getElementById('gallery-modal');
    const modalContent = modal.querySelector('.modal-content');
    
    const mediaElement = mediaType === 'video' 
        ? `<video controls class="w-full max-h-96 rounded-lg"><source src="${mediaUrl}" type="video/mp4"></video>`
        : `<img src="${mediaUrl}" alt="${title}" class="w-full max-h-96 object-contain rounded-lg">`;
    
    modalContent.innerHTML = `
        <div class="flex justify-between items-center mb-4">
            <h2 class="text-xl font-bold text-navy-800">${title}</h2>
            <button onclick="closeModal('gallery-modal')" class="text-gray-500 hover:text-gray-700">
                <i class="fas fa-times text-xl"></i>
            </button>
        </div>
        ${mediaElement}
    `;
    
    openModal('gallery-modal');
}

// Contact form submission
function submitContactForm() {
    const form = document.getElementById('contact-form');
    const formData = new FormData(form);
    const data = Object.fromEntries(formData);
    
    const submitBtn = form.querySelector('button[type="submit"]');
    const originalText = submitBtn.innerHTML;
    
    submitBtn.innerHTML = '<span class="loading"></span> Sending...';
    submitBtn.disabled = true;
    
    fetch('/api/contact', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        showAlert(data.message, 'success');
        form.reset();
    })
    .catch(error => {
        console.error('Error:', error);
        showAlert('Error sending message. Please try again.', 'error');
    })
    .finally(() => {
        submitBtn.innerHTML = originalText;
        submitBtn.disabled = false;
    });
}
