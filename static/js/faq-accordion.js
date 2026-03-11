const faqs = document.querySelectorAll('.faq-item');

faqs.forEach((faq) => {
    const faqHeader = faq.querySelector('h4');
    const p = faqHeader.nextElementSibling;
    p.style.maxHeight = '0';
    p.style.overflow = 'hidden';
    p.style.transition = 'max-height 0.1s ease';

    faqHeader.style.cursor = 'pointer';

    
    faqHeader.addEventListener('click', function() {
      if (p.style.maxHeight === '0px' || p.style.maxHeight === '0') {
          p.style.maxHeight = p.scrollHeight + 'px';
          faq.appendChild(document.createElement('br'));
        } else {
            p.style.maxHeight = '0';
            faq.removeChild(faq.lastChild);
        }
    });
});