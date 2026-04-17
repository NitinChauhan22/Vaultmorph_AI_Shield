@echo off
echo ========================================
echo VaultMorph Checksum Verification
echo ========================================
echo.

set "EXPECTED_HASH=E874B315114B6DD0CD6501BC6DCF2776245D359EE1707F793E5E2E137279B2C6"
set "FILE_NAME=VaultMorphAIShield_Setup_v1.0.0.exe"

if not exist "%FILE_NAME%" (
    echo ERROR: File not found: %FILE_NAME%
    echo Please ensure the installer is in the same directory as this script.
    pause
    exit /b 1
)

echo Calculating SHA256 hash...
echo.

certutil -hashfile "%FILE_NAME%" SHA256 > temp_hash.txt
findstr /v ":" temp_hash.txt | findstr /v "^$" > actual_hash.txt

set /p ACTUAL_HASH=<actual_hash.txt
del temp_hash.txt
del actual_hash.txt

rem Remove spaces from hash
set "ACTUAL_HASH=%ACTUAL_HASH: =%"

echo Expected: %EXPECTED_HASH%
echo Actual:   %ACTUAL_HASH%
echo.

if /i "%ACTUAL_HASH%"=="%EXPECTED_HASH%" (
    echo [32m??? SUCCESS: Checksums match! File is authentic.[0m
    echo.
) else (
    echo [31m??? WARNING: Checksums do NOT match![0m
    echo [31mDo not install this file - it may have been tampered with.[0m
    echo.
)

pause
