# ChainTales

[![ci/gh-actions/lint](https://github.com/sn1f3rt/ChainTales/actions/workflows/lint.yml/badge.svg)](https://github.com/sn1f3rt/ChainTales/actions/workflows/lint.yml)
[![ci/gh-actions/format](https://github.com/sn1f3rt/ChainTales/actions/workflows/format.yml/badge.svg)](https://github.com/sn1f3rt/ChainTales/actions/workflows/format.yml)

> A proof-of-concept web3-based blogging platform with KYC support

## Table of Contents

- [About](#about)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running](#running)
  - [Development](#development)
  - [Production](#production)
- [License](#license)

## About

ChainTales is a next-generation decentralized blogging platform that combines content freedom with responsible identity. It ensures that only users who have completed KYC verification can publish posts or send cryptocurrency tips, creating a trust-enhanced environment for meaningful, authentic interactions.

Users authenticate via **Sign-In with Ethereum (SIWE)**, using their Ethereum wallets instead of traditional usernames and passwords. The identity verification process is handled through a KYC module with context-sensitive privacy controls, allowing users to choose which identity attributes to disclose. Once verified, users can publish blogs, interact with others, and tip creators — all within a transparent, blockchain-powered ecosystem.

ChainTales integrates:
- 🔐 **KYC-Gated Access** – Posts and tipping are restricted to verified users only.
- 🧾 **Context-Sensitive Privacy** – Share only the identity details needed for each interaction.
- 📝 **Immutable Blog Posts** – Content is stored and tracked through blockchain-backed systems.
- 💸 **Crypto Tipping** – Reward creators with Ethereum-based microtransactions.
- ⚙️ **Modern Tech Stack** – Flask, SQLAlchemy, Web3.py, and Ganache for seamless DApp development.

This project builds on the capabilities of two foundational systems:
- [**BlogChain**](https://github.com/sn1f3rt/BlogChain) – A decentralized blogging application with Ethereum login and tipping.
- [**IDenSafe**](https://github.com/sn1f3rt/IDenSafe) – A blockchain-based digital identity platform with selective KYC.

ChainTales aims to redefine decentralized content platforms by merging anonymity, accountability, and incentive — all while giving users full control over their identity and data.

## Prerequisites

- Git
- Python 3.12
- Node.js 18 (& npm)
- MariaDB/MySQL database

## Installation

1. Install [`uv`](https://docs.astral.sh/uv/)

2. Install [`make`](https://www.gnu.org/software/make/)

3. Clone the repository

   ```shell
    git clone https://github.com/sn1f3rt/ChainTales.git
   ```
   
4. Switch to the project directory

   ```shell
    cd ChainTales
   ```
   
5. Create a virtual environment

   ```shell
   make env
   ```
   
6. Activate the virtual environment

   ```shell
   source .venv/bin/activate
   ```
   
7. Install Python dependencies

   ```shell
   make install
   ```
   
8. Install [Ganache](https://archive.trufflesuite.com/ganache/) CLI

   ```shell
    npm i
    ```

## Configuration

Create a file named `config.yaml` in the root directory with the following structure:

```yaml
app:
  secret_key: "n_bytes_hex_string"
  testing: true # set to false for production

db:
  host: "localhost"
  port: 3306
  user: "sn1f3rt"
  password: "password"
  name: "chaintales"

web3:
  provider: "http://localhost:7545" # Ganache default

recaptcha:
  site_key: "your_recaptcha_site_key"
  secret_key: "your_recaptcha_secret_key"

```

- update the `SECRET_KEY` variable with a 32-bit hexadecimal string.
- update the `DB_*` variables with your database credentials.
- update the `WEB3_PROVIDER` variable with the URL of your Ethereum node.

## Running

### Development

#### Run Ganache CLI

```shell
npm run ganache-dev
```

#### Run the web app

```shell
make dev
```

The app will be running at `http://localhost:3000`.

### Production

#### Run Ganache CLI

```shell
npm run ganache-prod
```

#### Run the web app

```shell
make prod
```

or if you want to enable SSL support

```shell
make prod-ssl cert.pem key.pem
```

The app will be running at `http(s)://<YOUR-SERVER_IP>>:13139`. The certificate and key files are required for SSL support.

## License

[![License](https://img.shields.io/github/license/sn1f3rt/ChainTales)](LICENSE)

Copyright &copy; 2025 [Sayan "sn1f3rt" Bhattacharyya](https://sn1f3rt.dev)
