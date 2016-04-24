#!/bin/bash

# Copyright (c) 2016 Stephen Warren <swarren@wwwdotorg.org>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# * Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# * Neither the name of the copyright holder nor the names of its contributors
#   may be used to endorse or promote products derived from this software
#   without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

stage_dir="$1"
pi_type="$2"

tree_dir="${stage_dir}/tree"
rmlist="${stage_dir}/rmlist"

mkdir -p "${tree_dir}"
touch "${rmlist}"

kernel_src=
kernel7_src=
kernel8_32_src=
kernel8_src=

case "${pi_type}" in
0123)
    kernel_src=build-rpi/u-boot.bin
    kernel7_src=build-rpi_2/u-boot.bin
    kernel8_src=build-rpi_3/u-boot.bin
    ;;
3-32-pl011)
    # FIXME: mkknlimg might not be needed with latest FW defaulting to DT?
    kernel8_32_src=build-rpi_2/u-boot.bin.img
    "${script_dir}/mkknlimg" --dtok build-rpi_2/u-boot.bin build-rpi_2/u-boot.bin.img
    ;;
3-32)
    # FIXME: mkknlimg might not be needed with latest FW defaulting to DT?
    kernel8_32_src=build-rpi_3_32b/u-boot.bin.img
    "${script_dir}/mkknlimg" --dtok build-rpi_3_32b/u-boot.bin build-rpi_3_32b/u-boot.bin.img
    ;;
3-64)
    kernel8_src=build-rpi_3/u-boot.bin
    ;;
*)
    echo Unknown Pi \""${pi_type}"\"
    exit 1
    ;;
esac

echo 'kern*.img' >> "${rmlist}"

if [ -n "${kernel_src}" ]; then
    cp "${kernel_src}" "${tree_dir}/kernel.img"
fi
if [ -n "${kernel7_src}" ]; then
    cp "${kernel7_src}" "${tree_dir}//kernel7.img"
fi
if [ -n "${kernel8_32_src}" ]; then
    cp "${kernel8_32_src}" "${tree_dir}//kernel8-32.img"
fi
if [ -n "${kernel8_src}" ]; then
    cp "${kernel8_src}" "${tree_dir}//kernel8.img"
fi

rm -f "${tree_dir}/config.txt"
touch "${tree_dir}/config.txt"

case "${pi_type}" in
3-32-pl011)
    echo "dtoverlay=pi3-miniuart-bt" >> "${tree_dir}/config.txt"
    ;;
0123|3-*)
    echo "enable_uart=1" >> "${tree_dir}/config.txt"
    ;;
esac
