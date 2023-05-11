FROM ubuntu:20.04

# Install common dependencies
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get -y update && \
    apt-get -y install sudo \ 
    apt-utils \
    build-essential \
    openssl \
    clang \
    graphviz-dev \
    git \
    autoconf \
    libgnutls28-dev \
    libssl-dev \
    llvm \
    python3-pip \
    nano \
    net-tools \
    vim \
    gdb \
    netcat \
    strace \
    wget \
    libtool \
    m4 \ 
    pkg-config \
    libjson-c-dev \
    libreadline-dev \
    libyang-dev \
    libcap-dev \
    flex \
    bison \
    systemctl \
    zip libelf-dev cmake libpcre2-dev libelf-dev

RUN pip3 install -i http://pypi.douban.com/simple --trusted-host pypi.douban.com gcovr==4.2 --default-timeout=1000
RUN pip3 install -i http://pypi.douban.com/simple --trusted-host pypi.douban.com pytest --default-timeout=1000

RUN mkdir -p /tmp && chmod -R 777 /tmp

USER root
WORKDIR /root/

ENV WORKDIR="/root/"
ENV PATH="${PATH}:${WORKDIR}"

RUN sudo groupadd -g 92 frr && \
    sudo groupadd -r -g 85 frrvty && \
    sudo useradd -u 92 -g 92 -M -r -G frrvty -s /sbin/nologin \
    -c "FRR FRRouting suite" -d /var/run/frr frr

RUN cd $WORKDIR && \
    git clone https://github.com/FRRouting/frr.git frr

# RUN cd $WORKDIR && \
#     wget https://github.com/FRRouting/frr/archive/refs/tags/frr-7.3.zip --no-check-certificate && \
#     unzip frr-7.3.zip && \
#     mv frr-frr-7.3/ frr

# install libyang-2.0.0
RUN cd $WORKDIR && \
    git clone https://github.com/CESNET/libyang.git

# Set up environment variables for ASAN
ENV ASAN_OPTIONS='log_path=/tmp/asan.log:disable_coredump=0:handle_segv=1:abort_on_error=1:symbolize=1:detect_leaks=1:detect_stack_use_after_return=1:detect_container_overflow=0:poison_array_cookie=0:malloc_fill_byte=0:max_malloc_fill_size=16777216'
ENV UBSAN_OPTIONS='print_stacktrace=1'

# disable this if build frr7
RUN cd $WORKDIR/libyang && \
    git checkout v2.0.0 && \
    mkdir build && cd build && \
    cmake -D CMAKE_INSTALL_PREFIX:PATH=/usr -D CMAKE_BUILD_TYPE:String="Release" .. && \
    make && sudo make install

ARG GIT_TAG

RUN cd $WORKDIR/frr && \
    git checkout ${GIT_TAG} && \
    ./bootstrap.sh && \
    ./configure --bindir=/usr/bin --sbindir=/usr/lib/frr \
    --sysconfdir=/etc/frr \
    --libdir=/usr/lib/frr \
    --libexecdir=/usr/lib/frr \
    --localstatedir=/var/run/frr \
    --with-moduledir=/usr/lib/frr/modules \
    --enable-multipath=64 \
    --enable-user=frr \
    --enable-group=frr \
    --enable-vty-group=frrvty \
    --disable-ldpd \
    --enable-fpm \
    --enable-fuzzing \
    --enable-netlink-fuzzing \
    --enable-address-sanitizer \
    --with-pkg-git-version \
    SPHINXBUILD=/usr/bin/sphinx-build \
    CC=clang &&\
    make && make install

RUN mkdir /var/log/frr && \
    mkdir -p /etc/frr && \
    touch /etc/frr/zebra.conf \
    /etc/frr/bgpd.conf \
    /etc/frr/ospfd.conf  \
    /etc/frr/ospf6d.conf  \
    /etc/frr/isisd.conf  \
    /etc/frr/ripd.conf  \
    /etc/frr/ripngd.conf  \
    /etc/frr/pimd.conf  \
    /etc/frr/nhrpd.conf  \
    /etc/frr/eigrpd.conf \
    /etc/frr/babeld.conf

RUN chown -R frr:frr /etc/frr/ && \
    touch /etc/frr/vtysh.conf && \
    chown frr:frrvty /etc/frr/vtysh.conf && \
    chmod 640 /etc/frr/*.conf && \
    mkdir /corefile/ && \
    chmod -R 777 /corefile

COPY --chown=frr:frr bgpd.conf /etc/frr/bgpd.conf
COPY --chown=frr:frr daemons /etc/frr/daemons
COPY --chown=root:root 90-routing-sysctl.conf /etc/sysctl.d/90-routing-sysctl.conf
COPY --chown=root:root run-frr /root/run-frr

RUN sudo install -p -m 644 /root/frr/tools/frr.service /usr/lib/systemd/system/frr.service



