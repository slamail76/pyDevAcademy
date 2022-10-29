from pytube import Playlist
from pathlib import Path
playlist = Playlist('https://www.youtube.com/playlist?list=PLqRTLlwsxDL_O2e73lHQvJyucwpcMQUnO')
Path('all.txt').write_text("\n".join(playlist))


#Then I manually (depends of the size of video and youtube algorithm to block ip) select first n items, and put them in a separate file called (part.txt), then use this one to download first n ones,

for name in $(cat part.txt);do pytube $name;done
#Then after some time, I would download some more ...