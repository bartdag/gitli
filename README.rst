gitli - Git Lightweight Issue Tracking System
=============================================

:Authors:
  Barthelemy Dagenais
:Version: 0.3

gitli is a simple git extension to manage issues in single-developer projects.

The issues are stored in the current branch of the git repository. gitli is
**not** a distributed issue tracker. It's just a script that I wrote after
spending a day looking for that kind of lightweight issue tracker for private
projects.

The script does not attempt to prevent goofs and error messages can make
children cry.

Don't hesitate to create issues in the github bug tracker if you have a feature
request or encounter a bug though.


Requirements
------------

This script has been tested with Python 2.7, 3.1, and 3.2.


Installation
------------

#. Make the git-li script executable (e.g., ``chmod a+x git-li``).
#. Add the git-li script to your path (e.g., ``export PATH=$PATH:/path/to/git-li``)
#. You are done.

Usage
-----

First, create a git repository and then, init git li. Notice the files created
by gitli.

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
    Task type: 1-Task, 2-Bug, 3-Enhancement [1]: 2
    Milestone: [0.1]:
    testgitli $ git li -e new 'My Third Issue'
    Task type: 1-Task, 2-Bug, 3-Enhancement [1]: 1
    Milestone: [0.1]: 0.2
    testgitli $ git li new 'My Fourth Issue'

The list command:

::

    testgitli $ git li list
    #1    My First Issue                                   [Task] [0.1]   - open
    #2    My Second Issue                                  [Bug]  [0.1]   - open
    #3    My Third Issue                                   [Task] [0.2]   - open
    #4    My Fourth Issue                                  [Task] [0.1]   - open

To colorize the output, just enter: ``git config --global add gitli.color auto``

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
    Task type: 1-Task, 2-Bug, 3-Enhancement [3]: 1 
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


License
-------

This software is licensed under the `New BSD License`. See the `LICENSE` file in the top distribution directory for the full license text.
