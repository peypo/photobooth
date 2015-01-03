#/bin/sh

# install all photobooth scripts

racine='/home/pi'
www='raw.githubusercontent.com/peypo/photobooth/master'


function about()
{
    echo "Install all photobooth scripts"
    echo "usage: ./script.sh [[-h]]"
    echo "NB : root or sudo mode is required"
}

function line_break()
{
    local tmp
    if [[ "$1" == '' ]]; then
        tmp='-'
    else
        tmp=$1
    fi
    printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' "${tmp}"
}

# parameters
while [ "$1" != "" ]; do
    case $1 in
#        -u | --user )           shift
#                                user=$1
#                                ;;
        -h | --help )           about
                                exit
                                ;;
        * )                     about
                                exit 1
    esac
    shift
done

if [ "$(whoami)" != "root" ]; then
    echo "Sorry, this script must be executed with sudo or as root"
    exit 1
fi

line_break
echo "Updating sources"

sudo apt-get update

line_break
echo "Creating photobooth dedicated folders"

# /photobooth/pictures
# /photobooth/pictures/original
# /photobooth/pictures/montages
# /photobooth/pictures/tmp
# /photobooth/scripts
sudo mkdir -p $racine/photobooth/{scripts,pictures/{montages,original,tmp}}

line_break
echo "Downloading the photobooth scripts"

cd $racine/photobooth/scripts/

#sudo wget $(www)/check.py

#sudo wget raw.github.com/safay/RPi_photobooth/master/check.py
#sudo wget raw.github.com/safay/RPi_photobooth/master/assemble_and_print
#sudo wget raw.github.com/safay/RPi_photobooth/master/photo_booth.py
#sudo wget raw.github.com/safay/RPi_photobooth/master/startup_script

sudo chmod 755 $racine/photobooth/scripts/*

line_break
echo "Edit the printer name in the script"
# TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO
#Edit the "assemble_and_print" script. Change the "lp" line to include your printer name.
#sudo nano assemble_and_print
#^X to exit, save the changes
# TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO

line_break
echo "Install third-party libraries & app"

sudo apt-get install imagemagick
# python-numpy 
#sudo apt-get install imagemagick python-dev python-pip python-imaging libffi-dev libjpeg8-dev
#sudo pip install cffi
#sudo pip install jpegtran-cffi

sudo $racine/photobooth/scripts/install_gphoto.sh

#line_break
#echo "Last but not least : LED test"
#echo "Does it look like Christmas ? (The 3 led should blink)"

#sudo python $racine/photobooth/scripts/check.py

line_break
echo "Finished!! Enjoy it!"
line_break