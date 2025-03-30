document.addEventListener('DOMContentLoaded', function() {
    document.addEventListener('click', function(e) {
        if(e.target.classList.contains('remove-btn')) {
            const productName = e.target.closest('.cart-item').getAttribute('data-product');
            if(confirm(`Vai tiešām vēlaties noņemt "${productName}" no groza?`)) {
                const form = document.createElement('form');
                form.method = 'POST';
                form.action = '/remove_from_cart';
                
                const input = document.createElement('input');
                input.type = 'hidden';
                input.name = 'perfume_name';
                input.value = productName;
                
                form.appendChild(input);
                document.body.appendChild(form);
                form.submit();
            }
        }
    });

    const completeOrderBtn = document.getElementById('complete-order');
    if(completeOrderBtn) {
        completeOrderBtn.addEventListener('click', function() {
            if(confirm('Vai tiešām vēlaties pabeigt pasūtījumu?')) {
                const form = document.createElement('form');
                form.method = 'POST';
                form.action = '/complete_order';
                document.body.appendChild(form);
                form.submit();
            }
        });
    }

    const addToCartForms = document.querySelectorAll('form[action="/add_to_cart"]');
    addToCartForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const quantityInput = this.querySelector('input[name="quantity"]');
            const quantity = parseInt(quantityInput.value);
            
            if(isNaN(quantity) || quantity < 1) {
                alert('Lūdzu, ievadiet derīgu daudzumu (vismaz 1)!');
                e.preventDefault();
            } else {
                const submitBtn = this.querySelector('button[type="submit"]');
                if(submitBtn) {
                    submitBtn.disabled = true;
                    submitBtn.textContent = 'Pievieno...';
                }
            }
        });
    });
});
