import logging
import subprocess

logger = logging.getLogger('fps_bot')

def encode_video(fname_input, fname_output):
    logger.info('Encoding...')
    subprocess.call(['butterflow',
        '-audio',
        '-r', '2x',
        fname_input,
        '-o', fname_output])
