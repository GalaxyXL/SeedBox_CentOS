#CentOS 7.2 Integrate rtorrent installation
import os
import getopt
import platform
import subprocess

httpfolder = "/usr/share/nginx/html/"
rtorrentuser = "rtuser"
password = "123456"

#Rtorrent Enviroment
new_env = os.environ.copy()
new_env['PKG_CONFIG_PATH'] = "/usr/local/lib/pkgconfig"

class SysRelated(object):
    def __init__(self):
        return
    
    def checkSystem(self):
        distribution = platform.linux_distribution()
        if "CentOS" not in distribution:
            print distribution[0] + "\nWrong System"
            exit(1)
        return

#Install dependency of rtorrent
class Rtorrent(object):
    #Initial function
    def __init__(self):
        self.installSystemDependency()
        self.getSourceCode()
        self.compileSource()
        self.getConfig()
        self.startRtorrent()
        self.installRutorrent()
        return

    #system dependency installation
    def installSystemDependency(self):
        p1 = subprocess.check_call(["yum","groupinstall","-y","Development Tools"], shell = False)
        p2 = subprocess.check_call(["yum", "install", "-y", "cppunit-devel", "libtool", "zlib-devel", \
        "gawk", "libsigc++20-devel", "openssl-devel", "ncurses-devel", "libcurl-devel", \
        "xmlrpc-c-devel", "unzip", "screen"], shell = False)
        return

    #Initial function
    def getSourceCode(self):
        self.getLibtorrent()
        self.getRtorrent()
        return

    #Get libtorrent from Github
    def getLibtorrent(self):
        try:
            p1 = subprocess.check_call(["git", "clone", "https://github.com/rakshasa/libtorrent"], shell = False)
        except:
            print "Get libtorrent error"
            exit(1)
        return

    #Get rtorrent from Github
    def getRtorrent(self):
        try:
            p1 = subprocess.check_call(["git", "clone", "https://github.com/rakshasa/rtorrent"], shell = False)
        except:
            print "Get rtorrent error"
            exit(1)
        return

    def compileSource(self):
        self.goToLibtorrentDirectory()
        self.configureLibtorrent()
        self.compileLibtorrent()
        self.goToRtorrentDirectory()
        self.configureRtorrent()
        self.compileLibtorrent()

        return

    #Go to libtorrent directory
    def goToLibtorrentDirectory(self):
        #Go to the libtorrent source code directory
        os.chdir("/root/libtorrent")
        return
        
    #Configure Makefile
    def configureLibtorrent(self):
        #autogen and check
        output1 = subprocess.check_output(["/root/libtorrent/autogen.sh"]).decode('utf-8')
        if "ready to configure" not in output1:
            print "autogen error"
            exit(1)
        
        #configure and check
        output2 = subprocess.check_output(["/root/libtorrent/configure", "--disable-debug"]).decode('utf-8')
        if "executing depfiles commands" not in output2:
            print "configure error"
            exit(1)
        return
    
    #Compile libtorrent
    def compileLibtorrent(self):
        #Compile and check
        output3 = subprocess.check_output("make -j$(nproc)", shell = True).decode('utf-8')
        if "Error" in output3:
            print "Compilation error"
            exit(1)

        #Installation
        p3 = subprocess.check_call(["make", "install"])
        #Go back home
        p4 = os.chdir("/root")
        return

    def goToRtorrentDirectory(self):
        #Go to the rtorrent directory
        os.chdir("/root/rtorrent")
        return

    #Configure Makefile
    def configureRtorrent(self):
        #autogen and check
        output1 = subprocess.check_output(["/root/rtorrent/autogen.sh"]).decode('utf-8')
        if "ready to configure" not in output1:
            exit(1)
        
        #configure and check
        output2 = subprocess.check_output(["/root/rtorrent/configure", "--with-xmlrpc-c", "--with-ncurses", "--enable-ipv6", "--disable-debug"], env = new_env).decode('utf-8')
        if "executing depfiles commands" not in output2:
            exit(2)
        return

    def getConfig(self):
        RtorrentConfig()
        return

    def startRtorrent(self):
        p0 = subprocess.check_call("sudo -u " + rtorrentuser + " screen -dmS rtorrent /usr/local/bin/rtorrent", shell = True)
        return

    def installRutorrent(self):
        Rutorrent()
        return

