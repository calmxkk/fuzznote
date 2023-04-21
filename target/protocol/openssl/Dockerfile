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

RUN pip3 install -i http://pypi.douban.com/simple --trusted-host pypi.douban.com boofuzz==0.4.1 --default-timeout=1000
RUN git clone https://github.com/jtpereyda/boofuzz.git

# Set up aflnet
RUN git clone https://github.com/calmxkk/aflnet.git && \
    cd aflnet && \
    make clean all $MAKE_OPT && \
    cd llvm_mode && make $MAKE_OPT

ENV WORKDIR="/root/workspace"
ENV PATH="${PATH}:${WORKDIR}"

# set corefile dir
RUN mkdir -p /corefile/ && \
    chmod -R 777 /corefile/ &&\
    ulimit -c unlimited

RUN mkdir -p $WORKDIR && \
    mkdir -p /tmp && \
    chmod -R 777 /tmp &&\
    mkdir -p $WORKDIR/aflnet-result

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

# Download and compile OpenSSL for fuzzing
RUN cd ${WORKDIR} && \
    git clone https://github.com/openssl/openssl.git

ARG GIT_TAG

COPY --chown=root:root key.pem ${WORKDIR}/key.pem
COPY --chown=root:root cert.pem ${WORKDIR}/cert.pem
COPY --chown=root:root rand.patch ${WORKDIR}/rand.patch

RUN cd ${WORKDIR}/openssl && \
    cp ${WORKDIR}/*.pem ./ && \
    git checkout ${GIT_TAG} && \
    CC=afl-clang-fast ./config no-shared && \
    AFL_USE_ASAN=1 CC=afl-clang-fast make $MAKE_OPT

COPY --chown=root:root in-tls ${WORKDIR}/in-tls
COPY --chown=root:root tls.dict ${WORKDIR}/tls.dict
COPY --chown=root:root run.sh ${WORKDIR}/run

