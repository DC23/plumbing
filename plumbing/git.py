# Built-in modules #
import os

# Internal modules #
from plumbing.autopaths import DirectoryPath

# Third party modules #
import sh

###############################################################################
class GitRepo(DirectoryPath):
    """A git repository with some convenience methods."""

    def __init__(self, path):
        # Super #
        DirectoryPath.__init__(self, path)
        # The git directory #
        self.git_dir = self.path + '.git'
        # Check exists #
        if not os.path.exists(self.git_dir):
            raise Exception("No git repository at '%s'" % (self.git_dir))

    @property
    def tag(self):
        tag = sh.git("--git-dir=" + self.git_dir, "describe", "--tags", "--dirty", "--always")
        return tag.strip('\n')

    @property
    def hash(self):
        sha1 = sh.git("--git-dir=" + self.git_dir, "rev-parse", "HEAD")
        return sha1.strip('\n')

    @property
    def branch(self):
        return sh.git("--git-dir=" + self.git_dir, 'symbolic-ref', '--short', 'HEAD').strip('\n')

    @property
    def remote_branch(self):
        return sh.git("--git-dir=" + self.git_dir, 'rev-parse', '--symbolic-full-name', '--abbrev-ref', '@{u}').strip('\n')