#Rtorrent Installation and running verification
class RtorrentRunningVerification(object):
    #Initial function
    def __init__(self):
        self.runRtorrent()
        self.checkRtorrent()
        self.killRtorrent()
        return

    #Run rtorrent
    def runRtorrent(self):
        self.p1 = subprocess.Popen(["screen", "-dmS", "rtorrent", "rtorrent"])
        return
    
    #Check rtorrent
    def checkRtorrent(self):
        p2 = subprocess.check_output(["ps", "-ef"])
        if "rtorrent" not in p2:
            exit(1)
        return

    #Kill rtorrent
    def killRtorrent(self):
        p3 = subprocess.check_call(["pkill", "rtorrent"])
        return

#Get config file for rtorrent
class RtorrentConfig(object):
    #Initial funcition
    def __init__(self):
        self.creatUserForRtorrent()
        self.mkdirSessionAndDownload()
        self.getConfigFileFromWeb()
        self.openPort()
        return

    #Creat rtorrent user
    def creatUserForRtorrent(self):
        global username
        username = "rtuser"
        p0 = subprocess.check_call(["adduser", username])
        return

    #Creat session and download directory
    def mkdirSessionAndDownload(self):
        p0 = subprocess.check_call("mkdir /.session", shell = True)
        p1 = subprocess.check_call("mkdir /home/" + username + "/rtdownloads", shell = True)
        p2 = subprocess.check_call("chmod -R 777 /.session", shell = True)
        return

    #Get config file from github
    def getConfigFileFromWeb(self):
        #Go to home directory
        p0 = subprocess.call("cd ~", shell = True)
        #Get File
        try:
            p1 = subprocess.check_call("wget https://github.com/GalaxyXL/SeedBox_CentOS/raw/master/conf/rtorrent.rc", shell = True)
        except:
            print "error"
        
        #Change file content and name
        p2 = subprocess.check_call("sed -i \"s/<username>/" + username + "/g\" rtorrent.rc", shell = True)
        p3 = subprocess.check_call(["mv", "rtorrent.rc", "/home/" + username + "/.rtorrent.rc"])
        return

    #Firewall port setting
    def openPort(self):
        p0 = subprocess.check_call("iptables -I INPUT -p tcp --dport 53698 -j ACCEPT", shell = True)
        p0 = subprocess.check_call("iptables -I INPUT -p tcp --dport 80 -j ACCEPT", shell = True)
        return
    
#Install Nginx and related dependency and set config file
class Rutorrent(object):
    #Initial function
    def __init__(self):
        self.installNginx()
        self.installRelatedDependency()
        self.setNginxConfigFile()
        self.setPhpFpmConfig()
        self.setPhpGeoIpConfig()
        self.setPassWordForRutorrent(password)
        self.getRutorrent()
        self.getRutorrentPlugin()
        self.startNginxAndPhpFpm()
        return

    #Install Nginx from epel-release
    def installNginx(self):
        p0 = subprocess.check_call(["yum", "install", "-y", "epel-release"])
        p1 = subprocess.check_call(["yum", "install", "-y", "nginx"])
        return

    #Install related dependency
    def installRelatedDependency(self):
        p2 = subprocess.check_call("yum install -y php-fpm httpd-tools php-cgi php-cli curl", shell = True)
        return

    #Nginx config file set
    def setNginxConfigFile(self):
        try:
            os.chdir("/etc/nginx")
            os.system("wget https://github.com/GalaxyXL/SeedBox_CentOS/raw/master/conf/nginx.conf -O nginx.conf")
        except:
            print "Error Nginx config file"
            exit(1)
        return

    #Php-fpm config file set
    def setPhpFpmConfig(self):
        p0 = subprocess.check_call("sed -i \"s/apache/" + rtorrentuser + "/g\" /etc/php-fpm.d/www.conf", shell = True)
        return

    #PHP-GeoIP config
    def setPhpGeoIpConfig(self):
        p0 = subprocess.check_call("yum install php-pecl-geoip -y", shell = True)
        p1 = subprocess.check_call("rm -f /usr/share/GeoIP/GeoIP.dat", shell = True)
        p2 = subprocess.check_call("cd /usr/share/GeoIP", shell = True)
        p3 = subprocess.check_call("wget http://geolite.maxmind.com/download/geoip/database/GeoLiteCountry/GeoIP.dat.gz", shell = True)
        p4 = subprocess.check_call("gunzip GeoIP.dat.gz", shell = True)
        p5 = subprocess.check_call("cd ~", shell = True)
        return

    #Set rutorrent password
    def setPassWordForRutorrent(self, password):
        #Creat password file
        p0 = subprocess.check_call(["htpasswd", "-cb", "/etc/nginx/rtpass", username, password])
        return

    #Start Nginx and PHP-FPM
    def startNginxAndPhpFpm(self):
        try:
            p0 = subprocess.check_output("systemctl start nginx.service", shell = True)
            p1 = subprocess.check_call("systemctl enable nginx.service", shell = True)
        except:
            print "Start Nginx Error"
            exit(1)
        try:
            p2 = subprocess.check_output("php-fpm -D", shell = True)
        except:
            print "Start Php-Fpm Error"
            exit(1)
        return

    #Download Rutorrent
    def getRutorrent(self):
        try:
            p0 = subprocess.check_call("git clone https://github.com/Novik/ruTorrent.git " + httpfolder + "rutorrent", shell = True)
        except:
            print "Download Rutorrent Error"
        p1 = subprocess.check_call("chown " + rtorrentuser + " -R /usr/share/nginx/html/rutorrent/share", shell = True)
        return
    
    #Rutorrent plugin
    def getRutorrentPlugin(self):
        try:
            p0 = subprocess.check_call("rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-EPEL-7", shell = True)
            p0 = subprocess.check_call("rpm --import http://li.nux.ro/download/nux/RPM-GPG-KEY-nux.ro", shell = True)
            p0 = subprocess.check_call("rpm -Uvh http://li.nux.ro/download/nux/dextop/el7/x86_64/nux-dextop-release-0-1.el7.nux.noarch.rpm", shell = True)
            p1 = subprocess.check_call("yum install -y ffmpeg unzip mediainfo rar unrar sox", shell = True)
        except:
            print "Rutorrent plugin install error"
        return

