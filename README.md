--- For Blue Archive Players on Steam ---

For those of you playing the Steam version who enjoy digging into game files like I do (for editing photos, making videos, or whatever else), you might have noticed that after the recent update, the game has packaged all image files into a single file with the .molru extension.

Previously, if you wanted the images, you’d have to load that .molru file into a hex editor, filter out every single image hex code manually (I estimate there are over 1000 images), export them one by one, and then search for the needle in a haystack to find the exact one you need. Doing that is a massive headache and a waste of time (and I bet none of you are insane enough to actually do that manually).

So, I wrote a program (okay, I lied, I asked Gemini AI to write it and I just tweaked it to my liking). It can help you handle that entire process in under 5 seconds. All you need to do is select the .molru file in the program, and it will automatically export all the images for you.

The program has been checked on VirusTotal, so you can use it with peace of mind. If you get a virus warning, it’s likely a false positive - you can temporarily disable your antivirus or just ignore the warning.

Here are the locations of the .molru files (start from the drive where you installed Steam):

Prologue Chapter Images (The part you play while the game is installing data): Steam\steamapps\common\BlueArchive\BlueArchive_Data\StreamingAssets\PUB\Resource\Preload\MediaResources\UIs\03_Scenario

Images for the Entire Game: Steam\steamapps\common\BlueArchive\BlueArchive_Data\StreamingAssets\PUB\Resource\GameData\MediaResources\UIs\03_Scenario

(Note: In these folders, you can also find the game's video and audio files if you want to mess around with those too.)

If you have any issues, suggestions, or want any features added, just let me know, and I'll update the program regularly.

1. Run extractor.exe as administrator.
2. Click the "Chọn File" button.
3. Select the .molru or bundle file you want to unpack from your computer.
4. Click the red button "BẮT ĐẦU GIẢI NÉN (SMART SCAN)" to start.
5. Wait for the progress bar to finish. The folder containing the extracted images will open automatically.
