import os
from typing import List
from collections import defaultdict, namedtuple
import supervisely as sly
import numpy as np
import nrrd
import tifffile
import cv2

import globals as g


IMAGES_DIR = "images"
RELEASES_DIR = "releases"

ImageGroup = namedtuple("ImageGroup", ["split", "upload"])


@sly.handle_exceptions
def main():
    sly.logger.debug("Starting main function...")
    data_path = download_data()

    project = g.api.project.create(
        g.WORKSPACE_ID, "Multispectral images", change_name_if_conflict=True
    )
    g.api.project.set_multispectral_settings(project.id)
    dataset = g.api.dataset.create(project.id, "ds0")

    directories = find_image_directories(data_path)

    uploaded = 0

    for group_path, image_group in directories.items():
        sly.logger.info(f"Found files in {group_path}.")
        # directory_name = os.path.basename(directory_path)
        # dataset = g.api.dataset.create(project.id, directory_name)
        # for file_group in file_groups:
        images = []
        channels = []

        images_to_split, images_to_upload = image_group.split, image_group.upload
        # if len(images_to_split) > 0:
        #     file_base_name = os.path.basename(images_to_split[0])
        # elif len(images_to_upload) > 0:
        #     file_base_name = os.path.basename(images_to_upload[0])
        # else:
        #     continue
        group_name = os.path.basename(group_path)
        for image_to_upload in images_to_upload:
            images.append(os.path.join(group_path, image_to_upload))
        for image_to_split in images_to_split:
            channels.extend(
                get_image_channels(os.path.join(group_path, image_to_split))
            )
        image_infos = g.api.image.upload_multispectral(
            dataset.id, group_name, channels, images
        )
        uploaded += len(image_infos)

        sly.logger.info(f"Uploaded {len(image_infos)} images to group {group_name}.")

    if uploaded == 0:
        sly.logger.warning("No images were uploaded, please check your data.")
    else:
        sly.logger.info(f"Uploaded {uploaded} images.")


def get_image_channels(file_path: str) -> List[np.ndarray]:
    file_ext = sly.fs.get_file_ext(file_path).lower()
    sly.logger.debug(f"Working with file {file_path} with extension {file_ext}.")

    if file_ext == ".nrrd":
        sly.logger.debug(f"Found nrrd file: {file_path}.")
        image, _ = nrrd.read(file_path)
    elif file_ext == ".tif":
        sly.logger.debug(f"Found tiff file: {file_path}.")
        image = tifffile.imread(file_path)
    elif sly.image.is_valid_ext(file_ext):
        sly.logger.debug(f"Found image file: {file_path}.")
        image = cv2.imread(file_path)
    else:
        sly.logger.warning(f"File {file_path} has unsupported extension.")
        return

    return [image[:, :, i] for i in range(image.shape[2])]


def download_data() -> str:
    sly.logger.info("Starting download data...")
    if g.SLY_FILE:
        sly.logger.info(f"Was provided a path to file: {g.SLY_FILE}")
        data_path = _download_archive(g.SLY_FILE)

    elif g.SLY_FOLDER:
        sly.logger.info(f"Was provided a path to folder: {g.SLY_FOLDER}")
        files_list = g.api.file.list(g.TEAM_ID, g.SLY_FOLDER)
        if len(files_list) == 1:
            sly.logger.debug(
                f"Provided folder contains only one file: {files_list[0].name}. "
                "Will handle it as an archive."
            )
            data_path = _download_archive(files_list[0].path)
        else:
            sly.logger.debug(
                f"Provided folder contains more than one file: {files_list}. "
                "Will handle it as a folder with unpacked data."
            )

            data_path = _download_folder(g.SLY_FOLDER)

    sly.logger.debug(f"Data downloaded and prepared in {data_path}.")

    return data_path


def find_image_directories(path: str):
    group_map = defaultdict(ImageGroup)
    for checked_directory in sly.fs.dirs_filter(path, check_function):
        sly.logger.debug(
            f"Found directory {checked_directory} meeting the requirements."
        )

        split_images = []
        upload_images = []

        split_dir = os.path.join(checked_directory, g.SPLIT_TO_CHANNELS_DIR_NAME)

        images_dir = os.path.join(checked_directory, g.UPLOAD_AS_IMAGES_DIR_NAME)

        if os.path.isdir(split_dir):
            split_images = sly.fs.list_files(split_dir)
        if os.path.isdir(images_dir):
            upload_images = sly.fs.list_files(images_dir)

        group_map[checked_directory] = ImageGroup(split_images, upload_images)

    return group_map


def check_function(path: str) -> bool:
    split_dir = os.path.join(path, g.SPLIT_TO_CHANNELS_DIR_NAME)
    images_dir = os.path.join(path, g.UPLOAD_AS_IMAGES_DIR_NAME)

    if os.path.isdir(split_dir) or os.path.isdir(images_dir):
        return True
    return False


def _download_folder(remote_path: str) -> str:
    sly.logger.info(f"Starting download folder from {remote_path}...")
    folder_name = sly.fs.get_file_name(remote_path)
    save_path = os.path.join(g.UNPACKED_DIR, folder_name)
    sly.logger.debug(f"Will download folder to {save_path}.")
    g.api.file.download_directory(g.TEAM_ID, remote_path, save_path)
    sly.logger.debug(f"Folder downloaded to {save_path}.")
    return save_path


def _download_archive(remote_path: str) -> str:
    sly.logger.info(f"Starting download archive from {remote_path}...")
    archive_name = sly.fs.get_file_name_with_ext(remote_path)
    save_path = os.path.join(g.ARCHIVE_DIR, archive_name)
    sly.logger.debug(f"Will download archive to {save_path}.")
    g.api.file.download(g.TEAM_ID, remote_path, save_path)
    sly.logger.debug(f"Archive downloaded to {save_path}.")

    file_name = sly.fs.get_file_name(remote_path)
    unpack_path = os.path.join(g.UNPACKED_DIR, file_name)
    sly.logger.debug(f"Will unpack archive to {unpack_path}.")
    try:
        sly.fs.unpack_archive(save_path, unpack_path)
    except Exception as e:
        raise RuntimeError(
            f"Can't unpack archive from {remote_path}. "
            f"Provided file must be a valid archive. {e}"
        )
    sly.logger.debug(f"Archive unpacked to {unpack_path}.")
    return unpack_path


if __name__ == "__main__":
    main()
