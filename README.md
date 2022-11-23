# ur-web-spider

## install dependency

```bash
python -m pip install -r requirements.txt
python -m pip install --upgrade -r requirements.txt
```

## execute

```bash
python src/main.py
```

## execute with dev mode (no request to real server)

cat config.yaml
isDev: true

```bash
python src/main.py
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
