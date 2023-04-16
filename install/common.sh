#!/bin/bash

# Common functions to support installation/configuration of pyduino setup

BASE_DIR=$(pwd)

function return_to_base_dir() {
    # Function to working directory when script was called
    cd "$BASE_DIR" || { echo "Unable to enter $BASE_DIR"; return 1; }
}

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

function get_pypi_version() {
    curl -sG -H 'Host: pypi.org' -H 'Accept: application/json' https://pypi.org/pypi/"$1"/json | awk -F "version\":\"" '{ print $2 }' | cut -d '"' -f 1
}

function get_remote_package_version() {
    apt-cache show "$1" | grep Version | cut -d ' ' -f 2
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

function show_no_python_version_declared_message() {
    echo "No python version declared!"
    echo "Acceptable Python Version Options:
    Python 2: -py2 | --py2
    Python 3: -py3 | --py3"
}

function get_declared_args_python_version() {
    local PARSED_ARGUMENTS
    PARSED_ARGUMENTS=$(getopt --name get_declared_args_python_version \
            --alternative --options '' --longoptions py2,py3 -- "$@")
    local valid_arguments=$?
    if [ $valid_arguments != 0 ]; then
        echo "Incorrect python version: $1 - [ -p2 | --py2 | -py3 | --py3 ]."
        return 2
    fi

    # echo "PARSED_ARGUMENTS is $PARSED_ARGUMENTS"
    # Reorder parameters
    eval set -- "$PARSED_ARGUMENTS"

    # Return error when no option was given
    if test "X$1" == "X--"; then
        return 1
    fi

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
                ;;
            esac
        shift
    done
    shift #get rid of the '--'
}

function apply_avrdudeconf_missing_fix() {
    echo "Apply avrdude.conf missing fix - Add symbolic link"
    # Weird avrdude.conf fix, where avrdude.conf is not detected in the right directory
    mkdir /usr/share/arduino/hardware/tools/avr/etc
    ln -s ../../avrdude.conf /usr/share/arduino/hardware/tools/avr/etc/avrdude.conf
}

function install_avrdude_rpi_autoreset() {
    # install dependency
    install_packages "strace"

    local CLONE_DIR
    CLONE_DIR="/home/${SUDO_USER:-$USER}/avrdude-rpi"

    echo "Downloading and installing avrdude-rpi from hydrogeologger repo"
    git clone "https://github.com/hydrogeologger/avrdude-rpi.git" "$CLONE_DIR"

    # Change owner of directory to current user
    chown -R "${SUDO_USER:-$USER}":"${SUDO_USER:-$USER}" "$CLONE_DIR"

    # Go to
    cd "$CLONE_DIR" || { echo "Unable to enter $CLONE_DIR"; return 1; }


    cp autoreset /usr/bin
    cp avrdude-autoreset /usr/bin

    # If avrdude is not a symlink, then back it up
    if [ -f "/usr/bin/avrdude" ] && ! [ -L "/usr/bin/avrdude" ]; then
        mv /usr/bin/avrdude /usr/bin/avrdude-original
    fi

    # symlink avrdude to avrdude-autoreset
    ln -s /usr/bin/avrdude-autoreset /usr/bin/avrdude

    return_to_base_dir
}


function do_finish() {
    # if [ "$ASK_TO_REBOOT" = true ]; then
    #     if (whiptail --yesno "Would you like to reboot now?" 20 60 2); then
    #         # yes
    #         sync
    #         reboot
    #     fi
    # fi
    # exit 0
    echo "System will reboot in approximately 15 Seconds."
    echo "Would you like to defer system reboot? You will need to manually reboot later. Y/N"
    while true; do
        if read -r -t 15 -n 1 yesno; then
            # user input something
            if [ "$yesno" = "y" ]; then
                return 0
            fi
        else
            # no user input
            break
        fi
    done
    echo "Rebooting now!"
    sync
    reboot
}

function create_empty_crontab_template() {
{ echo "# Edit this file to introduce tasks to be run by cron.
#
# Each task to run has to be defined through a single line
# indicating with different fields when the task will be run
# and what command to run for the task
#
# To define the time you can provide concrete values for
# minute (m), hour (h), day of month (dom), month (mon),
# and day of week (dow) or use '*' in these fields (for 'any').
#
# Notice that tasks will be started based on the cron's system
# daemon's notion of time and timezones.
#
# Output of the crontab jobs (including errors) is sent through
# email to the user the crontab file belongs to (unless redirected).
#
# For example, you can run a backup of all your user accounts
# at 5 a.m every week with:
# 0 5 * * 1 tar -zcf /var/backups/home.tgz /home/
#
# For more information see the manual pages of crontab(5) and cron(8)
#
# m h  dom mon dow   command"; } | crontab -u "${SUDO_USER:-$USER}" -

    # chmod 600  "/var/spool/cron/crontabs/${SUDO_USER:-$USER}"
    # chown "${SUDO_USER:-$USER}":crontab "/var/spool/cron/crontabs/${SUDO_USER:-$USER}"
}

function add_report_ip_to_thingsboard_to_cron() {
    local -r cron_command="/home/${SUDO_USER:-$USER}/pyduino/bash/send_ip_tb.sh"
    local -r cronjob="@reboot $cron_command"

    ( crontab -u "${SUDO_USER:-$USER}" -l | grep -v -F "$cron_command"; echo "$cronjob" ) | crontab -u "${SUDO_USER:-$USER}" -

    # To Remove
    # ( crontab -u ${SUDO_USER:-$USER} -l | grep -v -F "$cronjob" ) | crontab -u ${SUDO_USER:-$USER} -
}

function add_pyduino_arduino_library_symlink() {
    # Shouldn't be needed but if want to
    # Adds a Arduino/libraries symlink to pyduino/arduino/libraries
    mkdir "/home/${SUDO_USER:-$USER}/Arduino"
    ln -s "/home/${SUDO_USER:-$USER}/pyduino/arduino/libraries" "/home/${SUDO_USER:-$USER}/Arduino/libraries"
}

function create_thingsboard_ip_report_credentials() {
    local -r credential_file="/home/${SUDO_USER:-$USER}/pyduino/credential/tb.sh"
    local access_token
    local access_token_repeat

    if [ ! -f "$credential_file" ]; then
        while true; do
            # Get thingsboard Acess Token for IP address reporting
            # turn off terminal echoing
            read -r -p "Enter Access Token for IP Reporting: " access_token
            read -r -p "Repeat Access Token: " access_token_repeat
            echo # Turn it back on
            [ "$access_token" = "$access_token_repeat" ] && break
            echo "Please try again."
        done

        echo -e '#!/bin/bash\n' > "$credential_file"
        echo "TB_DOMAIN=\"monitoring.uqgec.org:8080\"" >> "$credential_file"
        echo "ACCESS_TOKEN=(\"$access_token\")" >> "$credential_file"
    fi
}

function configure_vimrc() {
    local -r VIMRC_FILE="/home/${SUDO_USER:-$USER}/.vimrc"
    local -r SOURCE_LINE="source \$VIMRUNTIME/defaults.vim"
    local -r DISABLE_MOUSE_Title="\" Disable mouse"
    local -r DISABLE_MOUSE_LINE="set mouse-=a"

    echo "Configuring \"$VIMRC_FILE\" ....."
    if [ ! -f "$VIMRC_FILE" ]; then
        # Create .vimrc
        echo > "$VIMRC_FILE"
        # echo -e "$SOURCE_LINE\n" > "$VIMRC_FILE"
        # echo -e "$DISABLE_MOUSE_Title\n$DISABLE_MOUSE_LINE" >> "$VIMRC_FILE"

        chown "${SUDO_USER:-$USER}":"${SUDO_USER:-$USER}" "$VIMRC_FILE"
        chmod 600 "$VIMRC_FILE"
    fi

    # Start Editting .vimrc

    # Add default .vimrc source if not found
    if ! grep -q "$SOURCE_LINE" "$VIMRC_FILE"; then
        sed -i "1 i\\$SOURCE_LINE" "$VIMRC_FILE"
    fi

    # Disable the mouse
    sed -i "s/^set\s*mouse\(-=|=\)\?\s*$/$DISABLE_MOUSE_LINE/" "$VIMRC_FILE"
    if ! grep -q "^$DISABLE_MOUSE_LINE$" "$VIMRC_FILE"; then
        echo -e "$DISABLE_MOUSE_Title\n$DISABLE_MOUSE_LINE" >> "$VIMRC_FILE"
    fi

    # Enable Line Number
    sed -i "s/^set\s*number\s*$/set number/" "$VIMRC_FILE"
    if ! grep -q "^set number$" "$VIMRC_FILE"; then
        echo -e "\" Enable Line Number\nset number" >> "$VIMRC_FILE"
    fi
}

# find ./install/ -type f -iname "*.sh" -exec chmod +x {} \;
# find ./install/ -type f -iname "*.sh" -exec chmod +x {} +;
# find ./install/ -type f -exec dos2unix {} \;
# git update-index --chmod=+x $script