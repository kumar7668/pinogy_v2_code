!function($){"use strict";$(function(){$(".testimonial-form-plugin input[type=submit]").on("click",function(r){function i(r){r.pk?(s.siblings(".success").html(r.success).show(100),s.add(".legend").hide(100)):(s.find(".error").empty(),$.each(r,function(r,i){var e=s.find("input[name="+r+"]").first();e.parents(".field-wrapper").find(".error").html(i.join(" "))}),r.__all__?s.siblings(".errors").find(".form-errors").html(r.__all__.join(" ")):s.siblings(".errors").find(".form-errors").empty(),s.siblings(".errors").show(100))}var s=$(this).parents("form").eq(0);r.preventDefault(),s.siblings(".errors, .success").hide(100),$.ajax({type:"POST",url:s.attr("action"),data:s.serialize()}).always(i)})})}(window.jQuery);