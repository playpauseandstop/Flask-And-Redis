"""
=======
testapp
=======

Test Comments app which shows how to use Flask-And-Redis extension.

Database Architercture
======================

To show full abilities of Flask-And-Redis extension data for Comments app split
into two Redis storages: links and content.

Links storage contains lists with all available threads and proper thread
comments sequences, when content storage contains all other content,
obviously, as threads metadata and comments for each thread if available.

Threads
-------

As said above Links storage contains Redis list where all available threads
stored. This list stored in Redis as::

    <prefix>:threads

where ``<prefix>`` is configurable value, which equals ``"far_testapp"`` by
default.

Thread
------

Thread metadata contains in Redis hashes which stored in Content storage.
Each Thread hash stored in Redis as::

    <prefix>:thread:<thread>

where ``<thread>`` is Thread UID and has next items::

    author -> Thread author
    subject -> Thread subject
    timestamp -> Timestamp when thread created
    last_comment_uid -> UID of latest comment if any

Comment
-------

Comment data also contains in Redis hashes which stored in Content storage.
Each Comment hash stored in Redis as::

    <prefix>:thread:<thread>:<comment>

where ``<comment>`` is Comment UID ans has next items::

    author -> Comment author
    text -> Comment text
    timestamp -> Timestamp when comment added

Thread Comments
---------------

To setup proper chronologically sequence of added comments for all thread
comments their UIDs stored by time of addition in Redis list in Links storage
as::

    <prefix>:thread:<thread>:comments

Thread Comments Counter
-----------------------



::

    <prefix>:thread:<thread>:counter

"""
