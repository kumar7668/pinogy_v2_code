def update_new_path(old_path, new_path):
    parts = old_path.split(new_path)
    if len(parts) < 2:
        return new_path

    transfer_part = parts[1].split('?')[0]
    new_path += transfer_part
    return new_path


def log_404(path):
    from .models import PathLog, NotFoundLog

    path_log = PathLog.objects.log_path(path=path)[0]
    NotFoundLog.objects.log_not_found(path_log=path_log)
