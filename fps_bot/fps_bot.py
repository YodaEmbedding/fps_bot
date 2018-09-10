from functools import wraps
from getpass import getpass
from time import sleep, time
import json
import logging
import pfycat
import praw
import sys
import youtube_dl

from encoder import encode_video

# TODO
# def process_messages(msgs):
#     for msg in msgs:
#         if not isinstance(msg, praw.models.Comment) or not msg.is_root:
#             continue
#
#         # do processing, sanitize inputs
#         # then pass msg and only if it passes validity checks
#         # e.g. valid domains, url formats (regex?)
#         yield msg

def timed(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        start = time()
        result = f(*args, **kwargs)
        dt = time() - start
        return dt, result

    return wrapper

def url_to_filename(url):
    s = url.split('/')[-1]
    basename = "".join(c if c.isalnum() else "_" for c in s)
    return f"{basename[:64]}.mp4"

def download_video(url, filename):
    logger.info('Downloading...')
    ydl_args = {
        'outtmpl': filename,
        'restrictfilenames': True }
    with youtube_dl.YoutubeDL(ydl_args) as ydl:
        ydl.download([url])

# TODO ewww passing in gfycat as argument
def upload_video(gfycat, filename):
    logger.info('Uploading...')
    d = gfycat.upload(filename)
    return f"https://gfycat.com/{d['gfyname']}"

def shrink_text(level, msg):
    return f'{"^" * level}{msg.replace(" ", "&nbsp;")}'

def make_reply(url, footer, times):
    time_names = ['Download', 'Encode', 'Upload']
    time_msg = shrink_text(1,
        ', '.join(f'{s} {int(t)}s' for s, t in zip(time_names, times)))
    return '\n\n'.join([url, time_msg, '---', footer])

def logging_setup():
    global logger

    file_formatter = logging.Formatter(
        '%(asctime)s | %(levelname)s | %(name)s | %(message)s')
    file_handler = logging.FileHandler(filename='../log/fps_bot.log')
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(logging.DEBUG)

    stdout_formatter  = logging.Formatter('%(message)s')
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(stdout_formatter)
    stdout_handler.setLevel(logging.INFO)

    logging.basicConfig(
        level=logging.DEBUG,
        handlers=[file_handler, stdout_handler])

    logger = logging.getLogger('fps_bot')

def comment_permalink(msg):
    return (f'https://reddit.com{msg.submission.permalink}{msg.id}')

def main():
    with open('secret.json') as f:
        secret = json.load(f)
    reddit_args = secret['reddit']
    gfycat_args = secret['gfycat']

    if reddit_args['password'] == '':
        reddit_args['password'] = getpass('Password: ')

    reddit = praw.Reddit(**reddit_args)
    #gfycat = pfycat.Client(**gfycat_args)
    gfycat = pfycat.Client()

    _download_video = timed(download_video)
    _encode_video   = timed(encode_video)
    _upload_video   = timed(upload_video)

    msg_footer = shrink_text(2,
        '[usage](https://github.com/SicariusNoctis/fps_bot) | '
        '[report issue](https://github.com/SicariusNoctis/fps_bot/issues) | '
        '[source code](https://github.com/SicariusNoctis/fps_bot)')

    logger.info('Run started')

    while True:
        for msg in reddit.inbox.unread():
            if not isinstance(msg, praw.models.Comment) or not msg.is_root:
                continue

            msg.mark_read()
            request = msg.body.split('\n', 1)[0]
            url_download = msg.parent().url
            fname_download = url_to_filename(url_download)
            fname_upload = f"enc-{fname_download}"
            times = []

            logger.info(f'Comment: {comment_permalink(msg)}')
            logger.info(f'Request: {request}')
            logger.info(f'Link:    {url_download}')

            t, _ = _download_video(url_download, fname_download)
            times.append(t)
            t, _ = _encode_video(fname_download, fname_upload)
            times.append(t)
            t, url_upload = _upload_video(gfycat, fname_upload)
            times.append(t)

            logger.info(f'Result:  {url_upload}')
            reply = msg.reply(make_reply(url_upload, msg_footer, times))
            logger.info(f'Reply:   {comment_permalink(reply)}')

        logger.debug('Sleeping 10s...')
        sleep(10)

# gfycat = pfycat.Client()
#
# _download_video = timed(download_video)
# _encode_video   = timed(encode_video)
# _upload_video   = timed(upload_video)
#
# request = '/u/fps_bot 2x'
# url_download = 'https://gfycat.com/gifs/detail/deadlydeafeningatlanticblackgoby'
# fname_download = url_to_filename(url_download)
# download_video(url_download, fname_download)
#
# fname_upload = f"enc-{fname_download}"
# encode_video(fname_download, fname_upload)
# url_upload = upload_video(gfycat, fname_upload)
# print(url_upload)

logging_setup()
main()
# encode_video('input.mp4', 'output.mp4', '/u/fps_bot 2x 0.5x')

# Connect to reddit account
# Monitor for mentions
# Download from gfycat (use youtube-dl?)
# Encode
# Upload to gfycat
# Reply to comment

# TODO
# Args: reverse video (maybe a separate bot)
# Break into multiple files
# Warnings (e.g. NSFW)
# Clever replies? :P
# Makefile lint
# Redirect PMs to /u/muntoo? Or reply with "please contact /u/muntoo or post issue on github (more likely to respond)"
# gfycat mark NSFW
# Cache/lookup table
# Remove download/upload videos once completed?
# Reencode as gyfcat webm
# Work with non-top level (use nearest mention of valid domain)
# Reject invalid domains
# setup.py; setup requirements, instructions
# Max length; rescale resolution
# Lower output quality (faster encode)
# Support for i.reddit, gifs, giphy
# GIF->mp4 conversion (https://unix.stackexchange.com/questions/40638/how-to-do-i-convert-an-animated-gif-to-an-mp4-or-mv4-on-the-command-line)
