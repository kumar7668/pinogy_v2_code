from django.db import models
from django.db.models import Count, Max, Min


class RedirectApplicationManager(models.Manager):

    def get_app_redirect_by(self, sub_path):
        url_parts = ['/{}/'.format(part) for part in sub_path.split('/') if part]
        res = super().get_queryset().filter(old_path_application__in=url_parts).first()
        return res

    def get_redirected_path(self, old_path):
        redirect_model = self.get_app_redirect_by(sub_path=old_path)
        return redirect_model.get_new_path(old_path) if redirect_model else None


class PathLogManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().annotate(
            first_log=Min('logs__logged_at'), last_log=Max('logs__logged_at'), log_count=Count('logs')
        )

    def log_path(self, path):
        truncated_path = path[:200]  # Take only the first 200 characters
        return super().get_queryset().get_or_create(path=truncated_path)

class NotFoundLogManager(models.Manager):

    def log_not_found(self, path_log):
        return super().get_queryset().create(path_log=path_log)