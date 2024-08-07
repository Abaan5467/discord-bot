# Owais Dar bot
**Discord bot inspired by Owais Dar Martial Art**

<ul>
<li>Play music from a file</li>
<li>Run a chemistry quiz</li>
<li>Send memes or videos from a folder to a channel</li>
</ul>
.... and many other features will be added soon

#How to run
**First make sure discord and dotenv modules are installed on your pc**
To do that, first run this command

```sh
pip install discord
```
Then run this command:

```sh
pip install python-dotenv
```
You also need to install ffmpeg for the music feature to work. Download ffmpeg [here](https://www.gyan.dev/ffmpeg/builds/packages/ffmpeg-2024-07-10-git-1a86a7a48d-full_build.7z)



Then go to the .env file and change the following variables: <br>
```env
TOKEN = ''
FFMPEG_PATH = ''
MEMES_FOLDER = ''
```