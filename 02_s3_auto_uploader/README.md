# Automatic S3 Uploader

## Purpose
Upload local files to an existing private S3 bucket using Python,
Boto3 and Watchdog.

## Features
- Watches incoming/ and its subfolders.
- Scans existing files at startup.
- Saves upload history to skip unchanged files after restarting.
- Prioritizes queued uploads before retrying failed files.
- Includes deletion handling for previously managed objects.
- Ignores .part and .tmp paths during incomplete copies.

## Run
python -m pip install -r requirements.txt
python uploader.py --bucket YOUR_BUCKET_NAME

Default profile: cloud-labs
Default region: eu-central-1

## Verified
New-file uploads, nested uploads, startup scanning,
restart deduplication and uploading modified files.

## Remaining validation
Retry priority during failures, deletion handling,
and Windows Task Scheduler execution.

## Notes
AWS credentials must remain valid.
The computer must be awake and connected for uploads.
Local removal can delete the corresponding managed S3 object.
Upload history and local incoming files are excluded from Git.