Ensure that package manager repositories are installed.  This role works
with the pattern of including variables for different operating systems.

.. note:: This role currently only supports RPM and DEB based distributions.

Example use for Debian and Ubuntu:

.. code-block:: yaml

   - name: Add all repositories
     include_role:
       name: ensure-package-repositories
     vars:
       repositories_keys:
         - url: https://deb.nodesource.com/gpgkey/nodesource.gpg.key
       repositories_list:
         - repo: deb-src https://deb.nodesource.com/node_6.x {{ ansible_distribution_release }} main
         - repo: deb https://deb.nodesource.com/node_6.x {{ ansible_distribution_release }} main

Example use for Fedora and Red Hat:

.. code-block:: yaml

   _docker_keys:
     - data: |
         -----BEGIN PGP PUBLIC KEY BLOCK-----
         ...
         -----END PGP PUBLIC KEY BLOCK-----

   _docker_repos:
     - name: docker-ce-stable
       description: Docker CE Stable - $basearch
       baseurl: "{{ docker_mirror_base_url }}/$releasever/$basearch/stable"
       gpgcheck: yes

   - name: Add all repositories
         include_role:
           name: ensure-package-repositories
         vars:
           repositories_keys: "{{ _docker_keys }}"
           repositories_list: "{{ _docker_repos }}"

Example use for openSUSE and SUSE Linux:

.. code-block:: yaml

   _docker_keys:
     - data: |
         -----BEGIN PGP PUBLIC KEY BLOCK-----
         ...
         -----END PGP PUBLIC KEY BLOCK-----

   _docker_repos:
     - name: docker-ce-stable
       description: Docker CE Stable - $basearch
       uri: "{{ docker_mirror_base_url }}/$releasever/$basearch/stable.repo"

   - name: Add all repositories
         include_role:
           name: ensure-package-repositories
         vars:
           repositories_keys: "{{ _docker_keys }}"
           repositories_list: "{{ _docker_repos }}"

**Role Variables**

.. zuul:rolevar:: repositories_keys
   :default: []

   List of dictionaries containing keys to install for the package manager,
   every dictionary may contain either the key ``url`` which will be
   downloaded and installed, or ``data`` which contains the key to be
   installed.

.. zuul:rolevar:: repository_list
   :default: []

   List of dictionaries containing repository configuration, the format
   of each dictionary is mapped to the same as the module parameters of
   the package manager for Ansible (such as ``yum_repository``, etc.)
