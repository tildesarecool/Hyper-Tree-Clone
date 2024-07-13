# Hyper Tree Clone

### Extremely fast directory tree duplicator for Windows.

12 July 2024

This is something of a utility spin off from another script I am developing called [tiny11 python edition](https://github.com/tildesarecool/Tiny11PyEd). Which in turn is heavily inspired by a PowerShell script called Tiny11.

I wanted to see how fast of a file copy utility I could make after watching and reading several things about the [1 billion row challenge](https://github.com/gunnarmorling/1brc/tree/main?tab=readme-ov-file) and associated Python version of the solution (all of which is entirely over my head).

I'm hoping to have some (very unscientific) time comparisons between reguarly drag/drop file copy, robocopy and this script. As well as comparisons on different sets of hardware. The benchmark against which all will be tested will be a Windows 11 install ISO.

#### Dev log

##### 12 July 2024

Compared to same operation from drag and drop windows copy...I saved a whole 4 seconds. 

As it turns out on this particular PC with this particular NVME drive copying the contents of the Windows 11 install CD from folder to folder on the same drive doesn't actually take that long anyway. It was from ~11 seconds to ~6.3 seconds btw.

Despite this I decided to continue working on the utility as it could hypothetically make a difference when copying to and from a USB thumb drive for instance. Somewhere the actual bus would be the bottle neck. And I wanted to.

I've already made one step forward while testing with a thumb drive: take some alternative action when the destination of the copy is FAT32 and the source contains a file exceeding 4 Gigabytes - the max file size of FAT32. 

I re-formatted the drive to exFAT and the test copy with the ~5 gig WIM copied in 773.8 seconds (12.88 minutes). Should probably calculate that as minutes/seconds. I did the same copy with drag-and-drop windows copy and it took 14 minutes 10 seconds. Other variables like contigoiusness of the flash not withstanding. Not scientific, obviously. I'm sure the file group/chunking still had something to do with it. I'm sure I can get it faster.