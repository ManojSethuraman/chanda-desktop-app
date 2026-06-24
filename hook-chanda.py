# PyInstaller hook for Chanda library
# This ensures all Chanda modules and data are properly included

from PyInstaller.utils.hooks import collect_all, collect_data_files, collect_submodules

# Collect all Chanda submodules
hiddenimports = collect_submodules('chanda')

# Collect Chanda data files
datas = collect_data_files('chanda', include_py_files=True)

# Collect all dependencies
tmp_ret = collect_all('chanda')
datas += tmp_ret[0]
binaries = tmp_ret[1]
hiddenimports += tmp_ret[2]
