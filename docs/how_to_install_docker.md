# Docker および Docker Compose インストールガイド

このドキュメントでは、Windows、macOS、Linuxにおける Docker および Docker Compose のインストール方法について説明します。

## 目次

- [Windows へのインストール](#windows-へのインストール)
- [macOS へのインストール](#macos-へのインストール)
- [Linux へのインストール](#linux-へのインストール)
- [インストールの確認](#インストールの確認)

## Windows へのインストール

### システム要件

- Windows 10 64ビット: Home、Pro、Enterprise、または Education（Build 19041以降）
- WSL 2（Windows Subsystem for Linux 2）が有効化されていること
- 仮想化がBIOSで有効化されていること

### インストール手順

1. [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/) の公式サイトからインストーラーをダウンロードします。

2. ダウンロードした `.exe` ファイルをダブルクリックしてインストーラーを実行します。

3. インストールウィザードの指示に従ってインストールを完了します。
   - 「WSL 2 based engine」オプションが選択されていることを確認してください。

4. インストールが完了したら、Docker Desktop を起動します。
   - 初回起動時に、WSL 2のインストールや設定が必要な場合があります。画面の指示に従って設定を完了してください。

5. Docker Desktop が正常に起動したら、タスクバーのDocker アイコンが表示されます。

### WSL 2 のセットアップ（必要な場合）

WSL 2がまだインストールされていない場合は、以下の手順でインストールします：

1. PowerShellを管理者として開き、以下のコマンドを実行します：

```powershell
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
```

2. コンピュータを再起動します。

3. [WSL 2 Linux カーネル更新プログラム](https://docs.microsoft.com/ja-jp/windows/wsl/install-manual#step-4---download-the-linux-kernel-update-package) をダウンロードしてインストールします。

4. PowerShellを開き、以下のコマンドを実行してWSL 2をデフォルトバージョンとして設定します：

```powershell
wsl --set-default-version 2
```

## macOS へのインストール

### システム要件

- macOS 12以降（Monterey、Ventura、Sonoma）
- Apple Silicon（M1、M2、M3チップ）または Intel チップ搭載のMac

### インストール手順

1. [Docker Desktop for Mac](https://www.docker.com/products/docker-desktop/) の公式サイトからインストーラーをダウンロードします。
   - Apple Silicon（M1/M2/M3）搭載のMacの場合は「Apple Chip」を選択
   - Intel チップ搭載のMacの場合は「Intel Chip」を選択

2. ダウンロードした `.dmg` ファイルをダブルクリックして開きます。

3. Docker アプリケーションをApplicationsフォルダにドラッグ＆ドロップします。

4. Applicationsフォルダから Docker を起動します。
   - 初回起動時に、システム拡張のインストールや権限の確認が求められる場合があります。

5. Docker Desktop が正常に起動したら、メニューバーのDocker アイコンが表示されます。

## Linux へのインストール

Linux では、ディストリビューションによってインストール方法が異なります。ここでは主要なディストリビューションでのインストール方法を説明します。

### Ubuntu

#### システム要件

- Ubuntu 20.04 LTS 以降
- 64ビットアーキテクチャ
- KVM 仮想化のサポート

#### Docker Engine のインストール

1. 古いバージョンがある場合は削除します：

```bash
sudo apt-get remove docker docker-engine docker.io containerd runc
```

2. 必要なパッケージをインストールします：

```bash
sudo apt-get update
sudo apt-get install ca-certificates curl gnupg lsb-release
```

3. Docker の公式 GPG キーを追加します：

```bash
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
```

4. リポジトリを設定します：

```bash
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

5. Docker Engine をインストールします：

```bash
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin
```

#### Docker Desktop のインストール（オプション）

1. [Docker Desktop for Linux](https://docs.docker.com/desktop/install/linux-install/) から `.deb` パッケージをダウンロードします。

2. パッケージをインストールします：

```bash
sudo apt-get update
sudo apt-get install ./docker-desktop-<version>-<arch>.deb
```

3. Docker Desktop を起動します：

```bash
systemctl --user start docker-desktop
```

### Fedora

#### Docker Engine のインストール

1. リポジトリを設定します：

```bash
sudo dnf -y install dnf-plugins-core
sudo dnf config-manager --add-repo https://download.docker.com/linux/fedora/docker-ce.repo
```

2. Docker Engine をインストールします：

```bash
sudo dnf install docker-ce docker-ce-cli containerd.io docker-compose-plugin
```

3. Docker サービスを開始します：

```bash
sudo systemctl start docker
sudo systemctl enable docker
```

#### Docker Desktop のインストール（オプション）

1. [Docker Desktop for Linux](https://docs.docker.com/desktop/install/linux-install/) から `.rpm` パッケージをダウンロードします。

2. パッケージをインストールします：

```bash
sudo dnf install ./docker-desktop-<version>-<arch>.rpm
```

3. Docker Desktop を起動します：

```bash
systemctl --user start docker-desktop
```

### Debian

#### Docker Engine のインストール

1. 古いバージョンがある場合は削除します：

```bash
sudo apt-get remove docker docker-engine docker.io containerd runc
```

2. 必要なパッケージをインストールします：

```bash
sudo apt-get update
sudo apt-get install ca-certificates curl gnupg lsb-release
```

3. Docker の公式 GPG キーを追加します：

```bash
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
```

4. リポジトリを設定します：

```bash
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

5. Docker Engine をインストールします：

```bash
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin
```

## インストールの確認

インストールが正常に完了したかどうかを確認するには、以下のコマンドを実行します：

### Docker のバージョン確認

```bash
docker --version
```

### Docker Compose のバージョン確認

```bash
docker compose version
```

### Docker が正常に動作するか確認

```bash
docker run hello-world
```

このコマンドが正常に実行されると、「Hello from Docker!」というメッセージが表示されます。これは、Docker が正しくインストールされ、動作していることを示しています。

## トラブルシューティング

### Windows での一般的な問題

- **WSL 2 関連のエラー**: WSL 2 が正しくインストールされていることを確認してください。
- **仮想化が有効になっていない**: BIOS/UEFI 設定で仮想化（Intel VT-x/AMD-V）が有効になっていることを確認してください。

### macOS での一般的な問題

- **権限エラー**: システム環境設定でセキュリティとプライバシーの設定を確認してください。
- **リソース不足**: Docker Desktop の設定でリソース（メモリ、CPU）の割り当てを調整してください。

### Linux での一般的な問題

- **権限エラー**: ユーザーが `docker` グループに追加されていることを確認してください：

```bash
sudo usermod -aG docker $USER
newgrp docker
```

- **サービスが起動しない**: Docker サービスの状態を確認してください：

```bash
sudo systemctl status docker
```

## 参考リンク

- [Docker 公式ドキュメント](https://docs.docker.com/)
- [Docker Desktop for Windows](https://docs.docker.com/desktop/install/windows-install/)
- [Docker Desktop for Mac](https://docs.docker.com/desktop/install/mac-install/)
- [Docker Engine for Linux](https://docs.docker.com/engine/install/)
