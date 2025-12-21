--- For fellow Blue Archive players on Steam ---

For those of you playing the Steam version who enjoy digging into game files like I do (for editing images, making videos, or whatever else), you might have noticed that after the recent update, the game has packaged all image files into a single file with the .molru extension.

Previously, if you wanted the images, you’d have to load that .molru file into a hex editor, filter out every single image hex code manually (I estimate there are over 1000 images), export them one by one, and then search for the needle in a haystack to find exactly what you need. Doing that is a massive headache and a waste of time (and I bet none of you are actually insane enough to do that manually).

So, I wrote a program (okay, I lied, I asked Gemini AI to write it and I just tweaked it to my liking). It can handle that entire process for you in under 5 seconds. All you need to do is input the .molru file path into the program, and it will automatically export all the images for you. The program has been verified on VirusTotal, so you can use it with peace of mind. If you get a virus warning, just temporarily disable your antivirus or ignore it (it's likely a false positive).

Here are the paths to the .molru files for you to choose from (start from the drive where you installed Steam):

Prologue Images (The part you play while the game is installing data): Steam\steamapps\common\BlueArchive\BlueArchive_Data\StreamingAssets\PUB\Resource\Preload\MediaResources\UIs\03_Scenario

Images for the entire game: Steam\steamapps\common\BlueArchive\BlueArchive_Data\StreamingAssets\PUB\Resource\GameData\MediaResources\UIs\03_Scenario

(Note: In these folders, you can also find the game's video and audio files if you want to mess around with those too.)

If you have any issues, suggestions, or want to add/remove features, just let me know, and I'll update the program regularly. Enjoy!

Update: I've added a feature to extract both Audio and Video formats (even though game video files aren't usually compressed this way). You can find the .molru files containing audio in the folders named Audio. These files include student voice lines, background music (BGM), and sound effects (SFX).

1. Right-click BA Steam file extractor.exe and select "Run as Administrator" (recommended to avoid permission errors).
2. Click the "..." button (or "Chọn File") to browse for files.
3. Navigate to the Blue Archive data folder and select the .molru file you want to unpack.
4. Click the big Green button "BẮT ĐẦU QUÉT & GIẢI NÉN" (Start Scan & Extract).
5. Wait for the progress bar to finish. The tool will automatically open a new folder containing your extracted files, neatly organized into subfolders (jpg, png, ogg, webm, etc.).

(Note: If you extract the same file twice, don't worry - the tool will create a new folder like "FolderName (1)" so it won't overwrite your previous work.)
