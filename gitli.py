#!/usr/bin/env python
# coding: utf-8

# For python 2 compatibility
from __future__ import unicode_literals
import sys
from codecs import open
from os.path import split, join, exists
from os import getcwd, mkdir
import subprocess

#from traceback import print_exc


# Python Version Compatibility
major = sys.version_info[0]
minor = sys.version_info[1]

if major < 3:
    rinput = raw_input
else:
    rinput = input

if major == 2 and minor == 6:
    check_output = lambda a: subprocess.Popen(a,
            stdout=subprocess.PIPE).communicate()[0]
else:
    check_output = subprocess.check_output


COLOR = ['git', 'config', '--get', 'gitli.color']
LIST = ['git', 'config', '--get', 'gitli.list.option']

DEFAULT_LIST_FILTER = 'all'

GITLIDIR = '.gitli'

ISSUES = '.issues'
OPEN = '.issues-open'
LAST = '.issues-last'
CURRENT = '.issues-current'
COMMENTS = '.issues-comments'
MSEPARATOR = ','
OSEPARATOR = '\n'

ITYPES = ['Task', 'Bug', 'Enhancement']


class BColors:
    BLUE = '\033[1;34m'
    GREEN = '\033[1;32m'
    YELLOW = '\033[1;33m'
    CYAN = '\033[1;36m'
    WHITE = '\033[1;37m'
    ENDC = '\033[0m'

    def disable(self):
        self.BLUE = ''
        self.GREEN = ''
        self.YELLOW = ''
        self.CYAN = ''
        self.WHITE = ''
        self.ENDC = ''


def is_colored_output():
    '''
    :rtype: True if gitli.color is on in the git config.
    '''
    try:
        value = check_output(COLOR).strip().lower().decode('utf-8')
        return value in ('auto', 'on', 'true')
    except Exception:
        return False


def get_default_list_filter():
    '''
    :rtype: The default list filter specified in the git config or
    DEFAULT_LIST_FILTER.
    '''
    try:
        value = check_output(LIST)
        if not value:
            return DEFAULT_LIST_FILTER
        else:
            return value.strip().lower().decode('utf-8')
    except Exception:
        return DEFAULT_LIST_FILTER


def ask_type(verbose=False, default=1):
    '''Asks the user what type of issue to create.

    :verbose: If False, the default type is returned without asking the user.
    :default: The default issue type.
    :rtype: The issue type selected by the user or the default one if verbose
    is False.
    '''
    if not verbose:
        return 1

    ttype = rinput('Issue type: 1-Task, 2-Bug, 3-Enhancement [{0}]: '\
            .format(default))
    ttype = ttype.strip().lower()

    if not ttype:
        return default
    elif ttype in ('1', 'task'):
        return 1
    elif ttype in ('2', 'bug'):
        return 2
    elif ttype in ('3', 'enhancement'):
        return 3
    else:
        return 1


def ask_milestone(path, verbose=False, default=None):
    '''Asks the user what milestone to associate the issue with.

    :param path: The path to the .gitli directory.
    :param verbose: If False, the default milestone is returned without asking
    the user.
    :param default: The default milestone. If None, the current milestone is
    provided as the default.
    :rtype: The milestone selected by th euser or the default one if verbose
    is False.
    '''
    if default is None:
        with open(join(path, CURRENT), 'r', encoding='utf-8') as current:
            current_value = current.read()
    else:
        current_value = default

    if not verbose:
        return current_value

    milestone = rinput('Milestone: [{0}]: '.format(current_value)).strip()
    if not milestone:
        milestone = current_value

    return milestone


def add_open(path, issue_number):
    '''Add a new issue to the open list.

    :param path: The path to the .gitli directory.
    :param issue_number: The issue to open.
    '''
    with open(join(path, OPEN), 'a', encoding='utf-8') as iopen:
        iopen.write('{0}{1}'.format(issue_number, OSEPARATOR))


def remove_open(path, issue_number):
    '''Remove an issue number from the issues-open file.

    :param path: The path to the .gitli directory.
    :param issue_number: The issue to close.
    '''
    with open(join(path, OPEN), 'r', encoding='utf-8') as iopen:
        issues = iopen.read().split(OSEPARATOR)

    new_issues = OSEPARATOR.join((issue for issue in issues if issue !=
        issue_number))

    with open(join(path, OPEN), 'w', encoding='utf-8') as iopen:
        iopen.write(new_issues)


