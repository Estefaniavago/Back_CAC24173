document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('maestroForm');
    const dniInput = document.getElementById('txtDni');
    
    form.addEventListener('submit', function (event) {
        // Validación personalizada para el DNI
        const dniValue = dniInput.value;
        const dniPattern = /^\d{8}$/;
        
        if (!dniPattern.test(dniValue)) {
            dniInput.setCustomValidity('El DNI debe tener exactamente 8 dígitos.');
        } else {
            dniInput.setCustomValidity('');
        }
        
        // Validar el formulario
        if (!form.checkValidity()) {
            event.preventDefault();
            event.stopPropagation();
        }
        form.classList.add('was-validated');
    }, false);
    
    // Remover el mensaje de error personalizado al corregir el campo
    dniInput.addEventListener('input', function () {
        if (dniInput.validity.patternMismatch) {
            dniInput.setCustomValidity('El DNI debe tener exactamente 8 dígitos.');
        } else {
            dniInput.setCustomValidity('');
        }
    });
});