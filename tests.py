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
        self.Options = namedtuple('Options', 'edit up')
        self.bcolor = gitli.BColors()
        self.bcolor.disable()

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
        options = self.Options(edit=False, up=False)
        call(['git', 'init'])
        gitli.main(None, ['init', ], None)
        gitli.main(options, ['new', 'Hello World 1'], None)
        lines = read_lines(gitli.ISSUES)
        self.assertEqual('1', lines[0].strip())
        self.assertEqual('Hello World 1', lines[1].strip())
        self.assertEqual('1', lines[2].strip())
        self.assertEqual('0.1', lines[3].strip())
        self.assertEqual('1', read_file(gitli.LAST))
        lines = read_lines(gitli.OPEN)
        self.assertEqual('1', lines[0].strip())

    def test_remove(self):
        options = self.Options(edit=False, up=False)
        call(['git', 'init'])
        gitli.main(None, ['init', ], None)
        gitli.main(options, ['new', 'Hello World 1'], None)
        gitli.main(options, ['new', 'Hello World 2'], None)
        gitli.main(options, ['new', 'Hello World 3'], None)
        gitli.main(options, ['remove', '2'], None)
        lines = read_lines(gitli.ISSUES)
        self.assertEqual('1', lines[0].strip())
        self.assertEqual('3', lines[4].strip())
        self.assertEqual('3', read_file(gitli.LAST))
        lines = read_lines(gitli.OPEN)
        self.assertEqual('1', lines[0].strip())
        self.assertEqual('3', lines[1].strip())
        gitli.main(options, ['remove', '3'], None)
        gitli.main(options, ['remove', '1'], None)
        self.assertEqual('', read_file(gitli.ISSUES).strip())
        self.assertEqual('3', read_file(gitli.LAST).strip())
        self.assertEqual('', read_file(gitli.OPEN).strip())

    def test_list_issues(self):
        options = self.Options(edit=False, up=False)
        call(['git', 'init'])
        gitli.main(None, ['init', ], None)
        gitli.main(options, ['new', 'Hello World 1'], None)
        gitli.main(options, ['new', 'Hello World 2'], None)
        gitli.main(options, ['new', 'Hello World 3'], None)
        gitli.main(options, ['close', '2'], None)
        issues = gitli.list_issues(self.gitlipath, [], self.bcolor)
        self.assertEqual(3, len(issues))
        issues = gitli.list_issues(self.gitlipath, ['all'], self.bcolor)
        self.assertEqual(3, len(issues))
        issues = gitli.list_issues(self.gitlipath, ['open'], self.bcolor)
        self.assertEqual(2, len(issues))
        issues = gitli.list_issues(self.gitlipath, ['close'], self.bcolor)
        self.assertEqual(1, len(issues))

    def test_list_issues_default(self):
        options = self.Options(edit=False, up=False)
        call(['git', 'init'])
        call(['git', 'config', '--add', 'gitli.list.option', 'open'])
        gitli.main(None, ['init', ], None)
        gitli.main(options, ['new', 'Hello World 1'], None)
        gitli.main(options, ['new', 'Hello World 2'], None)
        gitli.main(options, ['new', 'Hello World 3'], None)
        gitli.main(options, ['close', '2'], None)
        issues = gitli.list_issues(self.gitlipath, [], self.bcolor)
        self.assertEqual(2, len(issues))
        issues = gitli.list_issues(self.gitlipath, ['all'], self.bcolor)
        self.assertEqual(3, len(issues))
        issues = gitli.list_issues(self.gitlipath, ['open'], self.bcolor)
        self.assertEqual(2, len(issues))
        issues = gitli.list_issues(self.gitlipath, ['close'], self.bcolor)
        self.assertEqual(1, len(issues))

    def test_set_milestone(self):
        options = self.Options(edit=False, up=False)
        call(['git', 'init'])
        call(['git', 'config', '--add', 'gitli.list.option', 'open'])
        gitli.main(None, ['init', ], None)
        gitli.main(options, ['new', 'Hello World 1'], None)
        gitli.main(options, ['new', 'Hello World 2'], None)
        gitli.main(options, ['new', 'Hello World 3'], None)
        gitli.main(options, ['close', '2'], None)
        gitli.main(options, ['milestone', '0.2'], None)
        lines = read_lines(gitli.ISSUES)
        self.assertEqual('0.1', lines[3].strip())
        self.assertEqual('0.1', lines[7].strip())
        self.assertEqual('0.1', lines[11].strip())
        self.assertEqual('0.2', read_file(gitli.CURRENT))

    def test_up(self):
        options = self.Options(edit=False, up=True)
        call(['git', 'init'])
        call(['git', 'config', '--add', 'gitli.list.option', 'open'])
        gitli.main(None, ['init', ], None)
        gitli.main(options, ['new', 'Hello World 1'], None)
        gitli.main(options, ['new', 'Hello World 2'], None)
        gitli.main(options, ['new', 'Hello World 3'], None)
        gitli.main(options, ['close', '2'], None)
        gitli.main(options, ['milestone', '0.2'], None)
        lines = read_lines(gitli.ISSUES)
        self.assertEqual('0.2', lines[3].strip())
        self.assertEqual('0.1', lines[7].strip())
        self.assertEqual('0.2', lines[11].strip())
        self.assertEqual('0.2', read_file(gitli.CURRENT))
