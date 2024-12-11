$(document).ready(function () {

    // Initialize coloris color picker
    Coloris({
        el: '.coloris'
    });
    Coloris.setInstance('.instance1', {
        theme: 'default', format: 'auto', forceAlpha: true, defaultColor: '#000000ff',formatToggle: true,
    })

    // Update color when user clicks on pallete
    $(".theme-color-tab").on('click', 'li', function () {
        // Setting active-border class
        $(this).parent().find("li.active-border").removeClass("active-border");
        $(this).addClass("active-border");

        // Setting selected color value in input box
        const text_box_id = $(this).parent().data("id")
        const color_value = $(this).data('value')
        if (color_value) {
            $(`#${text_box_id}`).val(color_value)
            $(this).parent().find('li.custom-color').children().first().css({'color' : "#0fbcd2ff", "background-color" : "white", "border" : '1px solid #0fbcd2ff'})
        }
    });

    // Check if custom color is selected add active-border class
    $(".theme-color-tab").each(function () {
        const active_elem = $(this).find("li.active-border")
        if (!active_elem.length) {
            $(this).find("li.custom-color").addClass("active-border")
            
            if ($(this).find('.color-selector').val() == 'None'){
                $(this).find('li.custom-color').children().first().css({'background-color' : 'white', "color" : '#0fbcd2ff', 'border' : '1px solid #0fbcd2ff'})
            }
            else{
                $(this).find('li.custom-color').children().first().css({'background-color' : $(this).find('.color-selector').val(), "color" : 'white'})
            }
        }
    })
    document.addEventListener('coloris:pick', event => {
        let new_id = event.detail.currentEl.id
        $(`.${new_id}`).css({'background-color': event.detail.color,'color' : 'white', "border" : `1px solid ${event.detail.color}`})
      });
});

// When coloris value is changed we are setting in hidden input
function setColorValue(value, text_box_id) {
    $(`#${text_box_id}`).val(value)
}
