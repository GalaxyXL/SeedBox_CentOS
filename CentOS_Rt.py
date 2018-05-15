#CentOS 7.2 Integrate rtorrent installation
import subprocess

#Install dependency of rtorrent
class DependencyInstall(object):
    #Initial function
    def __init__(self):
        self.installSystemDependency()
        return

    #system dependency installation
    def installSystemDependency(self):
        p1 = subprocess.check_call(["yum","groupinstall","-y","Development Tools"], shell = 'False')
        p2 = subprocess.check_call(["yum", "install", "-y", "cppunit-devel", "libtool", "zlib-devel", \
        "gawk", "libsigc++20-devel", "openssl-devel", "ncurses-devel", "libcurl-devel", \
        "xmlrpc-c-devel", "unzip", "screen"], shell = 'False')
        return
    
#Get source code frome Github
class GitCloneSourceCode(object):
    #Initial function
    def __init__(self):
        return

    #Get libtorrent from Github
    def getLibtorrent(self):
        p1 = subprocess.check_call(["git", "clone", "https://github.com/rakshasa/libtorrent"], shell = 'False')
        return

    #Get rtorrent from Github
    def getRtorrent(self):
        p1 = subprocess.check_call(["git", "clone", "https://github.com/rakshasa/rtorrent"], shell = 'False')
        return

#Configure and Compile libtorrent
class ConfigureAndCompileLibtorrent(object):
    #Initial function
    def __init__(self):
        return

    #Go to libtorrent directory
    def goToLibtorrentDirectory(self):
        #Go to the libtorrent source code directory
        p1 = subprocess.check_call(["cd", "~"], shell = 'False')
        p2 = subprocess.check_call(["cd", "libtorrent"], shell = 'False')
        return
        
    #Configure Makefile
    def configureMakefile(self):
        #autogen and check
        output1 = subprocess.check_output(["./autogen.sh"]).decode('utf-8')
        if "ready to configure" not in output1:
            exit(1)
        
        #configure and check
        output2 = subprocess.check_output(["./configure", "--disable-debug"]).decode('utf-8')
        if "executing depfiles commands" not in output2:
            exit(2)
        return
    
    #Compile libtorrent
    def compileLibtorrent(self):
        #Compile and check
        output3 = subprocess.check_output(["make", "-j$(nproc)"]).decode('utf-8')
        if "Error" in output3:
            exit(3)

        #Installation
        p3 = subprocess.check_call(["make", "install"])
        #Go back home
        p4 = subprocess.check_call(["cd", "~"])
        return

#Configure and Compile rbtorrent
class ConfigureAndCompileRtorrent(ConfigureAndCompileLibtorrent):
    #Rewrite the method of go to
    def goToLibtorrentDirectory(self):
        #Go to the rtorrent directory
        p1 = subprocess.check_call(["cd", "~"])
        p2 = subprocess.check_call(["cd", "rtorrent"])
        return

    #Configure Makefile
    def configureMakefile(self):
        #autogen and check
        output1 = subprocess.check_output(["./autogen.sh"]).decode('utf-8')
        if "ready to configure" not in output1:
            exit(1)
        
        #configure and check
        output2 = subprocess.check_output(["./configure", "--with-xmlrpc-c", "--with-ncurses", "--enable-ipv6", "--disable-debug"]).decode('utf-8')
        if "executing depfiles commands" not in output2:
            exit(2)
        return

#Rtorrent Installation and running verification
class RtorrentRunningVerification(object):
    #Initial function
    def __init__(self):
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
        return

    #Creat rtorrent user
    def creatUserForRtorrent(self):
        global username
        username = "rtuser"
        p0 = subprocess.check_call(["adduser", username])
        return

    #Creat session and download directory
    def mkdirSessionAndDownload(self):
        p0 = subprocess.check_call("mkdir /home/" + username + "/.session", shell = True)
        p1 = subprocess.check_call("mkdir /home/" + username + "/rtdownloads", shell = True)
        p2 = subprocess.check_call("chmod -R 777 /home/" + username + "/.session", shell = True)
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

#Start rtorrent under rtuser
class RunningRtorrent(object):
    #Initial function
    def __init__(self):
        return
    
    #Start rtorrent under rtuser
    def startRtorrent(self):
        p0 = subprocess.check_call("sudo -u rtuser screen -dmS rtorrent /usr/local/bin/rtorrent", shell = True)
        return
    
#Install Nginx and related dependency and set config file
class NginxInstallationAndConfig(object):
    #Initial function
    def __init__(self):
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
        #Go to nginx config directory
        p0 = subprocess.check_call("cd /etc/nginx/", shell = True)
        #Get from githun
        try:
            p1 = subprocess.check_call("wget https://github.com/GalaxyXL/SeedBox_CentOS/raw/master/conf/nginx.conf -O nginx.conf", shell = True)
        except:
            print "Error Nginx config file"
            exit(1)
        return

    #Php-fpm config file set
    def setPhpFpmConfig(self):
        p0 = subprocess.check_call("sed -i \"s/apache/rtuser/g\" /etc/php-fpm.d/www.conf", shell = True)
        return

    #PHP-GeoIP config
    def setPhpGeoIpConfig(self):
        return

    #Set rutorrent password
    def setPassWordForRutorrent(self, password):
        #Creat password file
        p0 = subprocess.check_call(["htpasswd", "-cb", "/etc/nginx/rtpass", username, password])
        return

