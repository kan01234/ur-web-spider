# ur-web-spider

[![run](https://github.com/kan01234/ur-web-spider/actions/workflows/execute-main.yml/badge.svg)](https://github.com/kan01234/ur-web-spider/actions/workflows/execute-main.yml)

## install dependency

```bash
python3 -m pip install -r requirements.txt
python3 -m pip install --upgrade -r requirements.txt
```

## execute

```bash
python3 src/main.py
```

## execute with dev mode (no request to real server)

cat config.yaml
isDev: true

```bash
python3 src/main.py
```

## test

```bash
python3 -m pytest
python3 -m pytest -k testSplitStation
```

## output

### json file

bukken-yyyyMMdd'T'HHmm.json

example

```json
[
    {"madori": null, "allCount": "15", ....}
]
```
