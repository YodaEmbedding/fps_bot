A bot for reddit which increases fps of requested gifs/videos through motion interpolation.

To use, simply comment:

    /u/fps_bot

More options are described below.

## Usage

Simply leave a top-level comment in one of the following formats:

    /u/fps_bot           # auto
    /u/fps_bot 60        # 60fps
    /u/fps_bot 2x        # 2x frames
    /u/fps_bot 2x 0.5x   # 2x frames, but slow to 0.5x

(NOT IMPLEMENTED FULLY)

## Setup

An example `secret.json` config:

```json
{
    "reddit": {
        "client_id": "loRdOfThEriNGs",
        "client_secret": "ThEseArEnOtThEDrOiDsYouSeEk",
        "user_agent": "linux:com.github.someone.fps_bot:v0.1.0 (by /u/muntoo)",
        "username": "fps_bot",
        "password": "hunter2"
    },
    "gfycat": {
        "client_id": "iLiKeGiF",
        "client_secret": "0nc3uP0NaM1dN1gh7dr34rYwh1LEiP0nDeREdWe4kanDw34rYov3rM4nYaQuain7"
    }
}
```
