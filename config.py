import os


class Config(object):
    API_HASH = os.environ.get("202a9e8b13b7663417ddacc671420ad9")
    BOT_TOKEN = os.environ.get("6624007993:AAEzfv0DsHJ-byIdWD7ol-Pgw6dxc44RX9c")
    TELEGRAM_API = os.environ["28167530"]
    OWNER = os.environ.get("6440245883")
    OWNER_USERNAME = os.environ.get("ak_imax_premium")
    USERNAME = os.environ.get("Batman")
    PASSWORD = os.environ.get("Batman")
    DATABASE_URL = os.environ.get("mongodb+srv://jandu2:jandu2@cluster0.khgirye.mongodb.net/?retryWrites=true&w=majority")
    LOGCHANNEL = os.environ.get("-1002124078334")  # Add channel id as -100 + Actual ID
    GDRIVE_FOLDER_ID = os.environ.get("GDRIVE_FOLDER_ID", "root")
    USER_SESSION_STRING = os.environ.get("BAGtzWoAuPoOA5bQiHcIFUDho9VPKQNX8HO52b268CgrUV-utQwnZYC4L1iF1obGh38yZVEhySnuggRs5mfq9eWEHaOLZAAYlA0OvUEcKm9eEDdjGrNfBXJHmjzBRFZGxvaKJkm7Y0C-IxYmPkTBTxtfonP3VnS6u-afOkYwiVYXbWlkgzuOKb3P4buIPh8kattEqtBR8Aor5hIUkDK1-9eBiLB9ScTycOKhKVv3S5YV_YFZ-onWabff2mFNVUumPDYUN3g6qt7LPG1mST8PT_yQ5xvAIHMu3edbVfwzTwzY3qQioVYAZy-56Ty0uMpMvpG3CiZJsFSxMwNQ3MRh_i-DRBWygQAAAAF_3lp7AA", None)
    IS_PREMIUM = True
    MODES = ["video-video", "video-audio", "video-subtitle", "extract-streams"]
