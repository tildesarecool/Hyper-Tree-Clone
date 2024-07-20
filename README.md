# Hyper Tree Clone

### ~~Extremely~~ Theoreticallly somewhat fast directory tree duplicator for Windows.

This is something of a utility spin off from another script I am developing called [tiny11 python edition](https://github.com/tildesarecool/Tiny11PyEd). Which in turn is heavily inspired by a PowerShell script called Tiny11 (which in turn is inspired by something else...and so on).

I wanted to see how fast of a file copy utility I could make after watching and reading about the [1 billion row challenge](https://github.com/gunnarmorling/1brc/tree/main?tab=readme-ov-file) and associated Python version of the solution (all of which is entirely over my head).

I'm hoping to have some (very unscientific) time comparisons between reguarly drag/drop file copy, robocopy and this script. As well as comparisons on different sets of hardware. The benchmark against which all will be tested will be a Windows 11 install ISO.

Notes: 
* this utility **does note** claim to be faster than xcopy or robocopy and is **is not** claiming to be a replacement.
* As mentioned in the title this script is **only tested on Windows and only intended for Windows** (for linux etc there's about 1,000 copy utilities.)
* I am a beginner level programmer and therefore this script is not intended for production use in any way. 


**update 19 July:** I made it to a major milestone today in as much as the script does in fact copy files from a source to a destination based on either a source drectory path or a message pack binary file with the source information embedded in it. 

Examples of usage:

Normal copy of folder tree:
**--copy**
```.\HyperTreeClone.py  --copy <source folder>  <destination folder>```

Example:
```.\HyperTreeClone.py  --copy "P:\Windows Install Customization" "P:\Windows Install Customization_copy"```
Note the double quotes around the paths: for paths with spaces these are not optional.

Create a message pack binary file based on the root of a folder tree (the "source" if you will):
**--create_msgpack**

```.\HyperTreeClone.py  --create_msgpack <source folder> ```

This will create a message pack file in the current directory where the script is beign run with a default file name, which is currently directory_tree.msgpack

Example:
```.\HyperTreeClone.py  --create_msgpack "P:\Windows Install Customization" ```


Using a created message pack file as the source for the file copy. There's no check or warning before the operation yet though, so re-create the message file if there's any doubts about it being the wrong one. Or just rename the message pack file manually immediately after creating it.

**--use_msgpack**
The argument takes the form:
```.\HyperTreeClone.py  --use_msgpack "directory_tree.msgpack" <destination folder>"```

Example:
```.\HyperTreeClone.py  --use_msgpack "directory_tree.msgpack" "P:\Windows Install Customization_copy_2"```
Any valid message pack file can be used here, but the script does check on the **.msgpack** file extension - it doesn't error out if a different filename from "directory_tree.msgpack" is used, other words.


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

##### 15 July 2024

The good news and the bad news.

I got the file copying to work using a a binary file as the reference. Basically the "source" of the file copy operation is this message pack file. It ook entirely too long to get to work.

The bad news is that it's some how a slower copy operation than just using drag/drop to copy when I tested it.

Also bad news against my better judgement I used a lot of GPT assistance to writ the functionality. Like a lot. So although it technically works the code is an extreme mess. I'm just resigned to the assumption I'll be re-writing the whole thing from scratch. Which is likely what I would end up doing anyway.  Abandon all hope any who dare to try and veiw the code. It will not go well.

##### 19 July 2024

Note: below isn't necessarily supposed to imply work will stop on this script, it's more of a noteworthy checkpoint.

Well there's mostly good news today: the script is now working. By which I mean all three arguments are working without errors and succesfully copying files. 

Here's the latest test results:

test condiations:
internal nvme->internal nvme
directory with total size of 16MBs
Tree consists entirely of files less than 50KBs

normal file copy using --copy:
5 seconds

same tree file copy using msgpack:
26 seconds

so apparently this isn't optmized for a tree that's entirely small files

Second test tree:
internal nvme->internal nvme
tree has a total of ~30 gigabytes
mixture of file sizes from a few KBs to 5+ GBs

normal file copy using --copy:
8 min 34 seconds

same tree file copy using msgpack:
2 min 45 seconds

Much greater difference in copy operations between the two and clearly the msgpack approach is better.

It occured to me I should probably test the mounted ISO copy since that was the original reason I wanted to make this copy utility.

I used the unmodified Win 11 ISO downloaded from Microsoft mounted on an internal NVME drive. And copied the contents to a folder on the same NVME drive:

Total size: 6.34GBs
First, create the msgpack file:
``` .\HyperTreeClone.py  --create_msgpack "G:"``` 
Then, try the file copy with the msgpack file:
```.\HyperTreeClone.py  --use_msgpack "directory_tree.msgpack" "P:\Windows Install Customization_copy_2"```

Time reported: 54 seconds

Then same file copy with plain file copy:
```.\HyperTreeClone.py  --copy "G:" "P:\Win11DVD_2"```

Time reported: 44 seconds

This kind of a depressing result considering I thought using a binary file reference would be faster than a plain file copy. 



The bad news?

There's quite a few "long hanging fruit" improvements to make:

* custom file name for the msgpack file/generate a file name based on path it was created in combination with something else like a date stamp
* a way to "query" a msgpackfile to confirm the path it was pointed at when created
* let the user decide to overwrite or not existing files in a destination
* I would like to have an option of using a message pack file or text-based file like JSON. For testing and troubleshooting if nothing else.

Besides that the code needs to be cleaned up for readaibility, documentation and the argument help needs much better wording and extensive examples.

Actually, even worse: I used a stop watch and tested a plain old drag-and-drop copy of the same tree 
and got **17 seconds**. 

So I went through these 8 days or so of creating this side utility to...create a script that's 
somehow slower then Windows copy. Yea?