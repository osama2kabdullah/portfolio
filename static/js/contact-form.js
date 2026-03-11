const contactForm = document.querySelector('.contact-form');
const submitButton = contactForm.querySelector('button[type="submit"]');
const messageContainer = contactForm.querySelector('.message');

contactForm.addEventListener('submit', function(event) {
    event.preventDefault();
    submitButton.classList.add('loading');
    const formData = new FormData(contactForm);
    const data = {};
    formData.forEach((value, key) => {
        data[key] = value;
    });

    fetch(contactForm.action, {
        method: contactForm.method,
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (!response.ok) {
          messageContainer.textContent = 'মেসেজ পাঠাতে সমস্যা হয়েছে। আবার চেষ্টা করুন।';
          messageContainer.style.display = 'block';
        }
        messageContainer.textContent = 'মেসেজ সফলভাবে পাঠানো হয়েছে!';
        messageContainer.style.display = 'block';
        contactForm.reset();
    })
    .catch(error => {
        console.error('Error:', error);
        // Handle error (e.g., show an error message)
        messageContainer.textContent = 'মেসেজ পাঠাতে সমস্যা হয়েছে। আবার চেষ্টা করুন।';
        messageContainer.style.display = 'block';
    })
    .finally(() => {
        submitButton.classList.remove('loading');
        setTimeout(() => {
          messageContainer.textContent = '';
          messageContainer.style.display = 'none';
        }, 10000);
    });
});