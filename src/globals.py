import os
import supervisely as sly
from dotenv import load_dotenv

if sly.is_development():
    # * For convinient development, has no effect in the production.
    load_dotenv("local.env")
    load_dotenv(os.path.expanduser("~/supervisely.env"))

ABSOLUTE_PATH = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(ABSOLUTE_PATH)
sly.logger.debug(f"Absolute path: {ABSOLUTE_PATH}, parent dir: {PARENT_DIR}")

SPLIT_TO_CHANNELS_DIR_NAME = "split"
UPLOAD_AS_IMAGES_DIR_NAME = "images"

api: sly.Api = sly.Api.from_env()

TEMP_DIR = os.path.join(PARENT_DIR, "temp")

# * Directory, where downloaded as archives V7 datasets will be stored.
ARCHIVE_DIR = os.path.join(TEMP_DIR, "archives")

# * Directory, where unpacked V7 datasets will be stored.
UNPACKED_DIR = os.path.join(TEMP_DIR, "unpacked")
sly.fs.mkdir(ARCHIVE_DIR, remove_content_if_exists=True)
sly.fs.mkdir(UNPACKED_DIR, remove_content_if_exists=True)
sly.logger.debug(
    f"App starting... Archive dir: {ARCHIVE_DIR}, unpacked dir: {UNPACKED_DIR}"
)

TEAM_ID = sly.io.env.team_id()
WORKSPACE_ID = sly.io.env.workspace_id()

sly.logger.debug(f"App starting... Team ID: {TEAM_ID}, Workspace ID: {WORKSPACE_ID}")

SLY_FILE = sly.io.env.file(raise_not_found=False)
SLY_FOLDER = sly.io.env.folder(raise_not_found=False)
sly.logger.debug(f"App starting... File: {SLY_FILE}, Folder: {SLY_FOLDER}")

if SLY_FILE:
    sly.logger.info(
        "Path to file is provided, the application will run in file mode. "
        f"File path: {SLY_FILE}"
    )
elif SLY_FOLDER:
    sly.logger.info(
        "Path to folder is provided, the application will run in folder mode. "
        f"Folder path: {SLY_FOLDER}"
    )
