# JHack 2021

## What is JHack
JHack is a Hackathon for students around the Asian-Pacific region. For more information, visit our website at [www.jhack.tech](https://www.jhack.tech)

## How to Run
1. Install requirements with `pip install -r "requirements.txt"`. You should install them in a virtual environment.
2. Create a .env file inside `/application`. Set `SECRET_KEY`, `SQLALCHEMY_DATABASE_URI`, `MAIL_USERNAME`, `MAIL_PASSWORD` and `SENDGRID_API_KEY`. The email should be the same email as the one that is verified by Sendgrid.
3. Run `run.py`

To access the localhost from your devices on the same network, run using your local `198.168.x.x` IP address by changing the run.py file to
`app.run(host="192.168.x.x", debug=True)`

On a Mac, you can check this IP address from the Terminal by running `ipconfig getifaddr en0`