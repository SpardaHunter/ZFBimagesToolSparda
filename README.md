# ZFBimagesToolSparda

Description: Generates ZFB files. The program integrates an image and the shortcut where the rom is stored en masse.

![imagen](https://github.com/user-attachments/assets/c23cdca6-853e-4556-8bc3-0310940f61f0)


How it works:
- Select the folder where you have the images with the "Input Folder" button. IMPORTANT: the images must have the same name as the roms.
- Select the destination folder where you want the ZFB files to be saved with the "Output Folder" button.
- Click the "ARCADE" checkbox if you want to generate ZFB files from the roms stored in "ARCADE/bin".
- Write in "CORE:" the core from which you are going to load the rom.
- Write in "EXTENSION" the extension that the rom files have (example: If the "Super Nintendo" roms are .sfc, write sfc)
- Image size: You can edit the size of the preview images of each game. With the "Fulscreen" checkbox you can create full-size images, ideally combining this method with "Game Cover Generator"
- Press the "Create ZFB files" button to start the process.

Additional explanation: 
- Added "STOP" button to stop the process.
- Added "auto" button, it will create the ZFB file with the size of the image itself. 
- If the "Create ZFB Files" or "STOP" button is selected, pressing Enter will cause the button to be pressed.
- The buttons (except the Stop button) will be blocked when pressing the "Create ZFB Files" button.
- In "manual" mode, an error will occur if a size smaller than 144x208 is selected.
- In "auto" mode, if an image is smaller than 144x208, it will be resized in the ZFB to 144x208.

IMPORTANT: The SF2000 console must be configured according to the size in Foldername.ini/FoldernamX.ini.

Credits: Q_ta has made contributions to this distribution.

IMPORTANT: The SF2000 console must be configured according to the size in Foldername.ini/FoldernamX.ini.

Credits: Q_ta has made contributions to this distribution.
