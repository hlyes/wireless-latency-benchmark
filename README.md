# wireless-latency-benchmark

[![Build Status](https://travis-ci.org/if1live/wireless-latency-benchmark.png?branch=master)](https://travis-ci.org/if1live/wireless-latency-benchmark)
[![Coverage Status](https://coveralls.io/repos/if1live/wireless-latency-benchmark/badge.png?branch=master)](https://coveralls.io/r/if1live/wireless-latency-benchmark?branch=master)

wifi/bluetooth latency benchmark

## 개요

요즘에 스마트폰에서 자이로 센서값을 읽어서 PC로 전송하는걸 만들고 있다.
"센서값은 시간이 조금만 지나도 무의미하니까 일단 빨리 보낼수있게 UDP를 써야지",
"게임에서 사용할거니까 60FPS의 속도로 계속 보내면 거의 실시간값을 읽을수있겠지?" 하고 구현했는데 생각보다 후지더라.
몇 초 간격으로 패킷 LOST가 발생해서 센서값이 갱신되지 않더라. 
그래서 UDP를 포기하고 TCP로 짜봣는데 UDP에 비해서 썩 좋아진걸 느끼지 못했다.

그때, PS3 컨트롤러는 Bluetooth를 쓴다는 정보를 보고 Bluetooth의 latency에 대해서 찾아봤는데 마땅히 정리된 자료가 없더라.
그나마 [찾은 자료][bluetooth-vs-wifi]에는 Latency가 Bluetooh=200ms, Wifi=150ms라는 믿을 수 없는 수치가 적혀있더라.
아니, bluetooth의 latency가 200ms씩이나 되면 PS3 게임을 어떻게 할 수 있단 말인가?!?!

그러고보니 Throughput(처리량)과 Response Time(응답시간)이 비례하는건 아니었지?
wifi가 bluetooth보다 전송속도는 빠른데 latency는 느리다거나 뭐 그런건 아니려냐??

그래서 직접 Bluetooth/Wifi의 Latency를 측정해보기로 했습니다.

## 실험

TCP, UDP, RFCOMM을 이용한 Echo Server를 만들었다. 32바이트의 메세지를 1000번 전송하고 지연시간을 측정했다.
(지연시간은 클라이언트가 서버로 메세지를 보내고 서버로부터 메세지를 받을때까지 시간으로 정의한다)

TCP, UDP는 [SocketServer][socketserver]를 이용해서 구현하고
Bluetooth는 [PyBluez][pybluez]를 이용해서 구현했다. 
Bluetooth 통신 규격은 RFCOMM, L2CAP 이 있는데 [윈도우7에서는 PyBluez가 L2CAP를 제대로 지원하지 못하는 듯][pybluez-l2cap-error]해서 RFCOMM만 구현했다.

테스트 환경에서의 네트워크 구성은 다음과 같다
* Socket : A(client) <--wifi--> AP <--100Mb/s--> hub <--100Mb/s--> hub <--1Gb/s-> B(server)
* Bluetooth : A(client) <--bluetooth--> B(server)
* Ad-Hoc : A(client) <--wifi--> B(server)

### UDP

timeout=1초 잡았다. latency=999는 timeout을 의미한다.

```bash
# Server
cd benchmark
python udp_server.py
```

```bash
# Client
cd benchmark
python udp_client.py xxx.xxx.xxx.xxx
```

### TCP
```bash
# Server
cd benchmark
python tcp_server.py
```

```bash
# Client
cd benchmark
python tcp_client.py xxx.xxx.xxx.xxx
```

### RFCOMM
```bash
# Server
cd benchmark
python rfcomm_server.py
```

```bash
# Client
cd benchmark
python rfcomm_client.py
```


## 결과

실행 결과는 repo에 집어넣어놨다. 
[간단히 정리하고 그래프까지 넣은 스프레드시트][result-sheet]까지 준비했다

### 95%까지의 평균

단위는 ms이며, 소수 5자리 이하는 버렸다.

TCP	| UDP | RFCOMM | TCP Ad-Hoc | UDP Ad-Hoc
--- | --- | ------ | ---------- | ----------
2.5182 | 2.6631 | 8.4831 | 3.1789 | 3.1776

### 요약 정보

단위는 ms이며, 쓸데없이 긴 소수점 아래는 버렸다.

% | TCP | UDP | RFCOMM | TCP Ad-Hoc | UDP Ad-Hoc
--- | --- | --- | ------ | ---------- | ----------
10% | 1.7501 | 1.8091 | 6.94026	| 1.7335 | 1.7547
20%	| 1.8246 | 1.8489 | 6.99306	| 2.2221 | 2.3062
30%	| 1.8501 | 1.9330 | 7.88968	| 2.4378 | 2.5613
40% | 1.9431 | 1.9654 | 7.91706	| 2.5794 | 2.7284
50%	| 1.9751 | 2.0546 | 7.94053	| 2.7137 | 2.8415
60%	| 2.0889 | 2.1499 | 7.96840	| 2.8901 | 3.0271
70%	| 2.3826 | 2.5837 | 8.00800	| 3.6998 | 3.6380
80%	| 3.3274 | 3.6793 | 8.92857	| 4.8301 | 4.6495
90%	| 5.7567 | 6.3746 | 16.9038	| 6.0963 | 5.7756

[![상위 90% Latency][basic-latency-chart-img]][basic-latency-chart]

### 긴 지연시간(%)

latency | TCP | UDP | RFCOMM | TCP Ad-Hoc | UDP Ad-Hoc
------- | --- | --- | ------ | ---------- | ----------
>50ms | 1.6 | 1.7 | 0 | 1.9 | 0.6
>100ms | 1.7 | 1.8 | 0 | 1.9 | 0.7
>200ms | 1.7 | 1.8 | 0 | 1.1 | 0.7
>300ms | 1.4 | 1.8 | 0 | 0.4 | 0.7
Timeout | 0 | 1.8 | 0 | 0 | 0.7

[![Long Latency][long-latency-chart-img]][long-latency-chart]

## 결과분석

상위 95% 의 평균을 보면 latency가 16ms보다 작다. 재수없어서 하위 5%에 속하지 않는 이상 게임에 사용하면 1프레임마다 새로운 정보를 받을 수 있다. 이것만 보면 어떤 통신수단을 선택하더라도 게임에 쓰기에는 문제없는거처럼 보인다.

상위 10%~90%의 Latency를 보면 TCP/UDP/TCP Ad-Hoc/UDP Ad-Hoc 전부 거기서 거기다. 기껏해야 1ms정도밖에 차이가 안난다.
블투투스의 경우는 그것에 비하면 상당히 느려보인다. 그래도 상위 90%의 값을 보면 16ms근처다. 게임에 사용하기에는 큰 문제가 없어보인다.

제일 중요한 긴 지연시간의 발생비율을 보자. 50ms이상부터 긴 지연시간으로 간주했다. (50ms는 대략 16ms*3, 즉 60FPS기준으로 3프레임 늦는다는 의미이다)
**오직 RFCOMM만이 긴 지연시간 발생비율이 0%이다**. 다른것은 대략 1~2%정도의 확률로 발생한다. 1%면 별 문제 없는거 아니야? 라고 생각할수 없는 이유는 60FPS로 통신을 하기로 했기 때문이다. 1%면 2초에 한번씩은 끊기는것을 볼수 있다는건데...이게 말이 되나? 

긴 지연시간의 발생 비율은 TCP건 UDP건 크게 차이나지 않는다. 다만 UDP는 timeout이 존재한다. TCP의 경우는 가장 긴 latency가 300ms근처였다.

UDP와 UDP Ad-Hoc을 비교하면 UDP Ad-Hoc에서 긴 지연시간이 적게 발생한다. (% 자체가 정직하게 보여준다)
TCP의 경우도 마찬가지이다(50ms,100ms 초과한 비율은 ad-hoc이 더 높게 나오지만 200ms이상의 값은 ad-hoc가 적게 발생한다)
즉, 1:1 연결(Ad-Hoc)이 복잡한 네트워크에 비해서 빠르고 안정적이다.

## 결론

안정적이고 빠른 latency가 필요하면 Bluetooth가 최선의 선택이다. (예를 들면 게임 컨트롤러, 입력장치, 센서,...)

## Reference

* [Bluetooth vs Wifi][bluetooth-vs-wifi]
* [An Introduction to Bluetooth Programming][bluetooth-dev]
* [PyBluez][pybluez]

[bluetooth-vs-wifi]: http://www.diffen.com/difference/Bluetooth_vs_Wifi

[result-sheet]: https://docs.google.com/spreadsheet/ccc?key=0AhRfWUmEuMJxdHBaMm55MXBLZW9nWjFFQjUtVXBsZUE&usp=sharing

[basic-latency-chart-img]:https://raw.github.com/if1live/wireless-latency-benchmark/master/document/latency-basic.png
[basic-latency-chart]: https://docs.google.com/spreadsheet/oimg?key=0AhRfWUmEuMJxdHBaMm55MXBLZW9nWjFFQjUtVXBsZUE&oid=2&zx=kiukxz9003bx

[long-latency-chart-img]:https://raw.github.com/if1live/wireless-latency-benchmark/master/document/long-latency.png
[long-latency-chart]: https://docs.google.com/spreadsheet/oimg?key=0AhRfWUmEuMJxdHBaMm55MXBLZW9nWjFFQjUtVXBsZUE&oid=3&zx=chxjwry4h34q
[pybluez]: https://code.google.com/p/pybluez/
[socketserver]: http://docs.python.org/2/library/socketserver.html
[pybluez-l2cap-error]: https://code.google.com/p/pybluez/issues/detail?id=38
[bluetooth-dev]: http://people.csail.mit.edu/albert/bluez-intro/