def get_open_issues(path):
    '''
    :param path: The path to the .gitli directory.
    :rtype: A list of issue numbers that are open.
    '''
    with open(join(path, OPEN), 'r', encoding='utf-8') as iopen:
        issues = iopen.read().split(OSEPARATOR)

    return issues


def filter_issues(issue, filters, open_issues, milestones, itypes):
    '''Indicate whether or not an issue should be displayed (True) or not
    (False).
    :param issue: The issue tuple to filter.
    (issue_number, title, issue_type, milestone)
    :param filters: A list of filters, [str]. e.g., 'close', '0.1', 'task'.
    :param open_issues: A list of the issue numbers that are open. [str]
    :param milestones: A list of milestones, [str], that the issue must be
    associated with. If empty, the issue milestone is not checked.
    :param itypes: A list of issue types, [str], used to filter the issue. If
    the list is empty, the issue type is not checked.
    :rtype: True if the issue passes all filters and can be displayed. False
    otherwise.
    '''
    if 'open' in filters and issue[0] not in open_issues:
        return False

    if 'close' in filters and issue[0] in open_issues:
        return False

    if len(milestones) > 0 and issue[3] not in milestones:
        return False

    if len(itypes) > 0 and ITYPES[issue[2] - 1].lower() not in itypes:
        return False

    return True


def get_issue(path, issue_number):
    '''Return a tuple (issue_number, title, issue_type, milestone).

    :param path: The path to the .gitli directory.
    :param issue_number: The number of the issue to retrieve.
    :rtype: A tuple representing the issue or None if not found.
    '''

    with open(join(path, ISSUES), 'r', encoding='utf-8') as issues_file:
        lines = issues_file.readlines()
    size = len(lines)
    index = 0
    issue = None
    while index < size:
        issue = (
            lines[index].strip(),
            lines[index + 1].strip(),
            int(lines[index + 2].strip()),
            lines[index + 3].strip())
        if issue[0] == issue_number:
            break
        else:
            issue = None
            index += 4

    return issue


def get_issues(path, filters, open_issues, milestones, itypes):
    '''Returns a list of issues that match the filters.
    [(issue_number, title, issue_type, milestone)]

    :param path: The path to the .gitli directory.
    :param filters: A list of filters, [str]. e.g., 'close', '0.1', 'task'.
    :param open_issues: A list of the issue numbers that are open. [str]
    :param milestones: A list of milestones, [str], that the issue must be
    associated with. If empty, the issue milestone is not checked.
    :param itypes: A list of issue types, [str], used to filter the issue. If
    the list is empty, the issue type is not checked.
    :rtype: A list of issue tuples matching the filters.
    '''
    with open(join(path, ISSUES), 'r', encoding='utf-8') as issues_file:
        lines = issues_file.readlines()
    issues = []
    size = len(lines)
    index = 0
    while index < size:
        issue = (
            lines[index].strip(),
            lines[index + 1].strip(),
            int(lines[index + 2].strip()),
            lines[index + 3].strip())
        if filter_issues(issue, filters, open_issues, milestones, itypes):
            issues.append(issue)
        index += 4

    return issues


def print_issues(issues, open_issues, bcolor):
    '''Prints the issues on stdout.
    [(issue_number, title, issue_type, milestone)]

    :param issues: The list of tuples representing the issues to print.
    :param open_issues: The list of the issue numbers that are open.
    :param bcolor: An instance of the BColors class used to colorize the
    output.
    '''
    for (number, title, type_id, milestone) in issues:
        if number in open_issues:
            open_text = 'open'
            color = bcolor.YELLOW
        else:
            open_text = 'closed'
            color = bcolor.GREEN

        milestone_text = '[' + milestone + ']'
        type_text = '[' + ITYPES[type_id - 1] + ']'

        print('{5}#{0:<4}{9} {6}{1:<48}{9} {7}{2:<6} {3:<7}{9} - {8}{4}{9}'
            .format(number, title, type_text, milestone_text, open_text,
            bcolor.CYAN, bcolor.WHITE, bcolor.BLUE, color, bcolor.ENDC))


