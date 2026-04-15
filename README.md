# Reveal.js PPT Presentations

This repository contains web-based presentations built with [Reveal.js](https://revealjs.com/). 

## 📂 Contents

- **`react-agent-sharing/`**: A comprehensive presentation about ReAct Agents, LLMs, Tool Calling, and MCP (Model Context Protocol). Includes dynamic flowcharts and code walkthroughs.

## 🚀 How to View the Presentations

The presentations are fully self-contained and support **offline viewing** (all Reveal.js assets are bundled locally).

### Method 1: Direct File Open (Easiest)
1. Clone or download this repository to your local machine:
   ```bash
   git clone https://github.com/nvd11/revealjs-ppt-presentations.git
   ```
2. Navigate to the folder of the presentation you want to view (e.g., `react-agent-sharing/`).
3. Double-click the `index.html` file to open it in any modern web browser (Chrome, Edge, Safari, etc.).

### Method 2: Local Web Server (Recommended)
If you encounter any browser security restrictions with local files (CORS issues), it is recommended to run a simple local server:
1. Open a terminal in the root folder of the presentation (e.g., inside `react-agent-sharing/`).
2. Run Python's built-in HTTP server:
   ```bash
   python3 -m http.server 8000
   ```
3. Open your browser and navigate to `http://localhost:8000`.

## 🎮 Presentation Controls

- **`→` (Right Arrow) / `Spacebar`**: Next slide / Next animation step
- **`←` (Left Arrow)**: Previous slide / Previous animation step
- **`↓` (Down Arrow)**: Next vertical slide (used for deep dives into a specific topic)
- **`↑` (Up Arrow)**: Previous vertical slide
- **`F`**: Fullscreen mode
- **`ESC` / `O`**: Overview (Slide Map) mode

---
*Created for team sharing and technical presentations.*
