# house

## **Install Webdriver**

- [Link](https://github.com/mozilla/geckodriver/releases)

## **Start**

```sh
$ python -m venv venv && \
source ./venv/bin/activate && \
pip install --upgrade pip && \
pip install -r requirements.txt
```

## **Exec**

```sh
$ ./main.py
```

## **Format**

```sh
$ autopep8 --in-place --aggressive *.py --max-line-length 120
```