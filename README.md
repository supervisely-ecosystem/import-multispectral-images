<div align="center" markdown>
<img src="https://github-production-user-asset-6210df.s3.amazonaws.com/118521851/286251873-effe616d-6250-4da6-ba8b-41ced5f701ee.png"/>

# Import multispectral images as channels or as separate images

<p align="center">
  <a href="#Overview">Overview</a> •
  <a href="#Preparation">Preparation</a> •
  <a href="#How-To-Run">How To Run</a> •
  <a href="#Results">Results</a>
</p>

[![](https://img.shields.io/badge/supervisely-ecosystem-brightgreen)](https://ecosystem.supervise.ly/apps/supervisely-ecosystem/import-multispectral-images)
[![](https://img.shields.io/badge/slack-chat-green.svg?logo=slack)](https://supervise.ly/slack)
![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/supervisely-ecosystem/import-multispectral-images)
[![views](https://app.supervise.ly/img/badges/views/supervisely-ecosystem/import-multispectral-images.png)](https://supervise.ly)
[![runs](https://app.supervise.ly/img/badges/runs/supervisely-ecosystem/import-multispectral-images.png)](https://supervise.ly)

</div>

## Overview

This application allows you to import multispectral images as channels or as separate images without annotations. As a result you will get a project with images, where images a grouped by the group with name of the corresponding folder, which contains images.<br>

## Preparation

First, you need to prepare an archive with the correct structure. Each image group should be placed in a separate folder. In that folder, you need to create a folder `images` if you want to upload images without splitting to the channels or folder `split` which will contain images, that should be split.

You can download an example of data for import [here](https://github.com/supervisely-ecosystem/import-multispectral-images/files/13487269/demo_data.zip).<br>

Here's an example of the structure of the archive:

```text
📦 archive
 ┣ 📂 group_name_1
 ┃ ┣ 📂 split
 ┃ ┃ ┗ 🏞️ demo1.png
 ┣ 📂 group_name_2
 ┃ ┣ 📂 images
 ┃ ┃ ┣ 🏞️ demo4-rgb.png
 ┃ ┃ ┗ 🏞️ demo4-thermal.png
 ┃ ┣ 📂 split
 ┃ ┃ ┗ 🏞️ demo4-thermal copy.png
 ┣ 📂 group_name_3
 ┃ ┣ 📂 images
 ┃ ┃ ┣ 🏞️ demo8-mri1.png
 ┃ ┃ ┣ 🏞️ demo8-mri2.png
 ┃ ┃ ┗ 🏞️ demo8-rgb.png
```

In this example, we have 3 groups with images. In the first group, we have one image, which should be split. In the second group, we have one image, which should be splitted and two images, which should be uploaded as is. In the third group, we have three images, which should be uploaded as is.<br>

## How To Run

### Uploading an archive with images

**Step 1:** Run the app<br>

<img src="https://github-production-user-asset-6210df.s3.amazonaws.com/118521851/286258291-93e42bee-6709-40a6-946c-0809fc398c18.png"/><br>

**Step 2:** Drag and drop the archive or select it in Team Files<br>

<img src="https://github-production-user-asset-6210df.s3.amazonaws.com/118521851/286258301-008d6b5e-c1cb-408f-aa26-2b62c80508f6.png"/><br>

**Step 3:** Press the `Run` button<br>

## Results

After the app is finished, you will get a project with images, where images a grouped by the group with the name of the corresponding folder, which contains images.<br>
The images within the group will have synchronized zooming, panning and labeling.<br>

<img src="https://github-production-user-asset-6210df.s3.amazonaws.com/118521851/286261123-a07db05b-a5fe-4f9b-891e-8db99179b1b9.gif"/>