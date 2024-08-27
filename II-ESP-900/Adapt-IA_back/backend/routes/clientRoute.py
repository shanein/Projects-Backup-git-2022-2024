from fastapi import APIRouter, Depends, HTTPException, Request, BackgroundTasks
from typing import List
from datetime import datetime as date

from controllers.videoController import get_videos
from utils.encryption import aes_encrypt

# from schemas.videoSchema import VideoResponse
from schemas.clientSchema import ClientConfig
from controllers.mailController import EmailSchema, simple_send
from database.database import get_db
from sqlalchemy.orm import Session
from controllers.clientController import get_client_config
from fastapi.responses import FileResponse
from zipfile import ZipFile
import os

router = APIRouter(tags=["Client"])
# from cryptography.fernet import Fernet


@router.get("/client/{terminal_id}")
def read_client_config(
    request: Request,
    terminal_id: str,
    secret_key: str,
    version: str = None,
    db: Session = Depends(get_db),
):
    client_ip = request.client.host
    client_config = get_client_config(
        terminal_id=terminal_id,
        secret_key=secret_key,
        version=version,
        ip=client_ip,
        db=db,
    )
    if isinstance(client_config, HTTPException):
        raise client_config
    return client_config


def remove_file(path: str):
    os.remove(path)
    print(f"Supprimé {path}")


@router.get("/download/{terminal_id}/{secret_key}")
async def download_config_and_installer(
    background_tasks: BackgroundTasks, terminal_id: str, secret_key: str
):
    base_path = "ressources_terminal"
    config_filename = os.path.join(base_path, "config.txt")
    installer_filename = os.path.join(base_path, "Setup.msi")
    zip_filename = os.path.join(base_path, "config_and_installer.zip")
    os.makedirs(base_path, exist_ok=True)
    config_content = f"Terminal ID: {terminal_id}\nSecret Key: {secret_key}"
    encrypted_content = aes_encrypt(config_content)

    with open(config_filename, "wb") as file:
        file.write(encrypted_content)
    with ZipFile(zip_filename, "w") as zipf:
        zipf.write(config_filename, os.path.basename(config_filename))
        zipf.write(installer_filename, os.path.basename(installer_filename))
    os.remove(config_filename)
    response = FileResponse(
        path=zip_filename,
        filename="config_and_installer.zip",
        media_type="application/zip",
    )
    background_tasks.add_task(remove_file, zip_filename)
    return response
