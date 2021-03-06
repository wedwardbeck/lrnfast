FROM clearlinux:latest AS builder

ARG swupd_args
# Move to latest Clear Linux release to ensure
# that the swupd command line arguments are
# correct
RUN swupd update --no-boot-update $swupd_args

# Grab os-release info from the minimal base image so
# that the new content matches the exact OS version
COPY --from=clearlinux/os-core:latest /usr/lib/os-release /

# Install additional content in a target directory
# using the os version from the minimal base
RUN source /os-release && \
    mkdir /install_root \
    && swupd os-install -V ${VERSION_ID} \
    --path /install_root --statedir /swupd-state \
    --bundles=os-core-update,python3-basic,ncat --no-scripts
    # --bundles=os-core-update,python3-basic --no-boot-update

# For some Host OS configuration with redirect_dir on,
# extra data are saved on the upper layer when the same
# file exists on different layers. To minimize docker
# image size, remove the overlapped files before copy.
RUN mkdir /os_core_install
COPY --from=clearlinux/os-core:latest / /os_core_install/
RUN cd / && \
    find os_core_install | sed -e 's/os_core_install/install_root/' | xargs rm -d &> /dev/null || true


FROM clearlinux/os-core:latest

COPY --from=builder /install_root /

#set work directory early so remaining paths can be relative
WORKDIR /usr/src/app

# Adding requirements file to current directory
# just this file first to cache the pip install step when code changes
COPY requirements.txt .

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PIP_NO_CACHE_DIR=1

#install dependencies
RUN pip install cython && pip install -r requirements.txt

#temp fix for databases - not correct release on PyPi
COPY ./databases ./databases
RUN pip install ./databases  && cd ../ && rm -rf /databases

# expose the port 8000
EXPOSE 8000

# add app
COPY . .