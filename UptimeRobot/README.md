# UptimeRobot translation for UptimeMatrix
> [!NOTE]
> Translation for UptimeMatrix **will not** work with the [dashboard](https://app.upptimematrix.com), you will not be able to modify your status-page manually

## Features:
- Whitelabel status-page
- Integrates with all UptimeMatrix-compatible themes
- Categories (See the [documentation](https://lyrdy.co/dko4) for usage)
- Automatic refresh script


## Requirements:
- An [UptimeRobot](https://uptimerobot.com/) account with an API key
- A working server running the translator and/or UptimeMatrix compatible status-page
- Crontab or similar software


## For UptimeRobot:
If you believe this repository is breaking your terms of service, please email us at contact@layeredy.com or create an issue.


## More information:
Your data will go to status.json once you run uptimerobot.py with an API key in .env, see env.example for example.

You will need to setup a venv to run this, see https://docs.python.org/3/library/venv.html for documentaton.

Use pip install -r requirements.txt to install all requirements (Use venv)

If you encounter any bugs or issues, please create an issue at https://github.com/layeredy/uptimematrix-translators/issues

This .json file will be overwritten upon first successfull startup of uptimerobot.py, if you need to see this file again, check the Github repository.
