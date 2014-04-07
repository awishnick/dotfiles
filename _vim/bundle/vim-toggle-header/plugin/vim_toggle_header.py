import vim
import os.path


_EXTENSIONS = {
    'h': ['cpp', 'c'],
    'cpp': ['h', 'hpp'],
}


def _generate_toggle_filenames(path):
    """Generate potential filenames that can be toggled to from path."""
    base, ext = os.path.splitext(path)

    if ext:
        ext = ext[1:]

    try:
        extensions = _EXTENSIONS[ext]
    except KeyError:
        return

    for extension in extensions:
        yield base + '.' + extension


def toggle():
    buffer_path = vim.eval('@%')

    for candidate in _generate_toggle_filenames(buffer_path):
        if not os.path.exists(candidate):
            continue

        vim.command(':e {}'.format(candidate))
        return
