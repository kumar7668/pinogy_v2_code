$(document).ready(function() {
    // Phone number field validation
    $('.phone-validation').on('input', function() {
        /*
            Add "phone-validation" class to validate field as phone number
            Add <div class="invalid-feedback">Please enter a valid 10-digit number.</div> to display the error message
        */
        var $phoneInput = $(this);
        var rawValue = $phoneInput.val();
        var unmaskedValue = rawValue.replace(/\D/g, '');
        var isPlusOneFormat = rawValue.startsWith('+');

        if (isPlusOneFormat) {
            $phoneInput.val(formatPlusOne(unmaskedValue));
            $phoneInput.attr('maxlength', 17); // +1 (123) 456-7890 -> 17 characters
            validateInput($phoneInput, /^1\d{10}$/, "Please enter a 11 digit phone number starting with 1");
        } else {
            $phoneInput.val(formatStandard(unmaskedValue));
            $phoneInput.attr('maxlength', 14); // (123) 456-7890 -> 14 characters
            validateInput($phoneInput, /^\d{10}$/, "Please enter a 10 digit phone number");
        }
    });

    function formatPlusOne(unmaskedValue) {
        var maskedValue = '+';
        for (var i = 0; i < unmaskedValue.length; i++) {
            if (i === 1) maskedValue += ' (';
            if (i === 4) maskedValue += ') ';
            if (i === 7) maskedValue += '-';
            maskedValue += unmaskedValue[i];
        }
        return maskedValue;
    }

    function formatStandard(unmaskedValue) {
        var maskedValue = '';
        for (var i = 0; i < unmaskedValue.length; i++) {
            if (i === 0) maskedValue += '(';
            if (i === 3) maskedValue += ') ';
            if (i === 6) maskedValue += '-';
            maskedValue += unmaskedValue[i];
        }
        return maskedValue;
    }

    function validateInput($input, pattern, errorMessage) {
        var unmaskedValue = $input.val().replace(/\D/g, '');
        if (unmaskedValue.length === 0 || pattern.test(unmaskedValue)) {
            $input.get(0).setCustomValidity("");
            $input.removeClass('is-invalid');
            $input.next('.invalid-feedback').hide();
        } else {
            $input.get(0).setCustomValidity(errorMessage);
            $input.addClass('is-invalid');
            $input.next('.invalid-feedback').text(errorMessage).show();
        }
    }
});