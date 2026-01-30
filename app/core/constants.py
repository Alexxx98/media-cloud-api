import os

from pathlib import Path

from dotenv import load_dotenv


load_dotenv()

STORAGE_PATH = Path(os.getenv('STORAGE_PATH'))

MIME_TYPES = {
  "html": "text/html",
  "htm": "text/html",
  "js": "application/javascript",
  "mjs": "application/javascript",
  "css": "text/css",
  "json": "application/json",
  "map": "application/json",

  "xml": "application/xml",
  "txt": "text/plain",
  "csv": "text/csv",

  "jpg": "image/jpeg",
  "jpeg": "image/jpeg",
  "png": "image/png",
  "gif": "image/gif",
  "webp": "image/webp",
  "avif": "image/avif",
  "bmp": "image/bmp",
  "tiff": "image/tiff",
  "tif": "image/tiff",
  "svg": "image/svg+xml",
  "ico": "image/x-icon",
  "psd": "image/vnd.adobe.photoshop",
  "ai": "application/postscript",

  "mp4": "video/mp4",
  "m4v": "video/mp4",
  "mov": "video/quicktime",
  "mkv": "video/x-matroska",
  "webm": "video/webm",
  "avi": "video/x-msvideo",
  "wmv": "video/x-ms-wmv",
  "flv": "video/x-flv",
  "mpeg": "video/mpeg",
  "mpg": "video/mpeg",
  "3gp": "video/3gpp",

  "mp3": "audio/mpeg",
  "wav": "audio/wav",
  "flac": "audio/flac",
  "aac": "audio/aac",
  "m4a": "audio/mp4",
  "ogg": "audio/ogg",
  "opus": "audio/opus",
  "aiff": "audio/aiff",
  "aif": "audio/aiff",
  "mid": "audio/midi",
  "midi": "audio/midi",
  "wma": "audio/x-ms-wma",

  "zip": "application/zip",
  "rar": "application/vnd.rar",
  "7z": "application/x-7z-compressed",
  "tar": "application/x-tar",
  "gz": "application/gzip",
  "bz2": "application/x-bzip2",

  "pdf": "application/pdf",
  "doc": "application/msword",
  "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
  "xls": "application/vnd.ms-excel",
  "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
  "ppt": "application/vnd.ms-powerpoint",
  "pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",

  "woff": "font/woff",
  "woff2": "font/woff2",
  "ttf": "font/ttf",
  "otf": "font/otf",

  "exe": "application/vnd.microsoft.portable-executable",
  "dmg": "application/x-apple-diskimage",
  "iso": "application/x-iso9660-image",

  "bin": "application/octet-stream"
}
