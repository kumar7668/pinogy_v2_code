(function($) {
    /*
        Example usage:
        $('#country_dropdown_ID').loadRegionDropdown({
            countryDropdownId: '#country_dropdown_ID', 
            stateDropdownId: '#state_dropdown_ID', 
            apiUrl: '{% url "pinogy_shop_proxy:get_regions" %}', 
            valueKey: 'prgn_iso_code', // Specify the key for the region code
            onRegionsLoaded: function() {  // optional callback  }
        });
    */

    $.fn.loadRegionDropdown = function(options) {
        // Default settings
        var settings = $.extend({
            countryDropdownId: null,
            stateDropdownId: null,
            apiUrl: null,
            valueKey: 'prgn_iso_code',  // Default key for region code; can be customized
            onRegionsLoaded: null  
        }, options);

        if (!settings.countryDropdownId || !settings.stateDropdownId) {
            console.error('Country and state dropdown IDs must be specified.');
            return this;
        }

        if (!settings.apiUrl) {
            console.error('API URL must be specified.');
            return this;
        }

        function loadRegions(countryId, $stateDropdown) {
            $.ajax({
                url: settings.apiUrl,
                type: 'GET',
                data: { region_id: countryId },
                success: function(response) {
                    $stateDropdown.empty();
                    $stateDropdown.append('<option value=""></option>');  // Placeholder option

                    $.each(response.regions, function(index, region) {
                        var regionCode = region[settings.valueKey];  // Dynamically get the value using valueKey
                        var regionName = region.prgn_full_name;
                        
                        if (regionCode !== undefined) {
                            $stateDropdown.append(
                                $('<option></option>').val(regionCode).text(regionName)
                            );
                        }
                    });

                    if (typeof settings.onRegionsLoaded === 'function') {
                        settings.onRegionsLoaded();
                    }
                },
                error: function() {
                    alert("Failed to load regions. Please try again.");
                }
            });
        }

        var $countryDropdown = $(settings.countryDropdownId);
        var $stateDropdown = $(settings.stateDropdownId);

        $countryDropdown.on('change', function() {
            var countryId = $(this).val();
            if (countryId) {
                loadRegions(countryId, $stateDropdown);
            } else {
                $stateDropdown.empty();
            }
        });

        return this;
    };
})(jQuery);
