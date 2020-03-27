# smartWindow
### [데모 영상][demo]
--------
> ####  조도 센서, 온습도센서, 연기센서, 빗물감지센서, 인체감지센서 등 IoT 센서와 라즈베리 파이를 이용한 스마트 창문을 개발하였습니다.    
> ####  조도센서를 통해 전달받은 값을 이용하여 유리에 부착된 PDLC 필름에 ON/OFF 값을 주어 채광 조절을 하고, 온습도센서 및 기상청 API, 미세먼지 센서를 활용하여 여러 조건들을 만들어 자동으로 창문이 열림/닫힘 기능이 가능하도록 구현하였습니다.   
> ####  인체감지 센서는 창문 외부에 설치하여 사람이나 혹은 물체가 감지되었을 경우 조건과 무시하고 창문을 닫습니다. 빗물감지센서를 활용하여 설정된 조건이더라도 빗물이 감지된다면 창문을 닫도록 설계하였고 기상청 API를 활용하여 현재 위치의 기상상황과 일치한지 확인하고 일치하는 경우, 일치하지 않은 경우 등을 나누어 조건을 설정하였습니다.   
> ####  위와 같이 센서 값을 받아 자동으로 창문이 개폐 될 때도 있지만 스마트폰 어플리케이션을 활용하여 수동으로 개폐할 수 있도록 어플리케이션을 추가로 개발하였습니다. 어플리케이션은 등록된 창문의 센서 값을 실시간 확인 할 수 있고, 사용자가 원하는 조건을 설정할 수 있도록 만들었습니다.
| sample | main loop |
|---|---|
| ![img1](https://github.com/BangGyoo/Portfolio_Gyoo/blob/Test/language/python/3.gif) | ![img2](/documentation/total.jpg) |   
 
| output | weighted sum |
|---|---|
| ![img3](/documentation/output.jpg) | ![img4](/documentation/Weighted%20Sum.jpg) |

[//]: #
[link]: <https://www.dbpia.co.kr/journal/articleDetail?nodeId=NODE07613626>
[demo]: </documentation/demo.mp4>
