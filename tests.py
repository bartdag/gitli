import gitli
import unittest
import tempfile
import shutil
import os
from subprocess import call
from collections import namedtuple


def read_file(file_type):
    content = ''
    with open(os.path.join(gitli.GITLIDIR, file_type)) as f:
        content = f.read()
    return content


def read_lines(file_type):
    content = []
    with open(os.path.join(gitli.GITLIDIR, file_type)) as f:
        content = f.readlines()
    return content


def exists(file_type):
    return os.path.exists(os.path.join(gitli.GITLIDIR, file_type))


class TestGitli(unittest.TestCase):

    def setUp(self):
        self.tempdirpath = tempfile.mkdtemp()
        os.chdir(self.tempdirpath)
        self.gitlipath = os.path.join(self.tempdirpath, gitli.GITLIDIR)
        self.Options = namedtuple('Options', 'edit')

    def tearDown(self):
        shutil.rmtree(self.tempdirpath)

    def test_init(self):
        call(['git', 'init'])
        gitli.main(None, ['init', ], None)
        self.assertTrue(exists(gitli.ISSUES))
        self.assertTrue(exists(gitli.OPEN))
        self.assertTrue(exists(gitli.LAST))
        self.assertTrue(exists(gitli.CURRENT))
        self.assertTrue(exists(gitli.COMMENTS))
        self.assertEqual(read_file(gitli.CURRENT), '0.1')
        self.assertEqual(read_file(gitli.LAST), '0')

    def test_new(self):
        options = self.Options(edit=False)
        call(['git', 'init'])
        gitli.main(None, ['init', ], None)
        gitli.main(options, ['new', 'Hello World 1'], None)
        lines = read_lines(gitli.ISSUES)
        self.assertEqual('1', lines[0].strip())
        self.assertEqual('Hello World 1', lines[1].strip())
        self.assertEqual('1', lines[2].strip())
        self.assertEqual('0.1', lines[3].strip())
        self.assertEqual('1', read_file(gitli.LAST))