#Qbittorrent installation related
class Qbittorrent(object):
    def __init__(self):
        os.chdir("/root")
        self.installDependency()
        self.getLibtorrentRasterbar()
        self.configureLibtorrentRasterbar()
        self.getQbittorrent()
        self.configureQbittorrent()
        self.openPort()
        return

    #Install qt5 and development tools
    def installDependency(self):
        subprocess.check_output("yum -y groupinstall \"Development Tools\"", shell = True)
        subprocess.check_output("yum -y install qt-devel boost-devel openssl-devel qt5-qtbase-devel qt5-linguist", shell = True)
        return

    #Get libtorrent-rasterbar from web
    def getLibtorrentRasterbar(self):
        try:
            subprocess.check_call("wget https://github.com/arvidn/libtorrent/releases/download/libtorrent-1_1_5/libtorrent-rasterbar-1.1.5.tar.gz", shell = True)
            subprocess.check_call("tar xf libtorrent-rasterbar-1.1.5.tar.gz", shell = True)
        except:
            print "Get libtorrent-rasterbar error"
        return
        
    #configure and compile libtorrent-rasterbar
    def configureLibtorrentRasterbar(self):
        os.chdir("/root/libtorrent-rasterbar-1.1.5")
        os.system("./configure --disable-debug --prefix=/usr CXXFLAGS=-std=c++11")
        os.system("make")
        os.system("make install")

        #establish soft link
        subprocess.check_call("ln -s /usr/lib/pkgconfig/libtorrent-rasterbar.pc /usr/lib64/pkgconfig/libtorrent-rasterbar.pc", shell = True)
        subprocess.check_call("ln -s /usr/lib/libtorrent-rasterbar.so.9 /usr/lib64/libtorrent-rasterbar.so.9", shell = True)
        os.chdir("/root")
        return

    #Get qbittorrent from web
    def getQbittorrent(self):
        try:
            subprocess.check_call("wget https://github.com/qbittorrent/qBittorrent/archive/release-4.0.4.tar.gz", shell = True)
            subprocess.check_call("tar xf release-4.0.4.tar.gz", shell = True)
        except:
            print "Get Qbittorrent error"
        return

    #Configure and compile qbittorrent
    def configureQbittorrent(self):
        os.chdir("qBittorrent-release-4.0.4")
        os.system("./configure --disable-debug --prefix=/usr --disable-gui CPPFLAGS=-I/usr/include/qt5  CXXFLAGS=-std=c++11")
        os.system("make")
        os.system("make install")
        os.chdir("/root")
        print "qbittorrent install complete"
        return

    #Open port
    def openPort(self):
        subprocess.check_call("iptables -I INPUT -p tcp --dport 8080 -j ACCEPT", shell = True)
        subprocess.check_call("iptables -I INPUT -p tcp --dport 8999 -j ACCEPT", shell = True)
        return
            
#ServerSpeeder and BBR
class SpeederBBR(object):
    def __init__(self):
        return

    def checkKernel(self):
        return

    def changeKernel(self):
        return
    
    def installServerSpeeder(self):
        return

    def installBBR(self):
        return


def main():
    Rtorrent()
    Qbittorrent()

if __name__ == "__main__": main()

