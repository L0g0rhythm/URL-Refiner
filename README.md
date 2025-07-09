# url-refiner

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

A robust and elegant tool to process, modify, and deduplicate URL lists. Designed for security professionals, data analysts, and developers who need to manipulate large volumes of URL parameters efficiently.

---

## 📚 Index

- [✨ Features](#-features)
- [🛠️ Technology Stack](#️-technology-stack)
- [🚀 Installation](#-installation)
- [🖥️ Usage](#-usage)
  - [🔧 CLI (Command-Line Interface)](#-cli-command-line-interface)
  - [🖱️ GUI (Graphical User Interface)](#️-gui-graphical-user-interface)
- [✅ Tests](#-tests)
- [📄 License](#-license)
- [📬 Contact](#-contact)

---

## ✨ Features

- **Parameter Manipulation**: Replace or append values to query parameters in thousands of URLs.
- **Smart Deduplication**: Removes duplicate URLs based on domain, path (optional), and parameter names.
- **Flexible I/O**: Reads from files or stdin—ideal for script pipelines.
- **Organized Output**: Automatically saves processed lists to the `output/` directory with timestamp.
- **Enhanced UX**: Rich progress bar and colorful, informative feedback.
- **Optional GUI**: Simple and intuitive web-based interface.

---

## 🛠️ Technology Stack

| Layer         | Technologies             |
| ------------- | ------------------------ |
| Backend & CLI | Python 3, Typer, Rich    |
| GUI           | Eel, HTML5, Tailwind CSS |
| Testing       | Pytest                   |

---

## 🚀 Installation

### Method 1: End Users (via `pipx`) — **Recommended**

1. Install `pipx` (if not already installed):

   ```sh
   pip install pipx
   ```

2. Ensure `pipx` is in your system's PATH:

   ```sh
   pipx ensurepath
   ```

3. Install directly from GitHub:
   - **CLI + GUI**:

     ```sh
     pipx install "git+https://github.com/L0g0rhythm/url-refiner.git#egg=url-refiner[gui]"
     ```

   - **CLI only**:

     ```sh
     pipx install "git+https://github.com/L0g0rhythm/url-refiner.git"
     ```

After installation, the commands `url-refiner` and `url-refiner-gui` will be available globally.

---

### Method 2: Developers

1. Clone the repository:

   ```sh
   git clone https://github.com/L0g0rhythm/url-refiner.git
   cd url-refiner
   ```

2. Create and activate a virtual environment:
   - **Windows**:

     ```sh
     python -m venv .venv
     .\.venv\Scripts\activate
     ```

   - **macOS/Linux**:

     ```sh
     python3 -m venv .venv
     source .venv/bin/activate
     ```

3. Install with development and GUI dependencies:

   ```sh
   pip install -e ".[gui,dev]"
   ```

---

## 🖥️ Usage

### 🔧 CLI (Command-Line Interface)

Place your input files inside the `Inputs/` directory.

- **Read file and print to console**:

  ```sh
  url-refiner --input urls.txt
  ```

- **Save output to a timestamped file**:

  ```sh
  url-refiner --input urls.txt --output
  ```

- **Use stdin piping**:
  - **Windows**:

    ```sh
    type Inputs\urls.txt | url-refiner
    ```

  - **macOS/Linux**:

    ```sh
    cat Inputs/urls.txt | url-refiner
    ```

- **Advanced options**:
  - Append instead of replacing:

    ```sh
    url-refiner --input urls.txt --mode append
    ```

  - Use a custom value:

    ```sh
    url-refiner --input urls.txt --value "L0g0rhythm"
    ```

  - Exclude specific parameters:

    ```sh
    url-refiner --input urls.txt --exclude id --exclude token
    ```

  - Ignore URL path for strict deduplication:

    ```sh
    url-refiner --input urls.txt --ignore-path
    ```

---

### 🖱️ GUI (Graphical User Interface)

For an interactive experience:

1. Launch the GUI:

   ```sh
   url-refiner-gui
   ```

2. A browser window will open automatically.

3. Use the interface to:
   - Paste your list of URLs on the left.
   - Configure options like mode, value, exclusions.
   - Click **Process** to see results and stats.

---

## ✅ Tests

Run the full test suite from the root directory:

```sh
pytest
```

---

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for full details.

---

## 📬 Contact

**Victor Oliveira (L0g0rhythm)**
🔗 Website: [l0g0rhythm.com.br](https://l0g0rhythm.com.br)
