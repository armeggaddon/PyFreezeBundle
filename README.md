<div align="center">

# ⚡ PyFreezeBundle

### *Ship your Python application anywhere — no Python required.*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![cx_Freeze](https://img.shields.io/badge/cx__Freeze-powered-orange)](https://cx-freeze.readthedocs.io/)
[![FastAPI](https://img.shields.io/badge/FastAPI-demo-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-lightgrey)]()

> **Freeze. Bundle. Execute.** — Package your entire Python environment, dependencies, and runtime into a single portable executable that runs on any machine.

</div>

---

## 📖 Table of Contents

- [What is PyFreezeBundle?](#-what-is-pyfreezebundle)
- [Why Bundle Python?](#-why-bundle-python)
- [How It Works](#-how-it-works)
- [Project Structure](#-project-structure)
- [Deep Dive: bundle.py](#-deep-dive-bundlepy)
- [The Demo Application](#-the-demo-application)
- [Getting Started](#-getting-started)
- [Running the Bundle](#-running-the-bundle)
- [Output Artifacts](#-output-artifacts)
- [Platform Support](#-platform-support)
- [Best Practices](#-best-practices)
- [Advantages](#-advantages)
- [Use Cases](#-use-cases)
- [Citations & References](#-citations--references)
- [License](#-license)

---

## 🚀 What is PyFreezeBundle?

**PyFreezeBundle** is a reference implementation that demonstrates how to package a complete Python workflow — including all third-party libraries, the Python interpreter, and non-Python assets — into a **single self-contained executable** using [cx_Freeze](https://cx-freeze.readthedocs.io/).

The output is:
- A **`.exe`** file on **Windows** — double-click and it runs.
- A **binary executable** on **Linux/macOS** — `./run` and it runs.

No `pip install`. No `conda activate`. No version conflicts. No Python on the target machine.

---

## 💡 Why Bundle Python?

| Problem Without Bundling | Solution with PyFreezeBundle |
|---|---|
| Target machine needs Python installed | ✅ Interpreter is embedded in the bundle |
| Dependency conflicts between projects | ✅ Isolated, frozen environment |
| Complex deployment scripts | ✅ Single executable artifact |
| Version mismatches across teams | ✅ Exact environment is preserved |
| Distributing to non-technical users | ✅ Double-click to run |
| CI/CD artifact portability | ✅ Ship one binary, run anywhere |

---

## ⚙️ How It Works

```
Your Python Code  ──┐
requirements.txt  ──┼──► [ bundle.py + cx_Freeze ] ──► Standalone Executable
Non-Python Assets ──┘
(test files, configs,
 data files, etc.)
```

cx_Freeze introspects your entry point (`main.py`), traces all imports, resolves transitive dependencies, embeds the Python interpreter, and packs everything into an output directory that behaves as a self-contained application.

---

## 📁 Project Structure

```
PyFreezeBundle/
│
├── bundle.py          ← 🔧 The bundler configuration (the heart of this project)
├── main.py            ← 🚀 Application entry point (Uvicorn/FastAPI launcher)
├── settings.py        ← ⚙️  FastAPI app definition and middleware configuration
├── starter.py         ← 🔌 API router with demo endpoints
├── requirements.txt   ← 📦 Python packages to include in the bundle
└── test               ← 📄 Non-Python asset included via file_list
```

---

## 🔬 Deep Dive: `bundle.py`

This is the **only file you need to understand** to bundle your own workflow. Here is a line-by-line breakdown:

```python
import os
from cx_Freeze import setup, Executable
```
Standard imports — `os` for path resolution, `cx_Freeze` for the bundling engine.

---

### 1. Reading Dependencies from `requirements.txt`

```python
def read_requirements(file_name):
    with open(file_name) as f:
        return [line.strip() for line in f]

file_name = project_path + '/' + 'requirements.txt'
i_packages = read_requirements(file_name)
```

Instead of hardcoding package names, `bundle.py` dynamically reads `requirements.txt`. This means your bundle configuration **automatically stays in sync** with your dependency list — add a package to `requirements.txt`, and it gets bundled automatically.

---

### 2. Non-Python Assets via `file_list`

```python
file_list = []
file_list.append(f"{project_path}/test")
includefiles = file_list
```

cx_Freeze only auto-resolves `.py` files and Python packages. Any other file — configuration files, test fixtures, data files, JSON/YAML configs, certificates — must be **explicitly declared** here. This array of paths gets passed as `include_files` so they land inside the build output directory.

---

### 3. Exclude Packages

```python
e_packages = ['setuptools', 'pip', 'cx_Freeze']
```

These packages are used **only during the build process** and should never be embedded in the final executable. Excluding them:
- Reduces the output size significantly.
- Avoids shipping build tooling inside a production artifact.
- Prevents accidental execution of install/uninstall logic inside the bundle.

---

### 4. Build Path Configuration

```python
application_name = 'PyFreezeBundle'
build_path = project_path + '/' + application_name
```

The output directory is named after the application and placed alongside the source. You can override this to any absolute path (e.g., a `dist/` folder).

---

### 5. The Executable Declaration

```python
exe = [Executable("./main.py")]
```

`main.py` is the **entry point** — the file cx_Freeze uses as `__main__`. On Windows this becomes a `.exe`. You can pass additional arguments to `Executable()` such as:
- `target_name` — rename the output binary
- `icon` — embed a `.ico` file into the Windows executable
- `base="Win32GUI"` — suppress the console window for GUI apps

---

### 6. The `options` Dictionary

```python
options = {
    "build_exe": {
        'build_exe':      build_path,    # Output directory
        'packages':       i_packages,    # Packages to include
        'excludes':       e_packages,    # Packages to strip out
        'include_files':  includefiles   # Non-.py assets
    }
}
```

This single dictionary drives the entire bundle behavior. The key `"build_exe"` maps to the `build_exe` command target of cx_Freeze's `setup()`.

---

### 7. The `setup()` Call

```python
setup(
    name        = "PyFreezeBundle",
    version     = "1.0.0",
    description = "PyFreeze bundle demo",
    options     = options,
    executables = exe,
)
```

This mirrors Python's standard `setuptools.setup()` API — familiar to any Python developer. cx_Freeze extends it with the `executables` parameter and the `build_exe` build command.

---

## 🌐 The Demo Application

PyFreezeBundle ships with a fully functional **FastAPI REST API** as its demo payload — proving that even a networked web service can be frozen and distributed as a standalone binary.

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/healthCheck` | Returns `"Success"` if the service is up |
| `GET` | `/sumTwoNumbers?number1=5&number2=3` | Returns the sum of two integers |
| `GET` | `/docs` | Interactive Swagger UI (auto-generated) |
| `GET` | `/redoc` | ReDoc API documentation |

### Architecture

```
Executable (main.py)
    └── Uvicorn ASGI Server  (port 8099)
            └── FastAPI Application  (settings.py)
                    └── APIRouter  (starter.py)
                            ├── GET /healthCheck
                            └── GET /sumTwoNumbers
```

Once the bundle is executed, open your browser at `http://localhost:8099/docs` to explore the live API — with **zero Python installation** on the host.

---

## 🛠️ Getting Started

### Prerequisites

```bash
pip install cx_Freeze fastapi uvicorn
```

Or install from the requirements file:

```bash
pip install -r requirements.txt
```

> **Note:** cx_Freeze only needs to be installed on the **build machine**. The target machine requires nothing.

---

## ▶️ Running the Bundle

### Step 1 — Build the executable

```bash
python bundle.py build_exe
```

This triggers cx_Freeze to:
1. Trace all imports from `main.py`
2. Collect all declared packages from `requirements.txt`
3. Copy non-Python assets from `file_list`
4. Strip out excluded packages
5. Write everything into the `PyFreezeBundle/` output directory

### Step 2 — Run the executable

**Windows:**
```
PyFreezeBundle\main.exe
```
or simply double-click `main.exe` in File Explorer.

**Linux:**
```bash
./PyFreezeBundle/main
```

The FastAPI service starts immediately on port `8099`. Open `http://localhost:8099/docs` in your browser.

---

## 📦 Output Artifacts

After the build, the output directory contains everything needed to run:

```
PyFreezeBundle/
├── main.exe              ← Your standalone executable (Windows)
├── python3xx.dll         ← Embedded Python interpreter DLL
├── lib/                  ← All bundled Python packages
│   ├── fastapi/
│   ├── uvicorn/
│   ├── starlette/
│   └── ...
├── test                  ← Your non-Python asset (copied verbatim)
└── ...
```

The entire `PyFreezeBundle/` directory is your **distributable artifact**. Zip it, ship it, deploy it.

---

## 🖥️ Platform Support

| Platform | Output | How to Run |
|---|---|---|
| **Windows** | `main.exe` | Double-click or `.\main.exe` |
| **Linux** | `main` (ELF binary) | `./main` |
| **macOS** | `main` (Mach-O binary) | `./main` |

> Build on the **target platform**. A Windows build produces a Windows executable; a Linux build produces a Linux binary. Cross-compilation is not supported by cx_Freeze — use CI/CD runners (e.g., GitHub Actions) with platform-specific jobs for multi-platform releases.

---

## ✅ Best Practices

### 1. Always Pin Your Requirements
```
fastapi==0.111.0
uvicorn==0.29.0
```
Unpinned versions can cause non-deterministic bundles across different build environments.

### 2. Minimize Included Packages
Only include packages that are **actually used at runtime**. Unused packages bloat the executable and increase startup time.

### 3. Exclude Build-Only Tools
Always exclude `setuptools`, `pip`, `cx_Freeze`, `wheel`, and other build-time-only packages using the `excludes` list.

### 4. Use Absolute Paths in `file_list`
```python
project_path = os.path.dirname(os.path.realpath(__file__))
file_list.append(f"{project_path}/test")
```
Relative paths can break depending on the working directory at build time. Always resolve paths relative to `__file__`.

### 5. Test the Bundle in a Clean Environment
After building, copy the output directory to a machine **without Python installed** and verify it runs correctly. This is the only true test of portability.

### 6. Version-Control `bundle.py`, Not the Build Output
Add your `PyFreezeBundle/` build output to `.gitignore`. Only `bundle.py` and `requirements.txt` need to be tracked.

```gitignore
# .gitignore
PyFreezeBundle/
build/
dist/
__pycache__/
*.pyc
```

### 7. Use CI/CD for Reproducible Builds
Automate the build step in GitHub Actions to produce fresh, deterministic executables on every release tag.

---

## 🏆 Advantages

- **Zero Runtime Dependency** — The Python interpreter itself is embedded. Target machines need nothing pre-installed.
- **Consistent Environment** — Eliminates "works on my machine" problems caused by different Python versions or package states.
- **Single Artifact Distribution** — One directory (or zip) is your complete deployable unit — ideal for enterprise environments with strict installation policies.
- **Cross-Functional Sharing** — Share a working API or tool with non-developers who cannot be expected to manage virtual environments.
- **Immutable Deployments** — The frozen environment cannot be accidentally modified by external `pip install` commands.
- **Startup Determinism** — No package resolution at startup; all imports resolve immediately from the frozen lib directory.

---

## 🎯 Use Cases

| Scenario | Benefit |
|---|---|
| **Internal enterprise tools** | Distribute to colleagues without IT setup overhead |
| **Edge / IoT deployments** | Ship a self-contained agent to resource-constrained nodes |
| **Client deliverables** | Hand off a working product without source code exposure |
| **Offline environments** | Run Python-based services in air-gapped networks |
| **CI/CD build artifacts** | Produce a portable binary as a release asset on GitHub |
| **Cross-team API mocking** | Share a runnable API server stub without environment setup |
| **Kiosk / point-of-sale systems** | Lock down runtime into a single executable |

---

## 📚 Citations & References

| Resource | Link |
|---|---|
| cx_Freeze — Official Documentation | https://cx-freeze.readthedocs.io/ |
| cx_Freeze — GitHub Repository | https://github.com/marcelotduarte/cx_Freeze |
| FastAPI — Official Documentation | https://fastapi.tiangolo.com/ |
| Uvicorn — ASGI Server | https://www.uvicorn.org/ |
| Python Packaging User Guide | https://packaging.python.org/ |
| GitHub Actions — CI/CD | https://docs.github.com/en/actions |

> cx_Freeze is actively maintained by [@marcelotduarte](https://github.com/marcelotduarte) and the open-source community. See their [changelog](https://cx-freeze.readthedocs.io/en/latest/changelog.html) for version-specific behavior.

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome.

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -m 'Add my feature'`
4. Push to the branch: `git push origin feature/my-feature`
5. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License** — see below for details.

```
MIT License

Copyright (c) 2026 PyFreezeBundle Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
```

---

<div align="center">

**Made with ❄️ and Python**

*If this project helped you, give it a ⭐ on GitHub!*

</div>
