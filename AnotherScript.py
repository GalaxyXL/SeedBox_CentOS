#Another script for seedbox installation
import os
import subprocess

#Download source code
class DownloadFile(object):
    def __init__(self, name, version):
        self.name = name
        self.version = version
        return

    #Directory change
    def changeDirectory(self):
        defaultdir = os.path.expanduser("~")
        os.chdir(defaultdir)
        return

    #download file from url
    def downloadFile(self, url, filename = None):
        if not filename:
            subprocess.check_output("wget -O " + filename + " " + url, shell = True)
        else:
            subprocess.check_output("wget " + url, shell = True)
        return

    #tar
    def uncompressedTarGz(self, filename):
        outname = subprocess.check_output("tar -tf " + filename + " | awk -F \"/\" \'{print $1}\' | sort | uniq", shell = True)
        subprocess.check_call("tar xf " + filename, shell = True)
        return outname[:-1]

    #Qbittorrent related
    def getLibtorrentRasterbar(self, version):
        self.changeDirectory()
    
        #Split version string
        strset = version.split(".")

        #download source code from web
        filename = "libtorrent-rasterbar-" + version + ".tar.gz"
        url = "https://github.com/arvidn/libtorrent/releases/download/libtorrent-1_" \
        + strset[1] + "_" + strset[2] + "/libtorrent-rasterbar-" + version + ".tar.gz"
        self.downloadFile(url, filename)
        self.libtrdir = self.uncompressedTarGz(filename)
        return

    def getQbittorrent(self, version):
        self.changeDirectory()

        #download source code from web
        filename = "release-" + version + ".tar.gz"
        url = "https://github.com/qbittorrent/qBittorrent/archive/release-" + version + ".tar.gz"
        self.downloadFile(url, filename)
        self.qbdir = self.uncompressedTarGz(filename)
        return

    #Rtorrent related
    def getLibtorrent(self, version = None):
        self.changeDirectory()

        #download source code from web
        if version == None:
            subprocess.check_call("git clone https://github.com/rakshasa/libtorrent")
            self.libtdir = "libtorrent"
        else:
            filename = version + ".tar.gz"
            url = "https://github.com/rakshasa/libtorrent/archive/" + version + ".tar.gz"
            self.downloadFile(url, filename)
            self.libtdir = self.uncompressedTarGz(filename)
        return


    def getRtorrent(self, version = None):
        self.changeDirectory()

        #download source code from web
        if version == None:
            subprocess.check_call("git clone https://github.com/rakshasa/rtorrent")
            self.rtdir = "rtorrent"
        else:
            filename = version + ".tar.gz"
            url = "https://github.com/rakshasa/libtorrent/archive/" + version + ".tar.gz"
            self.downloadFile(url, filename)
            self.rtdir = self.uncompressedTarGz(filename)
        return

    def getRutorrent(self):
        # subprocess.check_call("git clone https://github.com/Novik/ruTorrent.git "  + "rutorrent", shell = True)
        return

#Compile the source code
class CompileSourceCode(object):
    def __init__(self, pwd, argv = []):
        self.libToRaArgv = ["--disable-debug", "--prefix=/usr", "CXXFLAGS=-std=c++11"]
        self.qBitArgv = ["--disable-debug", "--prefix=/usr", "--disable-gui", "CPPFLAGS=-I/usr/include/qt5", "CXXFLAGS=-std=c++11"]
        self.libToArgv = ["--disable-debug"]
        self.rToArgv = ["--with-xmlrpc-c", "--with-ncurses", "--enable-ipv6", "--disable-debug"]
        return

    #Generate config file
    def generateConfigureFile(self, pwd):
        subprocess.check_output(pwd + "/autogen.sh")
        return

    #Configure
    def configureMake(self, pwd, argList = []):
        os.chdir(pwd)
        cmd = pwd + "/configure"
        argList.insert(0, cmd)
        subprocess.check_output(argList)
        os.system("make")
        os.system("make install")
        os.chdir(os.path.expanduser("~"))
        return

class Denpendency(object):
    def __init__(self):
        subprocess.check_call(["yum","groupinstall","-y","Development Tools"])
        return

    def installRtorrentRelated(self):
        subprocess.check_call(["yum", "install", "-y", "cppunit-devel", "libtool", "zlib-devel", \
        "gawk", "libsigc++20-devel", "openssl-devel", "ncurses-devel", "libcurl-devel", \
        "xmlrpc-c-devel", "unzip", "screen"])
        return

    def installQbittorrentRelated(self):
        subprocess.check_call("yum -y install qt-devel boost-devel openssl-devel qt5-qtbase-devel qt5-linguist", shell = True)
        return

    def installRutorrentRelated(self):
        subprocess.check_call(["yum", "install", "-y", "epel-release"])
        subprocess.check_call(["yum", "install", "-y", "nginx"])
        subprocess.check_call("yum install -y php-fpm httpd-tools php-cgi php-cli curl", shell = True)
        subprocess.check_call("rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-EPEL-7", shell = True)
        subprocess.check_call("rpm --import http://li.nux.ro/download/nux/RPM-GPG-KEY-nux.ro", shell = True)
        subprocess.check_call("rpm -Uvh http://li.nux.ro/download/nux/dextop/el7/x86_64/nux-dextop-release-0-1.el7.nux.noarch.rpm", shell = True)
        subprocess.check_call("yum install -y ffmpeg unzip mediainfo rar unrar sox", shell = True)
        return

class ConfigOthers(object):
    def __init__(self):
        return

    def dealRtRelated(self):
        return




