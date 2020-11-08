DRIVE1="/Volumes/MyRAID"
DRIVE2="/Volumes/FUCKYOUWIND"

#diff <(ls -1a "${DRIVE1}") <(ls -1a "${DRIVE2}")


#1) list all directories on first drive
ls -d */

:'
Michaels-MacBook-Pro:WINDOWSDRIVE MichaelHackman$ ls -d */
$RECYCLE.BIN/
3DS SD contents/
Camera Uploads/
Games/
Music/
OS Images/
Play Piano Today Lessons/
Put these back in the Applications folder to make them work/
System Volume Information/
new dls/
new software/
new videos/
software/
special/
videos/
'

#2) list all directories on second drive

:'
Michaels-MacBook-Pro:MyRAID MichaelHackman$ ls -d */
3DS SD contents/
CMPUT301/
Camera Uploads/
Chambray Stems/
East West/
Export/
FEHIFHE/
Games/
Ha Gayyyyyyyy.band/
Interview with Michael 2.logicx/
Interview with Michael.logicx/
MUSIC FOR MIKE/
MacEwan_StudioB_Band_Tracking/
Music/
OS Images/
Play Piano Today Lessons/
Put these back in the Applications folder to make them work/
Put this into the root of a NTFS harddrive and it will be your windows 7 backup/
Quetzala:Jeff/
Reddit SongStems collection/
Spread Your Wings Backup/
Tasteful Dick Pics/
The Disaster Artist - My Life Inside the Room/
The Disaster Artist/
Tracks/
Virtual Machines/
new dls/
new software/
software/
special/
videos/
youtube/
'

#3) see which directories are missing from between the two and don't enter those:

:'
MyRAID/CMPUT301/
MyRAID/Chambray Stems/
...
'

#4) track the directories we do want to enter to continue diffing
#such as 3DS SD contents/


#5) now check which files are missing using `ls -1a` command
diff <(ls -1a "${DRIVE1}") <(ls -1a "${DRIVE2}")

#record the differences:
:'
"MyRAID/CMPUT301/" missing on WINDOWSDRIVE
"MyRAID/Chambray Stems/" missing on WINDOWSDRIVE
"MyRAID/Diff.sh/" missing on WINDOWSDRIVE
...
'

#6) now recurse, enter the first folder and repeat steps 1-6
#eventually you will reach a directory that has only files and you will back out of the recursion
#until you find a second directory (DFS basically)





