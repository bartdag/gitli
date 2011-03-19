gitli - Git Lightweight Issue Tracking System
=============================================

:Authors:
  Barthelemy Dagenais
:Version: 0.4

gitli is a simple git extension to manage issues in single-developer projects.

The issues are stored in the current branch of the git repository. gitli is
**not** a distributed issue tracker. It's just a script that I wrote after
spending a day looking for that kind of lightweight issue tracker for private
projects.

The script does not attempt to prevent goofs, and error messages can make
children cry.

Don't hesitate to create issues in the github bug tracker if you have a feature
request or encounter a bug though.


Requirements
------------

gitli has been tested with Python 2.6, 2.7, 3.1, and 3.2.


Installation
------------

Use pip or easy_install: ``easy_install gitli``

Alternatively:

#. Make the git-li script executable (e.g., ``chmod a+x git-li``).
#. Add the git-li script to your path (e.g., ``export PATH=$PATH:/path/to/git-li``)
#. You are done.

Usage
-----

First, create a git repository and then, initialize git li. Notice the files
created by gitli.

::

    projects $ mkdir testgitli
    projects $ cd testgitli 
    testgitli $ git init
    Initialized empty Git repository in projects/testgitli/.git/
    testgitli $ git li init
    testgitli $ git addremove
    testgitli $ git commit -m 'initial import'
    [master (root-commit) 8ef5046] initial import
      2 files changed, 2 insertions(+), 0 deletions(-)
      create mode 100644 .gitli/.issues
      create mode 100644 .gitli/.issues-comments
      create mode 100644 .gitli/.issues-current
      create mode 100644 .gitli/.issues-last
      create mode 100644 .gitli/.issues-open

Then, create a few issues. Notice the use of `-e` to override the default
values:

::

    testgitli $ git li new 'My First Issue'
    testgitli $ git li -e new 'My Second Issue'
    Issue type: 1-Task, 2-Bug, 3-Enhancement [1]: 2
    Milestone: [0.1]:
    testgitli $ git li -e new 'My Third Issue'
    Issue type: 1-Task, 2-Bug, 3-Enhancement [1]: 1
    Milestone: [0.1]: 0.2
    testgitli $ git li new 'My Fourth Issue'

The list command:

::

    testgitli $ git li list
    #1    My First Issue                                   [Task] [0.1]   - open
    #2    My Second Issue                                  [Bug]  [0.1]   - open
    #3    My Third Issue                                   [Task] [0.2]   - open
    #4    My Fourth Issue                                  [Task] [0.1]   - open


The close command:

::

    testgitli $ git li close 4
    testgitli $ git li list 
    #1    My First Issue                                   [Task] [0.1]   - open
    #2    My Second Issue                                  [Bug]  [0.1]   - open
    #3    My Third Issue                                   [Task] [0.2]   - open
    #4    My Fourth Issue                                  [Task] [0.1]   - closed

The list command with filters:

::

    testgitli $ git li list open
    #1    My First Issue                                   [Task] [0.1]   - open
    #2    My Second Issue                                  [Bug]  [0.1]   - open
    #3    My Third Issue                                   [Task] [0.2]   - open
    testgitli $ git li list close 
    #4    My Fourth Issue                                  [Task] [0.1]   - closed
    testgitli $ git li open bug 
    testgitli $ git li list open bug
    #2    My Second Issue                                  [Bug]  [0.1]   - open
    testgitli $ git li list open bug 0.1
    #2    My Second Issue                                  [Bug]  [0.1]   - open

The reopen command:

::

    testgitli $ git li reopen 4 
    testgitli $ git li list 
    #1    My First Issue                                   [Task] [0.1]   - open
    #2    My Second Issue                                  [Bug]  [0.1]   - open
    #3    My Third Issue                                   [Task] [0.2]   - open
    #4    My Fourth Issue                                  [Task] [0.1]   - open

Edit an issue (notice the use of default values):

::

    testgitli $ git li edit 3 
    Enter a new title (enter nothing to keep the same):
    Issue type: 1-Task, 2-Bug, 3-Enhancement [3]: 1 
    Milestone: [0.2]: 0.1
    testgitli $ git li list 
    #1    My First Issue                                   [Task] [0.1]   - open
    #2    My Second Issue                                  [Bug]  [0.1]   - open
    #3    My Third Issue                                   [Task] [0.1]   - open
    #4    My Fourth Issue                                  [Task] [0.1]   - open

Update the default milestone:

::

    testgitli $ git li milestone 0.2
    testgitli $ git li new 'My Fifth Issue' 
    testgitli $ git li list 
    #1    My First Issue                                   [Task] [0.1]   - open
    #2    My Second Issue                                  [Bug]  [0.1]   - open
    #3    My Third Issue                                   [Task] [0.1]   - open
    #4    My Fourth Issue                                  [Task] [0.1]   - open
    #5    My Fifth Issue                                   [Task] [0.2]   - open

The show command:

::

    testgitli $ git li show 5 
    #5    My Fifth Issue                                   [Task] [0.2]   - open

The remove command:

::

    testgitli $ git li remove 5
    testgitli $ git li list
    #1    My First Issue                                   [Task] [0.1]   - open
    #2    My Second Issue                                  [Bug]  [0.1]   - open
    #3    My Third Issue                                   [Task] [0.1]   - open
    #4    My Fourth Issue                                  [Task] [0.1]   - open

Update the default milestone and move all open issues to the new milestone:

::

    testgitli $ git li milestone --up 0.3
    testgitli $ git li list
    #1    My First Issue                                   [Task] [0.3]   - open
    #2    My Second Issue                                  [Bug]  [0.3]   - open
    #3    My Third Issue                                   [Task] [0.3]   - open
    #4    My Fourth Issue                                  [Task] [0.3]   - open


Show the usage help:

::

    testgitli $ git-li --help
    Usage: git-li <command> [command-options]

    Commands:
    init                      Initialize the git repositoryto use git-li
    list <PATTERN...>         List issues for this repository
    new  [--edit] <TITLE>     Create a new issue for this repository
    show <NUMBER>             Show the given issue
    edit <NUMBER>             Edit the given issue
    reopen <NUMBER>           Reopen the given issue
    remove <NUMBER>           Remove the given issue (removes all info)
    milestone                 Show the current milestone
    milestone [--up] <MILE>   Set the current milestone
    close <NUMBER>            Close the given issue

    A few examples:
    git li init

    git li new 'My First Issue'

    git li close 1

    git li list open task 0.1

    Aliases:
    git li new|add|open
    git li remove|delete

    Options:
    -h, --help  show this help message and exit
    -e, --edit  change issue type and milestone when adding a new issue.
    -u, --up    Move all the open issues to the next milestone specified by the                                                                                                     
                milestone command.


Git Configuration Variables
---------------------------

``git config --add gitli.color auto``
  Colorizes the shell output.

``git config --add gitli.list.option <option>`` 
  Specifies a default list option. For example, if you choose ``open``, the
  next time you call the ``list`` command without any option, gitli will only
  display the open issues.


License
-------

This software is licensed under the `New BSD License`. See the `LICENSE` file
in the for the full license text.
