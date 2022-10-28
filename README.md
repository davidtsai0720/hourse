# house

## **Install Python**

```sh
$ sudo apt update && sudo apt upgrade -y
```

```sh
$ sudo apt install software-properties-common -y
```

```sh
$ sudo add-apt-repository ppa:deadsnakes/ppa
```

```sh
$ sudo apt install python3.11
```

## **Install Google Chrome**

```sh
$ sudo curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add && \
sudo bash -c "echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' >> /etc/apt/sources.list.d/google-chrome.list" && \
sudo apt -y update && \
sudo apt -y install google-chrome-stable
```