import os


class Config(object):
    API_HASH = os.environ.get("API_HASH", "202a9e8b13b7663417ddacc671420ad9")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "6624007993:AAEzfv0DsHJ-byIdWD7ol-Pgw6dxc44RX9c")
    TELEGRAM_API = os.environ["TELEGRAM_API","28167530"]
    OWNER = os.environ.get("OWNER", "6440245883")
    OWNER_USERNAME = os.environ.get("OWNER_USERNAME", "ak_imax_premium")
    USERNAME = os.environ.get("USERNAME", "Batman")
    PASSWORD = os.environ.get("PASSWORD", "Batman")
    DATABASE_URL = os.environ.get("DATABASE_URL", "mongodb+srv://jandu2:jandu2@cluster0.khgirye.mongodb.net/?retryWrites=true&w=majority")
    LOGCHANNEL = os.environ.get("LOGCHANNEL, "-1002124078334)  # Add channel id as -100 + Actual ID
    GDRIVE_FOLDER_ID = os.environ.get("GDRIVE_FOLDER_ID", "root")
    USER_SESSION_STRING = os.environ.get("USER_SESSION_STRING", "BAGtzWoAJVswLTeJXGypT03DvEhQpJnJKSdr5dSb6e8H_9MBgpMxcjF6H82u9nEY-SuYr8LDkNyyrFhmeyaDeexwNiyKllsLOkhOqaXqFr_NjSVPty8aBDu_H_1sA0dNbumqYiZvN4YZLynhUTs2GnztSEZy-Vs8hwgPC1TAIERANZOpiYI7Dq2eSoSklujrbuA8YBCanS9eSxYLEePxd5PyGFEbbgdWUENvhyizUlJy8RoGa-ulPj2EAN69-3O6kmsRchW7zIZUTzZBNDqxeiOfopVrMQ20_qHYXiw2wO4cZZpGHHt3gsNIomSVhkFcuCeTJLh5O7dOxnRKrHEMdpLSeFCOnAAAAAF_3lp7AA")
    IS_PREMIUM = True
    MODES = ["video-video", "video-audio", "video-subtitle", "extract-streams"]
