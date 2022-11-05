# hourse

## **Install Webdriver**

- [Link](https://github.com/mozilla/geckodriver/releases)

## **Start**

```sh
$ python -m venv venv && \
source ./venv/bin/activate && \
pip install --upgrade pip && \
pip install -r requirements.txt
```

## **Format**

```sh
autopep8 --in-place --aggressive *.py --max-line-length 120
```

```sh
celery -A fetch worker --loglevel=info
```

```sh
ps aux | grep firefox | awk '{print $2}' | xargs kill -9
ps -ef | grep defunct | awk '{print $2" "$3}' | xargs kill -9
```