import logging
import re
import subprocess

logger = logging.getLogger('fps_bot')

# How to write unmaintainable gross parsers 101
def request_to_args(request):
    words = re.split(r'\s+', request)
    args = []

    if words[0] != '/u/fps_bot':
        raise Exception('Request invalid: missing /u/fps_bot')

    if len(words) == 1:
        return ['-r', '2x']

    if words[1] == '1x':
        pass
    elif re.match(r'^\d+(\.\d+)?x?$', words[1]):
        args.extend(['-r', words[1]])
    elif re.match(r'^\d+(\.\d+)?fps$', words[1]):
        args.extend(['-r', words[1][:-3]])
    else:
        raise Exception('Request invalid: incorrect format for framerate')

    if len(words) == 2:
        return args

    if words[2] == '1x':
        pass
    elif re.match(r'^\d+(\.?\d+)x$', words[2]):
        args.extend(['-s', f'a=0,b=end,spd={words[2][:-1]}'])
    else:
        raise Exception('Request invalid: incorrect format for speed')

    return args

def encode_video(fname_input, fname_output, request):
    logger.info('Encoding...')
    args = request_to_args(request)
    subprocess.call(['butterflow', *args, fname_input, '-o', fname_output])
