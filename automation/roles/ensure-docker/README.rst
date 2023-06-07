An ansible role to install docker and configure it to use mirrors if available.

**Role Variables**

.. zuul:rolevar:: mirror_fqdn
   :default: {{ zuul_site_mirror_fqdn }}

   The base host for mirror servers.

.. zuul:rolevar:: docker_mirror

   URL to override the generated docker hub mirror url based on
   :zuul:rolevar:`ensure-docker.mirror_fqdn`.

.. zuul:rolevar:: use_upstream_docker
   :default: True

   By default this role adds repositories to install docker from upstream
   docker. Set this to False to use the docker that comes with the distro.

.. zuul:rolevar:: docker_use_buildset_registry
   :default: False

   This role does not enable the usage of the buildset registry by default,
   this variable allows enabling the usage of the buildset registry after
   installing Docker.

.. zuul:rolevar:: docker_compose_install
   :default: False

   This role does not install docker-compose by default but you can use
   this setting to install docker-compose as well.

.. zuul:rolevar:: docker_update_channel
   :default: stable

   Which update channel to use for upstream docker. The two choices are
   ``stable``, which is the default and updates quarterly, and ``edge``
   which updates monthly.

.. zuul:rolevar:: docker_insecure_registries
   :default: undefined

   Declare this with a list of insecure registries to define the
   registries which are allowed to communicate with HTTP only or
   HTTPS with no valid certificate.

.. zuul:rolevar:: docker_gpg_key
   :default: string

   The raw content of the upstream docker gpg key, as found here
   https://download.docker.com/linux/fedora/gpg

.. zuul:rolevar:: docker_distro_packages
   :default: list

   List of packages to be installed when `use_upstream_docker` is set to
   **false**. The package set is defined by default using distro specific
   variables. If the package set needs to be changed this option can be
   overridden as needed.

.. zuul:rolevar:: docker_upstream_distro_required_packages
   :default: list

   List of packages to be installed when `use_upstream_docker` is set to
   **true**. The package set is defined by default using distro specific
   variables and contains a list of supporting packages required to be
   installed prior to installing docker-ce. If the package set needs to
   be changed this option can be overridden as needed.

.. zuul:rolevar:: docker_upstream_distro_remove_packages
   :default: list

   List of packages to be removed before installing new ones. It is used
   for avoiding potential conflicts. For example it can remove `docker`
   package before trying to install `docker-ce`. The default value is
   distro specific.

.. zuul:rolevar:: docker_upstream_distro_packages
   :default: list

   List of packages to be installed when `use_upstream_docker` is set to
   **true**. The package set is defined by default using distro specific
   variables. If the package set needs to be changed this option can be
   overridden as needed.

.. zuul:rolevar:: docker_download_fqdn
   :default: download.docker.com

   Add default option to set the docker download fqdn.

.. zuul:rolevar:: docker_mirror_base_url
   :default: https://{{ docker_download_fqdn }}/linux/{ubuntu,centos,fedora}

   By default this option sets the repository base url. This variable is
   based on :zuul:rolevar:`ensure-docker.docker_download_fqdn`. When this
   option is unset, the role will use distro specific variables which are
   loaded at the time of execution.

.. zuul:rolevar:: docker_userland_proxy
   :type: bool

   Set to false to disable the docker userland proxy. This variable is useful
   when docker is causing routing problem, such as when a kubernetes deployment
   is unable to reach its own service.
