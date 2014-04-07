import vim
import os.path
import subprocess
import sys


def _recurse_up(path):
    cur_path = os.path.dirname(os.path.abspath(path))

    while True:
        yield cur_path

        new_path = os.path.dirname(cur_path)
        if new_path == cur_path:
            break
        cur_path = new_path


def _find_xcode_projects_in_directory(path):
    if not os.path.exists(path):
        return []
    if not os.path.isdir(path):
        return []
    return [os.path.join(path, d) for d in os.listdir(path) if
            os.path.isdir(os.path.join(path, d)) and
            d.endswith('.xcodeproj')]


def find_xcode_project():
    """Search upwards from the current buffer for an Xcode project."""
    buffer_path = vim.current.buffer.name
    for path in _recurse_up(buffer_path):
        projects = _find_xcode_projects_in_directory(path)
        if projects:
            return projects[0]

        # Is there a build directory?
        build_path = os.path.join(path, 'build')
        projects = _find_xcode_projects_in_directory(build_path)
        if projects:
            return projects[0]

    return None


_PROJECT_SCHEMES = dict()


def _get_project_scheme(xcode_project, action):
    filename = os.path.basename(xcode_project)
    schemes_for_actions = _PROJECT_SCHEMES.get(find_xcode_project(), {})
    default_scheme = os.path.splitext(filename)[0]
    return schemes_for_actions.get(action, default_scheme)


def _set_project_scheme(xcode_project, action, scheme):
    try:
        schemes = _PROJECT_SCHEMES[xcode_project]
    except KeyError:
        _PROJECT_SCHEMES[xcode_project] = {}
        schemes = _PROJECT_SCHEMES[xcode_project]
    schemes[action] = scheme


def set_build_scheme(scheme):
    _set_project_scheme(find_xcode_project(), 'build', scheme)


def set_test_scheme(scheme):
    _set_project_scheme(find_xcode_project(), 'test', scheme)


def _run_build_action(action, success_msg):
    proj = find_xcode_project()
    if not proj:
        return

    args = ['xcodebuild', '-project', proj]

    scheme = _get_project_scheme(proj, action)
    if scheme:
        args.extend(['-scheme', scheme])

    args.append(action)

    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (stdoutdata, stderrdata) = p.communicate()
    if p.returncode == 0:
        print(success_msg)
    else:
        sys.stdout.write(stdoutdata)
        sys.stderr.write(stderrdata)


def test():
    """Run unit tests."""
    _run_build_action('test', 'Tests passed.')


def build():
    """Build the project."""
    _run_build_action('build', 'Finished building.')
