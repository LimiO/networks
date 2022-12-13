Давайте начнем с настроек. Настроим сначала интернет (R5)


```
> en
> conf t
// тут нам надо просто расставить айпишники на интерфейсы
> interface Ethernet 0/0
> no shutdown
> ip address 111.222.10.1 255.255.255.0
> exit

// на 0/1 ставим 111.222.20.1
// на 0/2 ставим 111.222.30.1
> wr
```


Теперь настраиваем R6. Тут довольно сложно, буду иногда буду комментить.
```
// расставляем айпишники. на 0/0 111.222.30.2, на 0/1 10.0.30.1, это можно взять выше.
// 
> ip route 0.0.0.0 0.0.0.0 111.222.30.1
> ip route 10.0.10.2 255.255.255.255 10.222.10.1

// Теперь тоннельчики!
> int tunnel 2
> no shutdown
> ip address 10.222.10.2 255.255.255.252
> tunnel source 111.222.30.2
> tunnel destination 111.222.10.2
> ip mtu 1400
> ip tcp adjust-mss 1360
> exit

Проверял я как обычно через пинги, через просмотр eve wireshark и через просмотр настроек на каждом из роутеров. 

// ACL'ки, как обычно. 
> access-list 101 permit gre host 111.222.30.2 host 111.222.10.2

// теперь шифрование
> crypto isakmp policy 10
> encryption aes
> authentication pre-share
> group 2
> hash sha
> exit
> crypto isakmp key albert address 111.222.10.2
> crypto ipsec transform-set ALBERT-IPSEC esp-aes 256 esp-sha-hmac
> mode transport
> exit
> crypto map ALBERT-MAP 1 ipsec-isakmp
> set peer 111.222.10.2
> set transform-set ALBERT-IPSEC
> match address 101
> exit

// и теперь бахаем это на 0/0 интерфейс
> crypto map ALBERT-MAP
```


Теперь настраиваем R4, он точно такой же как R6, только немного меняем айпишники и убираем часть про acl и шифрование. Меняем как в первой дз 1 на 2 и готово.

```
// айпишники: 0/0 - 10.0.10.1, 0/1 - 111.222.10.2
> ip route 0.0.0.0 0.0.0.0 111.222.10.1
> ip route 10.0.20.2 255.255.255.255 10.111.10.2
> ip route 10.0.30.2 255.255.255.255 10.222.10.2

// тут настраиваем два тоннеля, один tonnel 1, другой tonnel 2 (только тут меняем source и destination местами). 
// ACL'ки тоже меняем местами и немного по-другому. 
// crypto точно так же настраиваем до момента ipsec и меняем айпишник там на 30.
> crypto ipsec transform-set ALBERT-UNIT esp-aes 256 esp-sha-hmac
> mode transport
> exit
> set peer 111.222.30.2
> set transform-set ALBERT-UNIT
> match address 101
> exit

// И опять же криптомапу на первый интерфейс бахаем.
```

Осталось настроить R7 и тачки. 
```
// 0/0 интерфейс, 111.222.20.2
// 0/1 интерфейс, 10.0.20.1
// Теперь настраиваем туннель 1 тут по аналогии с тем как настроили раньше. На этом все.
```

VPC1 
```
ip 10.0.10.2 255.255.255.0 10.0.10.1
```

VPC2
```
ip 10.0.20.2 255.255.255.0 10.0.20.1
```

VPC3
```
ip 10.0.30.2 255.255.255.0 10.0.30.1
```
