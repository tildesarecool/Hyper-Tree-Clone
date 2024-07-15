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

##### 13 July 2024

I made a quite a lot of progress today. In theory anyway. I tried to add some edge cases and added in support for command line arguments instead of using constants for the tests. I also tried to add in a progress indicator where it just added a # every so many seconds. Just so it's easy to tell stuff is happening and it's not locked up. Not a progress bar, more of a "something is happening indicator". I don't think it's working correctly, though. I may take it out or use something more based on how much has been copied.

Also, I've found a pretty good way to (unscientifically) benchmark the script: I have a USB drive with a directory try I was trying to keep synced across multiple locations. The size of which has ballooned to ~35 gigabytes of files of all sizes. And I already have a prepared robocopy line (as a batch file). 

This will from a USB 3 storage drive (I think it's an NVME inside) to my nvme internal storage device. An empty folder so it's not overwriting anything.

And I don't think it matters but I'm running this via powershell in in Windows Terminal 7.4.3.

Test one with robocopy line:

```robocopy "F:\Windows Install Customization" "P:\Windows Install Customization" /mir  /r:1 /w:1```

Final Time: 
2 min 3 seconds
I think. Robocopy output is kind of confusing. Here's the output at the end of the copy, you can be the judge.
```
------------------------------------------------------------------------------

               Total    Copied   Skipped  Mismatch    FAILED    Extras
    Dirs :       938       938         0         0         0         0
   Files :      7390      7390         0         0         0         0
   Bytes :  32.590 g  32.590 g         0         0         0         0
   Times :   0:02:03   0:01:54                       0:00:00   0:00:08


   Speed :           304534234 Bytes/sec.
   Speed :           17425.588 MegaBytes/min.
   Ended : Saturday, July 13, 2024 17:55:02
```



Test one with HyperTreeClone

I'm using a different physical drive as a destination. Still on the root though. There's a few hundred variables I'm not accounting for. But I figure root-to-root is close enough. And also I made sure the C: drive had abundant free storage space like my P: drive. The C: drive has 83 gigs free, ready for 35 gig file copy.

```HyperTreeClone.py "F:\Windows Install Customization" "C:\Windows Install Customization"```

7 minutes 27.36 minutes(?)

Since the two are so far off I'm going to use HyperCloneTree against my P: drive as another test. I deleted the existing *Windows Install Customization* folder and decided to try it again.

Test 2 of HyperTreeClone, command line

```HyperTreeClone.py "F:\Windows Install Customization" "P:\Windows Install Customization"```

2 minutes 7.12 seconds

Well much closer. Apparently my C: drive is not very fast. And the script is barely comparable with robocopy. 

##### 14 July 2024

It took a while but the script is creating a message pack binary based on the directory tree. I haven't actually tried a file copy with it yet, just managed to have it create a message pack binary. 