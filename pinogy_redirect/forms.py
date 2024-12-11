from django import forms
from .models import RedirectApplication


class RedirectApplicationForm(forms.ModelForm):

    class Meta:
        model = RedirectApplication
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(RedirectApplicationForm, self).__init__(*args, **kwargs)
        app_gen = iter(self.fields['page_application'].choices)
        choices = [next(app_gen)]
        for page in self.fields['page_application'].queryset.filter(publisher_is_draft=True):
            level = page.node.get_depth() - 1
            label = ''.join(['-' * level, str(page)])
            choices.append((page.id, label))
        self.fields['page_application'].choices = choices

    def clean(self):
        form_data = self.cleaned_data
        target, extra_part = form_data['old_path_application'], form_data['extra_part']
        app_path = form_data['page_application'].get_absolute_url()
        unique_list = [app_path] if extra_part == '' else [app_path, extra_part]
        for unique in unique_list:
            if target in unique or unique in target:
                self.add_error('old_path_application', "This path is exists on application")
                break

        return super().clean()
