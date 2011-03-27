from __future__ import unicode_literals
import gitli
import unittest
import tempfile
import shutil
import os
from subprocess import call
from collections import namedtuple


def read_file(file_type, custom_path=gitli.GITLIDIR):
    content = ''
    with open(os.path.join(custom_path, file_type)) as f:
        content = f.read()
    return content


def read_lines(file_type, custom_path=gitli.GITLIDIR):
    content = []
    with open(os.path.join(custom_path, file_type)) as f:
        content = f.readlines()
    return content


def exists(file_type, custom_path=gitli.GITLIDIR):
    return os.path.exists(os.path.join(custom_path, file_type))


class TestGitli(unittest.TestCase):

    def setUp(self):
        self.tempdirpath = tempfile.mkdtemp()
        os.chdir(self.tempdirpath)
        self.gitlipath = os.path.join(self.tempdirpath, gitli.GITLIDIR)
        self.Options = namedtuple('Options', 'edit up path')
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
        self.assertEqual(read_file(gitli.LAST).strip(), '0')

    def test_new(self):
        options = self.Options(edit=False, up=False, path='')
        call(['git', 'init'])
        gitli.main(None, ['init', ], None)
        gitli.main(options, ['new', 'Hello World 1'], None)
        lines = read_lines(gitli.ISSUES)
        self.assertEqual('1', lines[0].strip())
        self.assertEqual('Hello World 1', lines[1].strip())
        self.assertEqual('1', lines[2].strip())
        self.assertEqual('0.1', lines[3].strip())
        self.assertEqual('1', read_file(gitli.LAST).strip())
        lines = read_lines(gitli.OPEN)
        self.assertEqual('1', lines[0].strip())

    def test_remove(self):
        options = self.Options(edit=False, up=False, path='')
        call(['git', 'init'])
        gitli.main(None, ['init', ], None)
        gitli.main(options, ['new', 'Hello World 1'], None)
        gitli.main(options, ['new', 'Hello World 2'], None)
        gitli.main(options, ['new', 'Hello World 3'], None)
        gitli.main(options, ['remove', '2'], None)
        lines = read_lines(gitli.ISSUES)
        self.assertEqual('1', lines[0].strip())
        self.assertEqual('3', lines[4].strip())
        self.assertEqual('3', read_file(gitli.LAST).strip())
        lines = read_lines(gitli.OPEN)
        self.assertEqual('1', lines[0].strip())
        self.assertEqual('3', lines[1].strip())
        gitli.main(options, ['remove', '3'], None)
        gitli.main(options, ['remove', '1'], None)
        self.assertEqual('', read_file(gitli.ISSUES).strip())
        self.assertEqual('3', read_file(gitli.LAST).strip())
        self.assertEqual('', read_file(gitli.OPEN).strip())

    def test_list_issues(self):
        options = self.Options(edit=False, up=False, path='')
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
        options = self.Options(edit=False, up=False, path='')
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
        options = self.Options(edit=False, up=False, path='')
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
        options = self.Options(edit=False, up=True, path='')
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

    def test_path_option(self):
        new_path = os.path.join(self.tempdirpath, 'foobar')
        options = self.Options(edit=False, up=True, path=new_path)
        call(['git', 'init'])
        gitli.main(options, ['init', ], None)
        gitli.main(options, ['new', 'Hello World 1'], None)
        lines = read_lines(gitli.ISSUES, new_path)
        self.assertEqual('1', lines[0].strip())
        self.assertEqual('Hello World 1', lines[1].strip())
        self.assertEqual('1', lines[2].strip())
        self.assertEqual('0.1', lines[3].strip())
        self.assertEqual('1', read_file(gitli.LAST, new_path).strip())
        lines = read_lines(gitli.OPEN, new_path)
        self.assertEqual('1', lines[0].strip())

        # THEN USE GIT CONFIG
        print(gitli.get_path(options.path))
        call(['git', 'config', '--add', 'gitli.path', new_path])
        options = self.Options(edit=False, up=True, path='')
        print(gitli.get_path(options.path))
        gitli.main(options, ['milestone', '0.2'], None)
        self.assertEqual('0.2', read_file(gitli.CURRENT, new_path))

    def test_no_team_mode(self):
        options = self.Options(edit=False, up=False, path='')
        call(['git', 'init'])
        gitli.main(options, ['init', ], None)
        gitli.main(options, ['new', 'Hello World 1'], None)
        self.assertFalse(gitli.is_team_mode())
        self.assertEqual('2', gitli.read_last_issue_number(self.gitlipath))
        self.assertEqual('1', read_file(gitli.LAST).strip())
        print('PREFIX: {0}'.format(gitli.get_team_prefix()))
        self.assertEqual(len(gitli.get_team_prefix()), 1)

    def test_team_mode_on(self):
        options = self.Options(edit=False, up=False, path='')
        call(['git', 'init'])
        gitli.main(options, ['init', ], None)
        call(['git', 'config', 'gitli.team.active', 'on'])
        call(['git', 'config', 'gitli.team.user', 'bob'])
        self.assertTrue(gitli.is_team_mode())
        self.assertEqual('bob1', gitli.read_last_issue_number(self.gitlipath))
        self.assertEqual('0\n', read_file(gitli.LAST))
        gitli.main(options, ['new', 'Hello World 1'], None)
        self.assertTrue(gitli.is_team_mode())
        self.assertEqual('bob2', gitli.read_last_issue_number(self.gitlipath))
        self.assertEqual('0\nbob1\n', read_file(gitli.LAST))

    def test_mixed_team_mode(self):
        options = self.Options(edit=False, up=False, path='')
        call(['git', 'init'])
        gitli.main(options, ['init', ], None)
        gitli.main(options, ['new', 'Hello World 1'], None)
        self.assertFalse(gitli.is_team_mode())
        self.assertEqual('2', gitli.read_last_issue_number(self.gitlipath))
        self.assertEqual('1', read_file(gitli.LAST).strip())
        call(['git', 'config', 'gitli.team.active', 'on'])
        call(['git', 'config', 'gitli.team.user', 'bob'])
        gitli.main(options, ['new', 'Hello World 2'], None)
        gitli.main(options, ['new', 'Hello World 3'], None)
        self.assertEqual('bob3', gitli.read_last_issue_number(self.gitlipath))
        self.assertEqual('1\nbob2\n', read_file(gitli.LAST))


if __name__ == '__main__':
    unittest.main()
