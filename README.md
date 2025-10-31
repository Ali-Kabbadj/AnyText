<p align="center">
  <img src="assets/logo.png" alt="AnyText Logo" width="200">
</p>

<h1 align="center">AnyText</h1>

<h3 align="center">Package your code repositories into a single, LLM-ready text file.</h3>

<p align="center">
  <a href="https://github.com/Ali-Kabbadj/AnyText/actions/workflows/release.yml">
    <img src="https://github.com/Ali-Kabbadj/AnyText/actions/workflows/release.yml/badge.svg" alt="Build Status">
  </a>
  <a href="https://github.com/Ali-Kabbadj/AnyText/releases/latest">
    <img src="https://img.shields.io/github/v/release/Ali-Kabbadj/AnyText" alt="Latest Release">
  </a>
  <a href="https://github.com/Ali-Kabbadj/AnyText/blob/main/LICENSE">
    <img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License">
  </a>
</p>

<p align="center">
  <img src="assets/img_demo.png" alt="AnyText Application Screenshot" width="800">
</p>

## Overview

AnyText is a powerful desktop utility designed to streamline the process of preparing source code for analysis by Large Language Models (LLMs). Instead of manually copying and pasting files, you can use this intuitive graphical interface to select, filter, and package an entire project's structure and content into a single, perfectly formatted text file, complete with accurate token counts.

This tool is essential for anyone doing AI related work, documentation, or analysis, saving you time and ensuring you get the most out of your LLM's context window.

## Key Features

- **Visual File Selection:** An interactive and collapsible file tree lets you visually select exactly which files and folders to include in the output.
- **Advanced Filtering:** Quickly include or exclude files based on their extension (e.g., `.py`, `.js`) or by common generic filenames (e.g., `Dockerfile`, `requirements.txt`).
- **Accurate Token Counting:** Uses the official `tiktoken` library to provide a highly accurate token estimate for OpenAI models (GPT-3.5, GPT-4), helping you manage context window limits.
- **Intelligent Output Generation:** Creates a clean, readable text file that starts with a formatted directory tree of the selected files, followed by the complete content of each file.
- **Cross-Platform:** Built with Python and CustomTkinter, it runs on Windows, macOS, and Linux.
- **One-Click Actions:** Easily generate the output, copy it to your clipboard, save it to a file, or open a full-featured preview in a separate window.
- **Polished User Experience:** Features a modern dark theme, animated notifications, and a responsive, non-blocking interface that can handle large projects without freezing.

## Getting Started

The easiest way to use AnyText is to download the latest pre-built executable for your system.

1.  Go to the [**Latest Release**](https://github.com/Ali-Kabbadj/AnyText/releases/latest) page.
2.  Download the `AnyText.exe` (for Windows) or the corresponding file for your OS.
3.  Run the executable. No installation is needed!

## How to Use

1.  **Select Project Folder:** Click the main button to open a file dialog and choose the root folder of your project.
2.  **Filter and Refine:**
    - The **Filter Panels** on the left will instantly populate. Uncheck any file extensions or generic file types you wish to exclude.
    - The **Project Structure** panel on the right will show your entire project. Uncheck any specific files or folders you want to omit.
3.  **Generate Output:** Click the **Generate** button. The application will process your selections and display detailed statistics in the "Actions" panel, including the number of selected files, lines, and the estimated token count.
4.  **Save, Copy, or Preview:**
    - **Save to File:** Saves the complete output to a `.txt` file and opens the file's location.
    - **Copy to Clipboard:** Copies the entire output, ready to be pasted into an LLM prompt.
    - **Preview Output:** Opens a new, scrollable window displaying the full generated text.

## Building from Source

#### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO
```

#### 2. Create a Virtual Environment

```bash
python -m venv .venv
# On Windows
.venv\Scripts\activate
# On macOS/Linux
source .venv/bin/activate
```

#### 3. Install Dependencies

```bash
pip install -r requirements-dev.txt
```

#### 4. Run the Application

```bash
python run.py
```

#### 5. Build the Executable

```bash
# On Windows
.\scripts\build.bat
```

The final `.exe` will be in `release` folder.

## Tech Stack

- **Python**
- **CustomTkinter**
- **Pillow**
- **Tiktoken**
- **PyInstaller**

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
