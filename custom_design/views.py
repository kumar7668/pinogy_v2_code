import json
from ast import literal_eval

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import HttpResponseRedirect, render
from django.urls import reverse
from django.views.generic import FormView, View

from custom_design.forms import ThemeConfigurationForm
from custom_design.models import ThemeConfiguration, ThemeImages


class ThemeChangeView(FormView):
    template_name = "theme-change-form.html"

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, "Theme saved successfully")
        return reverse("admin:index")

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            theme = ThemeConfiguration.objects.filter(id=1).first()
            form = ThemeConfigurationForm(instance=theme)
            context = {"form": form}
            context["theme"] = theme
            context["logos"] = ThemeImages.objects.filter(image_type="logo")
            context["favicons"] = ThemeImages.objects.filter(image_type="favicon")
            context["backgrounds"] = ThemeImages.objects.filter(image_type="background")
            return render(request, self.template_name, context)
        return HttpResponseRedirect("/")

    def post(self, request, *args, **kwargs):
        form = ThemeConfigurationForm(request.POST or None, request.FILES)
        if form.is_valid():

            if request.FILES.get("theme_json"):
                templatefile = request.FILES.get("theme_json")
                read_file = templatefile.read()
                formdata = literal_eval(read_file.decode("utf8"))
                form1 = ThemeConfigurationForm(formdata)

                if form1.is_valid():
                    theme = form1.save(commit=False)
                else:
                    return self.form_invalid(form1)
            else:
                theme = form.save(commit=False)

            logos = request.FILES.getlist("logo")
            if logos:
                for logo in logos:
                    logoobj = ThemeImages(image=logo, image_type="logo")
                    logoobj.save()
                    theme.selected_logo = logoobj

            favicons = request.FILES.getlist("favicon")
            selected_favicon = request.POST.get('selected_favicon')
            if favicons:
                for favicon in favicons:
                    if selected_favicon == favicon.name:
                        faviconobj = ThemeImages(image=favicon, image_type="favicon")
                        faviconobj.save()
                        selected_favicon = faviconobj.id
                    faviconobj = ThemeImages(image=favicon, image_type="favicon")
                    faviconobj.save()
            backgrounds = request.FILES.getlist("background")
            selected_background = request.POST.get('select_background')
            if backgrounds:
                for background in backgrounds:
                    backgroundobj = ThemeImages(image=background, image_type="background")
                    backgroundobj.save()
                    theme.selected_background = backgroundobj
            if selected_background and ThemeImages.objects.filter(id = selected_background).exists():
                theme.selected_background_id = int(selected_background)
            if selected_favicon and ThemeImages.objects.filter(id = selected_favicon).exists():
                theme.selected_favicon_id = int(selected_favicon)
            theme.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class ThemeImageView(View):
    def post(self, request, *args, **kwargs):
        addedLogo = None
        logofile = request.FILES.get("logoimage")
        if logofile:
            addedLogo = ThemeImages(image=logofile, image_type="logo")
            addedLogo.save()
        if addedLogo:
            return HttpResponse(
                json.dumps(
                    {
                        "message": "Image uploaded succesfully.",
                        "id": addedLogo.id,
                        "url": addedLogo.image.url,
                    }
                ),
                status=200,
            )
        else:
            return HttpResponse(
                json.dumps({"message": "Something went wrong."}), status=400
            )

    def delete(self, request, *args, **kwargs):
        json_data = json.loads(request.body)
        deleted_img = ThemeImages.objects.filter(id=json_data["image_id"]).delete()
        if deleted_img:
            return HttpResponse(
                json.dumps(
                    {
                        "message": "Image deleted succesfully",
                    }
                ),
                status=200,
            )
        else:
            return HttpResponse(
                json.dumps(
                    {
                        "message": "Something went wrong.",
                    }
                ),
                status=400,
            )
