Update JSON file

This role reads a JSON file, merges it with supplied values using
Ansible's ``combine`` filter and writes it back out.  It is useful for
updating configuration files.  Note this role is not currently
idempotent and will write the file each time.

**Role Variables**

.. zuul:rolevar:: update_json_file_name
   :type: path

   The path to the file to edit.

.. zuul:rolevar:: update_json_file_combine
   :type: object

   The data to be combined with the existing file data.  This uses the
   Jinja ``combine`` filter.

.. zuul:rolevar:: update_json_file_debug
   :default: false
   :type: bool

   If enabled, output the combined result in a debug task.

.. zuul:rolevar:: update_json_file_default
   :default: {}

   The default value if the given file does not exist.

.. zuul:rolevar:: update_json_file_become
   :type: bool
   :default: false

   The ``become:`` status when writing out the new file.

.. zuul:rolevar:: update_json_file_mode

   The mode for the combined file.

.. zuul:rolevar:: update_json_file_user

   The user for the combined file.

.. zuul:rolevar:: update_json_file_group

   The group for the combined file.

.. zuul:rolevar:: update_json_dir_mode

   The mode for the directory if that does not already exists.