def init(path):
    '''Initialize the .gitli directory by creating the gitli files.

    :param path: The path to the .gitli directory.
    '''
    if not exists(path):
        mkdir(path)

    new_path = join(path, ISSUES)
    if not exists(new_path):
        open(new_path, 'w', encoding='utf-8').close()

    new_path = join(path, OPEN)
    if not exists(new_path):
        open(new_path, 'w', encoding='utf-8').close()

    new_path = join(path, COMMENTS)
    if not exists(new_path):
        open(new_path, 'w', encoding='utf-8').close()

    new_path = join(path, LAST)
    if not exists(new_path):
        with open(new_path, 'w', encoding='utf-8') as last:
            last.write('0')

    new_path = join(path, CURRENT)
    if not exists(new_path):
        with open(new_path, 'w', encoding='utf-8') as current:
            current.write('0.1')


def new_issue(path, title, verbose=False):
    '''Creates a new issue: add the issue to the issues file, add the issue
    number to the issues-open file, and increment the last issue number in
    issues-last.

    :param path: The path to the .gitli directory.
    :param title: The title of the issue.
    :param verbose: If True, ask the user for the issue type and milestone.
    '''
    with open(join(path, LAST), 'r', encoding='utf-8') as last:
        issue_number = int(last.read().strip()) + 1

    ttype = ask_type(verbose)
    milestone = ask_milestone(path, verbose)

    with open(join(path, ISSUES), 'a', encoding='utf-8') as issues:
        issues.write('{0}\n{1}\n{2}\n{3}\n'.format(issue_number, title,
            ttype, milestone))

    add_open(path, issue_number)

    with open(join(path, LAST), 'w', encoding='utf-8') as last:
        last.write('{0}'.format(issue_number))


def close_issue(path, issue_number):
    '''Closes the issue by removing its number from the issues-open file.

    :param path: The path to the .gitli directory.
    :param issue_number: The number of the issue to close.
    '''
    remove_open(path, issue_number)


def list_issues(path, filters=None, bcolor=BColors()):
    '''Prints a list of issues matching the provided filters.

    :param path: The path to the .gitli directory.
    :param filters: A list of filters such as ['open', '0.1', 'task']
    :param bcolor: An instance of the BColors class to colorize the output.
    '''
    if filters is None or len(filters) == 0:
        filters = [get_default_list_filter()]
    else:
        filters = [ifilter.strip().lower() for ifilter in filters]

    if 'all' in filters:
        filters = []

    open_issues = get_open_issues(path)

    itypes = [ifilter for ifilter in filters if ifilter in
        ('task', 'bug', 'enhancement')]

    milestones = [ifilter for ifilter in filters if ifilter not in
        ('open', 'close', 'task', 'bug', 'enhancement')]

    issues = get_issues(path, filters, open_issues, milestones, itypes)

    print_issues(issues, open_issues, bcolor)

    # Useful for testing
    return issues


def move_issues(path, milestone):
    '''Updates the milestone of all open issues.

    :param path: The path to the .gitli directory.
    :param milestone: The new milestone
    '''
    open_issues = get_open_issues(path)
    issues = get_issues(path, [], [], [], [])

    with open(join(path, ISSUES), 'w', encoding='utf-8') as issues_file:
        for (number, title, itype, imilestone) in issues:
            if number in open_issues:
                imilestone = milestone
            issues_file.write('{0}\n{1}\n{2}\n{3}\n'.format(
                    number,
                    title,
                    itype,
                    imilestone
                    ))


def reopen_issue(path, issue_number):
    '''Reopens an issue by adding its number back to the issues-open file.
    If the issue is already opened, this operation does nothing.

    :param path: The path to the .gitli directory.
    :param issue_number: The number of the issue to reopen.
    '''
    # To make sure that we don't add the issue twice... that would be bad
    remove_open(path, issue_number)
    add_open(path, issue_number)


def show_issue(path, issue_number, bcolor=BColors()):
    '''Prints information about an issue.

    :param path: The path to the .gitli directory.
    :param issue_number: The number of the issue to display.
    :param bcolor: A BColors instance to colorize the output.
    '''
    issue = get_issue(path, issue_number)
    if issue is not None:
        open_issues = get_open_issues(path)
        print_issues([issue], open_issues, bcolor)
    else:
        print('Issue #{0} not found'.format(issue_number))


