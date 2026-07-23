

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

## 💻 Supported Browsers

- **Google Chrome** (macOS, Linux, Windows)
- **Mozilla Firefox** (macOS, Linux, Windows)
- **Safari** (macOS)
*(Note: Browser support depends on the underlying OS Process APIs available.)*

## ⚙️ Usage & Configuration

By default, the daemon runs in the foreground. You can pass configuration options via command-line flags or environment variables (coming soon).

To run the daemon with custom settings (example):
```bash
python -m zerotab.main --timeout 300 --max-ram 4096
```
*(Check back for more detailed configuration options as they are implemented!)*

## 🤝 Contributing

We welcome contributions! If you have suggestions for improvements, found a bug, or want to add support for a new browser:
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

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
  <a href="https://x.com/SukritiSpeak" target="_blank">
    <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/twitter/twitter-original.svg" width="40" height="40" alt="X (Twitter)"/>
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
