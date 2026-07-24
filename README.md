

# ZeroTab

![Python](https://img.shields.io/badge/python-3.12+-blue.svg)
![License](https://img.shields.io/badge/license-Apache%202.0-green.svg)
![Dependencies](https://img.shields.io/badge/dependencies-0-brightgreen.svg)

Zero-dependency LRU tab eviction daemon built with Python asyncio to profile browser activity and compress idle tabs.

![Hero Image Placeholder](assets/hero.png)

## ✨ Features

- **Zero-Dependency:** Runs entirely on standard Python libraries. No external packages required.
- **O(1) Tab Eviction:** Instantly identifies and compresses idle tabs using an efficient LRU (Least Recently Used) tracking mechanism.
- **Low Footprint:** Operates on `<12MB` RAM without competing with your main system workloads.
- **Non-Blocking Concurrency:** Built with `asyncio` to prevent performance lag, even during heavy browser interactions.

## Architecture Overview

### ZeroTab: Streamlining Browser Memory Management

The architecture involves a flow from the **Active Browser Engine** (which might consume large amounts of RAM, e.g., 6.4 GB) through the **ZeroTab Daemon** (utilizing `asyncio` & O(1) LRU), which passes data to the **JSON Gzip State Serializer**, and finally into **Local Storage** (significantly reducing the footprint, e.g., to 4.2 MB).

Key architectural components and highlights:
* **The Eviction Engine - O(1) LRU State Tracking:** Uses a Hash Map and Doubly-Linked List for instant identification of idle tabs.
* **Non-Blocking Concurrency:** Employs asyncio event loops to prevent performance lag during heavy browser interactions.
* **System Performance - <12 MB RAM Footprint:** The daemon operates with minimal overhead, never competing with main system workloads.
* **Zero-Dependency Architecture:** Built entirely on Python 3.10+ standard library primitives like gzip and collections.

![Architecture Overview Placeholder](assets/architecture_overview.png)

## Setup

### Prerequisites
* **Tech Stack:** Python 3.12+ (Standard Library: `asyncio`, `collections`, `gzip`, `json`)
* **APIs:** OS Process APIs
* **Storage:** Local compressed JSON storage

Follow these steps to get ZeroTab up and running:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/SukritiC/ZeroTab.git
   cd ZeroTab
   ```

2. **Set up a virtual environment (optional but recommended):**
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

3. **Install the package:**
   *(ZeroTab is zero-dependency, so this step simply installs the daemon itself)*
   ```bash
   pip install .
   ```

4. **Run the daemon:**
   ```bash
   python -m zerotab.main
   ```

## ⚙️ Usage & Testing

### Running the Daemon

By default, the daemon runs in the foreground. You can pass configuration options via command-line flags.

To run the daemon targeting a specific browser with custom settings:
```bash
python3 -m zerotab.main --browser safari --timeout 300 --poll 5
```
*(Check `python3 -m zerotab.main --help` for all available options)*

### Running Unit Tests
To verify the core LRU logic and Storage compression, run the built-in `unittest` suite:
```bash
python3 -m unittest discover tests/
```

### Manual Testing & Execution

**For macOS (Native):**
macOS is natively supported via AppleScript. Simply run the daemon targeting your browser of choice (`chrome`, `safari`, `edge`, `brave`, `opera`):
```bash
python3 -m zerotab.main --browser chrome --timeout 30
```
Open a few tabs in your browser, wait 30 seconds without interacting with them, and watch them suspend to a lightweight local stub!

**For Windows & Linux (Chromium Browsers):**
To keep the tool zero-dependency, Windows and Linux use the Chrome Remote Debugging Protocol.
1. Launch your browser from the terminal with the debugging port exposed:
   ```bash
   # Windows (Chrome)
   chrome.exe --remote-debugging-port=9222
   # Linux (Chrome)
   google-chrome --remote-debugging-port=9222
   ```
2. Start the ZeroTab daemon:
   ```bash
   python3 -m zerotab.main --browser chrome --timeout 30
   ```

## 💻 Supported Browsers

- **Google Chrome** (macOS, Linux, Windows)
- **Microsoft Edge** (macOS, Linux, Windows)
- **Brave Browser** (macOS, Linux, Windows)
- **Opera** (macOS, Linux, Windows)
- **Safari** (macOS)

*(Note: Firefox is currently not supported natively as it lacks required AppleScript and CDP tab-query endpoints without heavy modification.)*

## 🤝 Contributing

We welcome contributions! If you have suggestions for improvements, found a bug, or want to add support for a new browser:

- Fork the repository
- Create your feature branch (`git checkout -b feature/AmazingFeature`)
- Commit your changes (`git commit -m 'Add some AmazingFeature'`)
- Push to the branch (`git push origin feature/AmazingFeature`)
- Open a Pull Request

---

## 🚀 Check Out TBRly!

<table>
  <tr>
    <td rowspan="2" align="center" valign="middle">
      <img src="assets/logo.jpeg" width=750" alt="TBRly Logo">
    </td>
    <td>
      If you appreciate tools like <strong>ZeroTab</strong> that streamline your workflow and boost productivity, you'll love <strong>TBRly</strong>! It's our product built for professionals who want to organize and reclaim their time.
    </td>
  </tr>
  <tr>
    <td>
      🔗 <strong><a href="https://tbrly-app.vercel.app/">Visit the TBRly Website</a></strong> <br><br>
      📺 <strong><a href="https://www.youtube.com/playlist?list=PLWLCpnAAmbVk">Watch the TBRly YouTube Demo</a></strong> <br><br>
    </td>
  </tr>
</table>

---

## 🤝 Share the Knowledge

Found these notes helpful?  
Feel free to share them with your peers, friends, or anyone in your learning circle who might benefit from them. Learning is better when it’s collaborative!

> ⚠️ Please note: These notes are shared under the [Apache License 2.0](./LICENSE). While you're welcome to use, modify, and share them, make sure to provide proper credit and include the original license file if you redistribute or adapt the content.
---

## 💬 Let's Connect

<p align="center">
  <a href="https://www.linkedin.com/in/sukritichatterjee/" target="_blank" style="margin-right: 45px;">
    <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/linkedin/linkedin-original.svg" width="40" height="40" alt="LinkedIn"/>
  </a>
  <a href="https://github.com/SukritiC" target="_blank" style="margin-right: 45px;">
    <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/github/github-original.svg" width="40" height="40" alt="GitHub"/>
  </a>
   <a href="https://sukriti-speaks.medium.com/" target="_blank" style="margin-right: 45px;">
    <img src="assets/medium.png" width="40" height="40" alt="Medium"/>
  </a>
    <a href="https://www.youtube.com/@TechDev_Insights" target="_blank" style="margin-right: 45px;">
    <img src="https://upload.wikimedia.org/wikipedia/commons/4/42/YouTube_icon_%282013-2017%29.png" width="55" height="40" alt="YouTube"/>
  </a>
  <a href="https://x.com/SukritiSpeak" target="_blank" style="margin-right: 45px;">
    <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/twitter/twitter-original.svg" width="40" height="40" alt="X (Twitter)"/>
  </a>
  <a href="https://dev.to/sukriti_c" target="_blank" style="margin-right: 45px;">
    <img src="https://d2fltix0v2e0sb.cloudfront.net/dev-badge.svg" width="40" height="40" alt="Dev.to"/>
  </a>
  <a href="https://www.producthunt.com/products/tbrly?launch=tbrly" target="_blank">
    <img src="https://api.producthunt.com/widgets/embed-image/v1/featured.svg?post_id=1&theme=light" width="180" height="40" alt="Product Hunt"/>
  </a>
</p>

<br/>

🔗 [Commudle Profile](https://www.commudle.com/users/SukritiC)
🔗 [Google Cloud Badges](https://www.cloudskillsboost.google/public_profiles/53df2710-444d-4f31-9c37-6c87dfcf102f)
🔗 [Accredible Credential](https://www.credential.net/profile/sukritichatterjee/wallet)
🔗 [Credly Badges](https://www.credly.com/users/sukriti-chatterjee.aadce67f)


> I'm always up for a good AI chat or knowledge exchange — feel free to drop a message!

---

## 📄 License
This project is licensed under the [Apache License 2.0](LICENSE).
