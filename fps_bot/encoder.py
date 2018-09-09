import subprocess
# import butterflow

def encode_video(fname_input, fname_output):
    subprocess.call(['butterflow',
        '-audio',
        '-r', '2x',
        fname_input,
        '-o', fname_output])
