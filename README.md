# Robot_arm
  robot arm control
  프로젝트로 사용했던 코드.

## 코드내용

- 1.gpio_control.py : tkinter 를 이용하여 모터제어 확인
- 2.cam_roi.py : opencv 를 이용한 ROI 영역 감지.
- 3.cam_udp.py : udp 통신으로, 캠 모니터링 (외부에서 접속
- 4.control_motor.py : 로봇팔의 모터를 동작별로 정의
- 5.roi_with_contorl.py : roi 영역과 모터컨트롤을 연동.

- gpioclass.py : 모터제어를 클래스화.
  - 모터와 GPIO 핀맵을 생성자를 통해 정의 
  - run 메서드의 파라매터로 모터를 제어.
  
- old 폴더 : 구현에 사용된 기본 코드조각들.