def edit_issue(path, issue_number):
    '''Enables the user to edit an issue by asking several questions (title,
    issue type, milestone).

    :param path: The path to the .gitli directory.
    :param issue_number: The number of the issue to edit.
    '''
    issues = get_issues(path, [], [], [], [])
    issue = None
    index = -1
    for i, temp_issue in enumerate(issues):
        if temp_issue[0] == issue_number:
            issue = temp_issue
            index = i

    if issue is None:
        print('Issue #{0} unknown'.format(issue_number))
        return
    else:
        title = rinput('Enter a new title (enter nothing to keep the same): ')
        if not title.strip():
            title = issue[1]
        ttype = ask_type(True, issue[2])
        milestone = ask_milestone(path, True, issue[3])
        new_issue = (issue_number, title, ttype, milestone)

        with open(join(path, ISSUES), 'w', encoding='utf-8') as issues_file:
            for i, temp_issue in enumerate(issues):
                if i != index:
                    issues_file.write('{0}\n{1}\n{2}\n{3}\n'.format(
                        temp_issue[0],
                        temp_issue[1],
                        temp_issue[2],
                        temp_issue[3]))
                else:
                    issues_file.write('{0}\n{1}\n{2}\n{3}\n'.format(
                        new_issue[0],
                        new_issue[1],
                        new_issue[2],
                        new_issue[3]))


def remove_an_issue(path, issue_number):
    '''Removes an issue from the issues file.

    :param path: The path to the .gitli directory.
    :param issue_number: The number of the issue to remove.
    '''
    issues = get_issues(path, [], [], [], [])
    with open(join(path, ISSUES), 'w', encoding='utf-8') as issues_file:
        for issue in issues:
            if issue[0] != issue_number:
                issues_file.write('{0}\n{1}\n{2}\n{3}\n'.format(issue[0],
                    issue[1], issue[2], issue[3]))


def edit_milestone(path, milestone, up):
    '''Changes the current milestone by overwriting the issues-current file.

    :param path: The path of the .gitli directory.
    :param milestone: The new current milestone, e.g., '0.1'
    :param up: If True, all open issues will be moved to the new current
    milestone.
    '''
    if milestone:
        current_path = join(path, CURRENT)
        with open(current_path, 'w', encoding='utf-8') as current:
            current.write(milestone)
    if up:
        move_issues(path, milestone)


def show_milestone(path):
    '''Prints the current milestone.

    :param path: The path of the .gitli directory.
    '''
    current_path = join(path, CURRENT)
    with open(current_path, 'r', encoding='utf-8') as current:
        milestone = current.read().strip()

    print('The current milestone is {0}'.format(milestone))


def remove_issue(path, issue_number):
    '''Removes an issue by removing its number for the issues-open file and all
    its information from the issues file.

    :param path: The path of the .gitli directory.
    :param issue_number: The number of the issue to remove.
    '''
    remove_open(path, issue_number)
    remove_an_issue(path, issue_number)


def main(options, args, parser):
    bcolor = BColors()
    if not is_colored_output():
        bcolor.disable()

    if len(args) == 0:
        parser.print_help()
        sys.exit(1)

    command = args[0]
    args = args[1:]
    path = getcwd()
    while not exists(join(path, ".git")):
        path, extra = split(path)
        if not extra:
            print("Unable to find a git repository. ")
            sys.exit(1)

    path = join(path, GITLIDIR)
    if command == 'init':
        init(path)
    elif command in ('new', 'add', 'open'):
        new_issue(path, args[0].strip(), options.edit)
    elif command == 'close':
        close_issue(path, args[0].strip())
    elif command == 'list':
        list_issues(path, args, bcolor)
    elif command == 'reopen':
        reopen_issue(path, args[0].strip())
    elif command == 'show':
        show_issue(path, args[0].strip(), bcolor)
    elif command == 'edit':
        edit_issue(path, args[0].strip())
    elif command in ('remove', 'delete'):
        remove_issue(path, args[0].strip())
    elif command == 'milestone':
        if len(args) == 0:
            show_milestone(path)
        else:
            edit_milestone(path, args[0].strip(), options.up)
