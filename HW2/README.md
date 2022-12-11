Скриптик и его запуск такой да. 

```
docker build -t app -f Dockerfile .
docker run -i -t app
```

Протестим? 

```
albert@albert-caos:~/networks$ docker run -i -t app
root@e2e82c53c54f:/# python3 main.py github.com
1472
```