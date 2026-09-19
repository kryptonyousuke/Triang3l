<h1 align="center">
    <img src=".assets/icon.png" style="width: 100px; margin-inline: auto; position: absolute; top: -110px; left: calc(50% - 50px);" />
    <p style="margin-top: 120px; font-size: 2rem; font-weight: bold;">Triang3l</p>
    <p style="font-weight: bold;">Light-weight discord bot to share punishments across different servers.</p>
    <div align="center">
        <img src="https://img.shields.io/github/last-commit/kryptonyousuke/Triang3l?style=for-the-badge&logo=git&color=red" />
        <img src="https://img.shields.io/github/stars/kryptonyousuke/Triang3l?style=for-the-badge&logo=starship&labelColor=941fd3&color=white" />
        <img alt="GitHub commits since latest release" src="https://img.shields.io/github/commits-since/kryptonyousuke/Triang3l/latest?include_prereleases&style=for-the-badge&logo=google-calendar" />
    </div>
</h1>

## Introduction
Triang3l is a discord bot designed to solve one of the core problems of discord: the big amount of people who harass our members, spam or flood links or insults, etc.

With Triang3l in your server, you can share punishments across a lot of servers which are in the same group, review the reason of such punishment and approve or deny this in your own community, making the moderation of servers with mutual topics become easier and seamless.

> [!NOTE]
> This project is still under development!

## Usage
You do create a group, send the ID to other server owners, they send a join request to the group ID, you accept it and now you all have a common list of punishments.
In the end of the day, you can review the punishments and select exactly which ones you want to sync in your server or not.


## ⛩️ Architecture
Triang3l architecture can be divided into two distinct parts:
- **Command Management**  — User Command -> Triang3l -> asynchronous Discord module -> Discord API.
- **Database Management** — User Command -> Triang3l -> asynchronous Database Management via aiosqlite -> store or read operation -> output via Discord API.

## 🛡️ Security
Triang3l does **not** store any sensitive content about your server or anything else — its only function is to share punishments across diferent servers. Just for instance, Triang3l doesn't even believe or depends on informations given by the user.

The oficial Discord API provides everything that is needed to do our tasks, the only system that depends on extern infos is the invite one, but it has an so simple and pragmatic logic that it's pretty easy to prevent any kind of hacking attemptive.

## 📊 Performance
Triang3l is full asynchronous based, then we have only two bottlenecks: the single-threaded architecture (that can be changed in the future) and the python VM itself.

For large scale bots (1+ Million daily users) this is potentially something that needs some kind of enhancements and attention to avoid expensive hosting fees or even to use everything that your hosting service can provide, but is usually not relevant to small/medium deploys. Since Triang3l is still under development process, that's not our main concern for now.

> [!NOTE]
> Triang3l can even run into a potato!!

## 🗽 Philosophy
Despite of the fact of being still under development, Triang3l aims to be fast, secure, reliable, easy to use and easy to maintain. Beautiful and sophisticated code brings real results to the table.

## 📜 Roadmap
Still thinking about it, but I will update this specific part as soon as possible.

## 💻 Contributing
We didn't built stable contribution standards yet, so feel free to do it at your own way.

## 💎 Donating
<div align="center">
    <p><b>Buy us a coffee!</b></p>
    <a href="https://github.com/sponsors/kryptonyousuke">
        <img src="https://raw.githubusercontent.com/kryptonyousuke/kryptonyousuke/fc854bb8ea379c5afae709335869132f9e412cf1/sponsor.svg" alt="Sponsor Aura" width="220" />
    </a>
</div>

# Credits & Contributors

<div align="center">
	 <p><b>Special thanks to our skilled developers:</b></p>
    <img src="https://contrib.rocks/image?repo=kryptonyousuke/Triang3l" />
</div>

# 💬 Community
Under development.

# 📄 License
Each file in this project carries its own license terms, which are indicated by an `SPDX-License-Identifier` header at the top of the file.

