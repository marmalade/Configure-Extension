@echo off
if not exist "%S3E_DIR%\makefile_builder\extensions" (
echo S3E environment not found
) else (
if not exist .\start_configure.py (
echo Start me from the directory where I am exist
) else (
copy .\start_configure.py "%S3E_DIR%\makefile_builder\extensions"
)
)