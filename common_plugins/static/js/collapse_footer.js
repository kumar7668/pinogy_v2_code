
$(document).ready(function(){

    function closeFooterElement() {
        $(".contact-us").hide();        
        if ($(".contact-sym").html() ==='-'){
            $(".contact-sym").html('+');
        }

        $(".contact-us2").hide();        
        if ($(".contact-sym2").html() ==='-'){
            $(".contact-sym2").html('+');
        }

        $(".store-hours-links").hide();
        if ($(".store-sym").html() ==='-'){
            $(".store-sym").html('+');
        }

        $(".quick-links").hide();
        if ($(".quick-link-sym").html() ==='-'){
            $(".quick-link-sym").html('+');
        }
    }

    function openFooterElement(){
        $(".contact-us").show();        
        if ($(".contact-sym").html() ==='+'){
            $(".contact-sym").html('-');
        }

        $(".contact-us2").show();        
        if ($(".contact-sym2").html() ==='+'){
            $(".contact-sym2").html('-');
        }

        $(".store-hours-links").show();
        if ($(".store-sym").html() ==='+'){
            $(".store-sym").html('-');
        }

        $(".quick-links").show();
        if ($(".quick-link-sym").html() ==='+'){
            $(".quick-link-sym").html('-');
        }
    }
    
    // By default collapse all the footer element
    if ($(window).width() <= 575) {
        closeFooterElement()
    }

    function resize() {
        if ($(window).width() > 575 ) {
            openFooterElement()
        }else{
            closeFooterElement()
        }
    }
    
    $(window).on('resize', function() {
        resize()
    });
     
    // Changing the collapse/expand symbol accordingly onClick event
    $(".contact-sym").click(function(){
        let sign = $(this).html();
        if (sign === '-'){
        $(this).html('+') ; 
        $(".contact-us").hide();        
        }
        else{
        $(this).html('-');
        $(".contact-us").show();
        }
    });

    // Changing the collapse/expand symbol accordingly onClick event
    $(".contact-sym2").click(function(){
        let sign = $(this).html();
        if (sign === '-'){
        $(this).html('+') ; 
        $(".contact-us2").hide();        
        }
        else{
        $(this).html('-');
        $(".contact-us2").show();
        }
    });
    
    // changing the collapse/expand symbol accordingly onClick event
    $(".store-sym").click(function(){
    let sign = $(this).html();
    if (sign === '-'){
        $(this).html('+') ; 
        $(".store-hours-links").hide();
    }
    else{
        $(this).html('-');
        $(".store-hours-links").show();
    }
    });

    // changing the collapse/expand symbol accordingly onClick event
    $(".quick-link-sym").click(function(){
    let sign = $(this).html();
    if (sign === '-'){
        $(this).html('+') ; 
        $(".quick-links").hide();
    }
    else{
        $(this).html('-');
        $(".quick-links").show();
    }
    });

});
