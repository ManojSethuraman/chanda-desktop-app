# Build Script for Chanda Desktop Standalone Executable

Write-Host "==========================================================="
Write-Host "  Building Chanda Desktop Standalone Executable"
Write-Host "==========================================================="
Write-Host ""

# Step 1: Clean previous builds
Write-Host "[1/4] Cleaning previous builds..."
if (Test-Path "dist") {
    Remove-Item -Recurse -Force "dist"
    Write-Host "  - Removed dist folder"
}
if (Test-Path "build") {
    Remove-Item -Recurse -Force "build"
    Write-Host "  - Removed build folder"
}
Write-Host ""

# Step 2: Verify Chanda data directory
Write-Host "[2/4] Verifying Chanda data directory..."
$chandaDataDir = "C:\Chandojnana\chanda\chanda\data"
if (Test-Path $chandaDataDir) {
    $meterFiles = (Get-ChildItem $chandaDataDir -Filter "*.json").Count
    Write-Host "  - Found Chanda data directory with $meterFiles files"
}
else {
    Write-Host "  ERROR: Chanda data directory not found at $chandaDataDir"
    Write-Host "  Please update the path in chanda_desktop.spec"
    exit 1
}
Write-Host ""

# Step 3: Build executable with PyInstaller
Write-Host "[3/4] Building executable - this may take 2-3 minutes..."
python -m PyInstaller chanda_desktop.spec --clean

if ($LASTEXITCODE -eq 0) {
    Write-Host "  - Build completed successfully"
}
else {
    Write-Host "  ERROR: Build failed with error code $LASTEXITCODE"
    exit $LASTEXITCODE
}
Write-Host ""

# Step 4: Verify output
Write-Host "[4/4] Verifying output..."
if (Test-Path "dist\ChandaDesktop.exe") {
    $size = (Get-Item "dist\ChandaDesktop.exe").Length / 1MB
    Write-Host "  - Executable created: dist\ChandaDesktop.exe"
    Write-Host "  - Size: $([math]::Round($size, 2)) MB"
    Write-Host ""
    Write-Host "==========================================================="
    Write-Host "  BUILD SUCCESSFUL!"
    Write-Host "==========================================================="
    Write-Host ""
    Write-Host "The standalone executable is ready at:"
    Write-Host "  $(Resolve-Path 'dist\ChandaDesktop.exe')"
    Write-Host ""
    Write-Host "Users can now run ChandaDesktop.exe without:"
    Write-Host "  - Python installation"
    Write-Host "  - pip install commands"
    Write-Host "  - Chanda library setup"
    Write-Host "  - Any technical setup"
    Write-Host ""
    Write-Host "To distribute:"
    Write-Host "  1. Copy dist\ChandaDesktop.exe to any Windows computer"
    Write-Host "  2. Double-click to run"
    Write-Host "  3. That's it!"
    Write-Host ""
}
else {
    Write-Host "  ERROR: Executable not found"
    Write-Host "  Check the build output above for errors"
    exit 1
}
