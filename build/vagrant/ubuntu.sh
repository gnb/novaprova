# Setup C development environment and prereqs
<% if @ppa %>
add-apt-repository -y ppa:<%= @ppa %>
<% end %>
apt-get update
apt-get install -y \
    <% if @gcc_version %>gcc-<%= @gcc_version %><% end %> \
    <% if @gcc_version %>g++-<%= @gcc_version %><% end %> \
    git autoconf automake libxml2-dev libxml2-utils \
    pkg-config valgrind binutils-dev doxygen \
    zlib1g-dev libiberty-dev sphinx-common
apt-get install -y python3-sphinx python3-breathe || apt-get install -y python-sphinx python-breathe
<% if @gcc_version %>
update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-<%= @gcc_version %> \
    60 --slave /usr/bin/g++ g++ /usr/bin/g++-<%= @gcc_version %>
<% end %>
