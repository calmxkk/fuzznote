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
    libcap-dev

RUN pip3 install -i http://pypi.douban.com/simple --trusted-host pypi.douban.com gcovr==4.2 --default-timeout=1000 

RUN echo 'root:root' | chpasswd
USER root
WORKDIR /root/

ENV WORKDIR="/root/workspace"
ENV PATH="${PATH}:${WORKDIR}"

# install boofuzz
RUN pip3 install -i http://pypi.douban.com/simple --trusted-host pypi.douban.com boofuzz==0.4.1 --default-timeout=1000
RUN git clone https://github.com/jtpereyda/boofuzz.git

# Set up aflnet
RUN git clone https://github.com/calmxkk/aflnet.git && \
    cd aflnet && \
    make clean all $MAKE_OPT && \
    cd llvm_mode && make $MAKE_OPT

# set corefile dir
RUN mkdir -p /corefile/ && \
    chmod -R 777 /corefile/ &&\
    ulimit -c unlimited

RUN mkdir -p $WORKDIR && \
    mkdir -p /tmp && \
    chmod -R 777 /tmp &&\
    mkdir -p $WORKDIR/aflnet-result

# Download and compile OpenSSL for fuzzing
RUN cd ${WORKDIR} && \
    git clone https://github.com/openssl/openssl.git openssl

# Download and compile OpenSSH for fuzzing
RUN cd ${WORKDIR} && \
    git clone https://github.com/openssh/openssh-portable.git openssh

# Set up environment variables for AFLNet
ENV WORKDIR="/root/workspace"
ENV AFLNET="/root/aflnet"
ENV PATH="${PATH}:${AFLNET}:${WORKDIR}"
ENV AFL_PATH="${AFLNET}"
ENV AFL_I_DONT_CARE_ABOUT_MISSING_CRASHES=1 \
    AFL_SKIP_CPUFREQ=1 \
    AFL_NO_AFFINITY=1

# Set up environment variables for ASAN
ENV ASAN_OPTIONS='log_path=/tmp/asan.log:symbolize=1:disable_coredump=0:handle_segv=1:abort_on_error=1:symbolize=1:detect_leaks=0:detect_stack_use_after_return=1:detect_container_overflow=0:poison_array_cookie=0:malloc_fill_byte=0:max_malloc_fill_size=16777216'
ENV UBSAN_OPTIONS='print_stacktrace=1'

COPY --chown=root:root rand.inc ${WORKDIR}/rand.inc
COPY --chown=root:root rand.patch ${WORKDIR}/rand.patch

# Download and compile OpenSSL 1.0.2
# (for compatibility with older OpenSSH used in this benchmark)
RUN cd ${WORKDIR} && \
    cd openssl && \
    git checkout 12ad22d && \
    ./Configure linux-x86_64-clang shared --prefix=$WORKDIR/openssl-install && \
    make $MAKE_OPT && \
    make install

ENV LD_LIBRARY_PATH="${WORKDIR}/openssl-install/lib"

ARG GIT_TAG

RUN cd ${WORKDIR} && cd openssh && \
    git checkout V_9_3_P1 && \
    cp ${WORKDIR}/rand.inc . && \
    patch -p1 < ${WORKDIR}/rand.patch && \
    autoreconf && \
    ./configure \
    CC="afl-clang-fast" \
    CFLAGS="-g -O3 -I$WORKDIR/openssl-install/include" \
    --prefix=$PWD/install \
    --with-openssl=$WORKDIR/openssl-install \
    --with-ldflags="-L$WORKDIR/openssl-install/lib" \
    --with-privsep-path=$PWD/var-empty \
    --with-sandbox=no \
    --with-privsep-user=ubuntu && \
    AFL_USE_ASAN=1 make $MAKE_OPT && \
    make install

COPY --chown=root:root in-ssh ${WORKDIR}/in-ssh
COPY --chown=root:root ssh.dict ${WORKDIR}/ssh.dict
COPY --chown=root:root run-aflnet ${WORKDIR}/run-aflnet

