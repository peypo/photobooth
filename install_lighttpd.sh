#/bin/sh

# install photobooth www server

racine='/home/pi'
www='raw.githubusercontent.com/peypo/photobooth/draft---www-server'


function about()
{
    echo "Install all photobooth scripts"
    echo "usage: ./install.sh [[-h]]"
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

echo "Update sources lists from repository"

apt-get update

echo "Install Lighttpd webserver"

#sudo apt-get -y install lighttpd
sudo apt-get install lighttpd

echo "Install PHP server"

#sudo apt-get -y install php5-common php5-cgi php5
sudo apt-get install php5-common php5-cgi php5

sudo lighty-enable-mod fastcgi-php #Enable the Fastcgi module which will handle the PHP pages

sudo service lighttpd force-reload #restart the Lighttpd service

echo "Setup permissions"

sudo chown www-data:www-data /var/www

sudo chmod 775 /var/www #permission to write to this directory

sudo usermod -a -G www-data pi #add the “Pi” user to the “www-data” group

echo "Remove the default page"

rm /var/www/index.lighttpd.html

echo "Download the custom Photobooth pages"

cd /var/www/

if wget -r --no-parent $www/www/
	then
		echo "ok :-)"
	else
		echo "---> WARNING : Unable to get the photobooth pages"
		#echo "Cleaning and exiting..."
		#exit 1
fi

echo "Restart the server"

/etc/init.d/lighttpd force-reload