import sys
import logging
import pexpect

process = pexpect.spawn('/usr/local/bin/adb shell')
process.logfile = sys.stdout.buffer

def sendCmd(cmd, timeout=-1):
    process.expect('# ', timeout=timeout)
    process.sendline(cmd)

cmds = """
duelLinksDataDir="/data/data/com.netease.ma84.bilibili"
sharedDir="/sdcard/\$MuMu共享文件夹"
outputDir="outputs"
gzFiles="duelLinkDataFiles.tar.gz"
cd $duelLinksDataDir
# touch $gzFiles
tar -zcf $gzFiles files
mv $gzFiles $sharedDir
cd $sharedDir
if [ -d $outputDir ]; then rm -rf $outputDir; fi
mkdir $outputDir
tar -zxf $gzFiles -C $outputDir
exit
"""
for cmd in cmds.split("\n"):
    logging.debug(f'run {cmd}')
    sendCmd(cmd, timeout=None)
