import freetype
import subprocess
import shlex

__all__ = 'Face',


def capture_stdout(cmd):
    proc = subprocess.Popen(
        shlex.split(cmd),
        stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    stdout, stderr = proc.communicate()
    return stdout.decode()


def fc_match(pattern, *fields):
    format_ = '\n'.join(map(lambda field: '%{' + field + '}', fields))
    data = capture_stdout(f'fc-match --format="{format_}" "{pattern}"')
    return data.splitlines()


class Face(freetype.Face):
    @classmethod
    def from_pattern(cls, pattern):
        file, = fc_match(pattern, 'file')
        return cls(file)

    def __repr__(self):
        qualname = self.__class__.__qualname__
        return f'{qualname}({self._filename !r})'
