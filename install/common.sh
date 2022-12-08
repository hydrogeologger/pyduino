#!/bin/bash

# Common functions to support installation/configuration of pyduino setup

function version() {
    # Function to convert a string of up to four decimal places to integer
    echo "$@" | awk -F. '{ printf("%d%03d%03d%03d\n", $1,$2,$3,$4); }';
}

function is_installed() {
    if [ "$(dpkg -l "$1" 2> /dev/null | tail -n 1 | cut -d ' ' -f 1)" != "ii" ]; then
        return 1
    else
        return 0
    fi
}

function install_packages() {
    if [ $# -eq 0 ]; then
        return 1
    fi
    # apt -y install --dry-run $@
    # apt -y install $@
    # apt-get -y install --dry-run $@
    # shellcheck disable=SC2068 # Allow element re-splitting
    apt-get -y install $@
    # debconf-apt-progress -- apt-get -y install $@

    # if [ -n "$PACKAGES" ]; then
        # apt-get -y install --dry-run $PACKAGES
        # apt-get -y install $PACKAGES
    # fi
}

function transfer_conf_files_from_path() {
    local FILE_PATH
    if [ $# -ne 1 ]; then
        echo "Incorrect or no file path passed to transfer_conf_files_from_path()"
        return 1
    fi
    # echo $(dirname "$0")
    # echo "$1"
    FILE_PATH=$1
    for file_name in $(find "$FILE_PATH/" -type f); do
        # echo "$file_name"
        # echo "${file_name#*"$FILE_PATH"}"
        cp -v "$file_name" "${file_name#*"$FILE_PATH"}"
    done
}

function get_declared_args_python_version() {
    local PARSED_ARGUMENTS
    PARSED_ARGUMENTS=$(getopt -a -n install_sinovoip_rpi_gpio_pymodule -o '' --long py2,py3 -- "$@")
    local valid_arguments=$?
    if [ $valid_arguments != 0 ]; then
        echo "Incorrect python version: $1 - [ -p2 | --py2 | -py3 | --py3 ]."
        return 2
    fi

    # echo "PARSED_ARGUMENTS is $PARSED_ARGUMENTS"
    eval set -- "$PARSED_ARGUMENTS"

    while test "X$1" != "X--"; do
        case "$1" in
            --py2) F_PYTHON2=true; echo "F_PYTHON2=$F_PYTHON2";;
            --py3) F_PYTHON3=true; echo "F_PYTHON3=$F_PYTHON3";;
            # -- means the end of the arguments; drop this, and break out of the while loop
            --) shift; break;;
            # If invalid options were passed, then getopt should have reported an error,
            # which we checked as VALID_ARGUMENTS when getopt was called...
            *)
                echo "Unexpected option: $1 - this should not happen."
                usage
                ;;
            esac
        shift
    done
    shift #get rid of the '--'
}

do_finish() {
    if [ "$ASK_TO_REBOOT" = true ]; then
        if (whiptail --yesno "Would you like to reboot now?" 20 60 2); then 
            # yes
            sync
            reboot
        fi
    fi
    exit 0
}

# find ./install/ -type f -iname "*.sh" -exec chmod +x {} \;
# find ./install/ -type f -iname "*.sh" -exec chmod +x {} +;
# find ./install/ -type f -exec dos2unix {} \;
# git update-index --chmod=+x $script