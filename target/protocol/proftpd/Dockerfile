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

# set corefile dir
RUN mkdir -p /corefile/ && \
    chmod -R 777 /corefile/ &&\
    ulimit -c unlimited

RUN mkdir -p $WORKDIR && \
    mkdir -p /tmp && \
    chmod -R 777 /tmp &&\
    mkdir -p $WORKDIR/aflnet-result

RUN pip3 install -i http://pypi.douban.com/simple --trusted-host pypi.douban.com boofuzz==0.4.1 --default-timeout=1000
RUN git clone https://github.com/calmxkk/boofuzz.git && cd boofuzz && git pull && cd ..

# Set up aflnet
RUN git clone https://github.com/calmxkk/aflnet.git && \
    cd aflnet && \
    make clean all $MAKE_OPT && \
    cd llvm_mode && make $MAKE_OPT

# Download and compile proftpd for fuzzing
RUN cd $WORKDIR && \
    git clone https://github.com/proftpd/proftpd.git

# Set up environment variables for AFLNet
ENV WORKDIR="/root/workspace"
ENV AFLNET="/root/aflnet"
ENV PATH="${PATH}:${AFLNET}:${WORKDIR}"
ENV AFL_PATH="${AFLNET}"
ENV AFL_I_DONT_CARE_ABOUT_MISSING_CRASHES=1 \
    AFL_SKIP_CPUFREQ=1 \
    AFL_NO_AFFINITY=1

ENV ASAN_OPTIONS='log_path=/tmp/asan.log:symbolize=0:disable_coredump=0:handle_segv=1:abort_on_error=1:symbolize=1:detect_leaks=0:detect_stack_use_after_return=1:detect_container_overflow=0:poison_array_cookie=0:malloc_fill_byte=0:max_malloc_fill_size=16777216'
ENV UBSAN_OPTIONS='print_stacktrace=1'

ARG GIT_TAG

COPY --chown=root:root fuzzing.patch ${WORKDIR}/fuzzing.patch

RUN cd $WORKDIR && cd proftpd && \
    git checkout ${GIT_TAG} && \
    CC="afl-clang-fast" CXX="afl-clang-fast++" ./configure && \
    AFL_USE_ASAN=1 make $MAKE_OPT

COPY --chown=root:root basic.conf ${WORKDIR}/
COPY --chown=root:root in-ftp ${WORKDIR}/in-ftp
COPY --chown=root:root ftp.dict ${WORKDIR}/ftp.dict
COPY --chown=root:root run.sh ${WORKDIR}/run
COPY --chown=root:root clean.sh ${WORKDIR}/clean
COPY --chown=root:root cov_script.sh ${WORKDIR}/cov_script

RUN mkdir -p ${WORKDIR}/ftpshare && \
    chown -R root:root ${WORKDIR}/ftpshare



COPY --chown=root:root run-aflnet ${WORKDIR}/run-aflnet
