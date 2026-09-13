# PySCF Installation Debugging Log

**Environment:** Windows 10, Python 3.14, qiskit conda environment

## Problem Summary
Unable to install pyscf in the qiskit conda environment. CMake cannot find BLAS libraries during build.

---

## Approaches Attempted

### Attempt 1: Direct pip install
```powershell
conda activate qiskit
pip install pyscf
```
**Result:** FAILED  
**Error:** CMake error - "Could NOT find BLAS (missing: BLAS_LIBRARIES)"  
**Details:** pyscf requires BLAS for compilation, but CMake cannot locate the library

---

### Attempt 2: Install BLAS/LAPACK via conda
```powershell
conda activate qiskit
conda install -c conda-forge openblas lapack libblas -y
```
**Result:** SUCCESS (libraries installed)  
**Output:** Installed libopenblas-0.3.33, lapack-3.11.0, openblas-0.3.33, scipy-1.18.0  
**Next action:** Retried pip install pyscf

---

### Attempt 3: Retry pip install after BLAS installation
```powershell
conda activate qiskit
pip install pyscf
```
**Result:** FAILED  
**Error:** Same BLAS not found error - CMake still cannot locate BLAS_LIBRARIES  
**Root cause:** Build environment isolation prevents CMake from accessing conda's BLAS libraries

---

### Attempt 4: conda install from conda-forge
```powershell
conda activate qiskit
conda install -c conda-forge pyscf -y
```
**Result:** FAILED  
**Error:** PackagesNotFoundInChannelsError - pyscf not available for Windows in conda-forge  
**Details:** Checked channels: conda-forge/win-64, main, r, msys2

---

### Attempt 5: pip install with environment variable + --no-build-isolation
```powershell
conda activate qiskit
$env:BLAS_LIBRARIES = "openblas"
pip install pyscf --no-build-isolation
```
**Result:** FAILED  
**Error:** Still cannot find BLAS (missing: BLAS_LIBRARIES)  
**Issue:** Environment variable alone insufficient for CMake to locate libraries

---

### Attempt 6: Install Intel MKL
```powershell
conda activate qiskit
conda install -c conda-forge mkl -y
```
**Result:** Already installed (no new packages)

---

### Attempt 7: Set CMAKE paths + pip install with --no-build-isolation
```powershell
conda activate qiskit
$env:CMAKE_LIBRARY_PATH = "$env:CONDA_PREFIX\Library\lib"
$env:CMAKE_INCLUDE_PATH = "$env:CONDA_PREFIX\Library\include"
pip install pyscf --no-build-isolation
```
**Result:** PARTIAL - Build appeared to progress further through libxc compilation  
**Outcome:** Large output log generated (~72KB) but final verification showed pyscf module not found
**Status:** Unknown if build completed or failed silently

---

### Attempt 8: Verify installation
```powershell
conda activate qiskit
python -c "import pyscf; print('pyscf successfully installed!')"
```
**Result:** FAILED  
**Error:** ModuleNotFoundError: No module named 'pyscf'

---

### Attempt 9: Check available versions
```powershell
pip index versions pyscf
```
**Result:** SUCCESS  
**Available versions:** 2.13.1 (latest) down to 1.4.0  
**Note:** All versions require source compilation for Windows

---

## Root Cause Analysis

**Primary Issue:** PySCF on Windows requires Fortran/C++ source compilation with proper BLAS/LAPACK linkage. The build system (CMake + MS Visual Studio BuildTools) cannot locate BLAS libraries even when installed via conda because:

1. Build environments in pip use isolation that prevents access to conda's libraries
2. CMake's BLAS detection on Windows is unreliable with conda-installed libraries
3. No pre-compiled Windows wheels available on PyPI (unlike Linux/macOS)

---

## Relevant System Information

- **OS:** Windows 10.0.26200
- **Compiler:** MSVC 19.44.35226.0 (Visual Studio 2022 BuildTools)
- **Python Version:** 3.14 (in qiskit env)
- **CMake:** Available in conda
- **BLAS Installed:** openblas 0.3.33, libopenblas 0.3.33, lapack 3.11.0
- **Build Tool:** Successfully compiles through libxc but fails on BLAS linking

---

## Recommendations for Alternative Models

1. **Option 1:** Check if pre-compiled wheels exist on other package indices (PyPI-compatible) or GitHub releases - FAILED
2. **Option 2:** Try MESON build system (more Windows-friendly than CMake): - FAILED
   ```powershell
   conda activate qiskit
   conda install -c conda-forge meson ninja -y
   pip install pyscf --no-build-isolation
   ```
3. **Option 3:** Use WSL2/Linux subsystem for proper pyscf compilation
4. **Option 4:** Check if `qiskit-nature` offers alternatives that don't require pyscf
5. **Option 5:** Examine pyscf's CMakeLists.txt to manually configure BLAS paths
6. **Option 6:** Contact qiskit community - this is a known Windows issue

