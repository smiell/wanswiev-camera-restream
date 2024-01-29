# Wanswiev camera simply Rest API

RESTful API for controlling and streaming from an IP camera like Wanswiev. Provide also live stream from camera in .jpg format.

This simply app you can run as docker container or you can download source code of Python app and run on own way.

#### Get live stream from camera

```http
  GET http://<YOUR-APP-PUBLIC-IP>:<CONTAINER-PORT>/camera/ch0
```
example:
```http
  GET http://10.66.66.6:5673/camera/ch0
```
## PTZ Control

In compose.yaml file you can provide **two** PTZ preset, which can be used in API request to move camera head.

#### Get all items

```http
  POST http://<YOUR-APP-PUBLIC-IP>:<CONTAINER-PORT>/camera/control/ptz/<int:preset_number>
```
example:
```http
  POST http://10.66.66.6:5673/camera/control/ptz/1
```

## IR Control

App provide ability to toggle IR diode. Try this with API
```http
  POST http://<YOUR-APP-PUBLIC-IP>:<CONTAINER-PORT>/camera/control/ir/<string:on/off>
```
example:
```http
  POST http://10.66.66.6:5673/camera/control/ir/on
```

## Reboot camera
You can reboot camera via API request
```http
  POST http://<YOUR-APP-PUBLIC-IP>:<CONTAINER-PORT>/camera/control/reboot
```
example:
```http
  POST http://10.66.66.6:5673/camera/control/reboot
```
## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`CAMERA_IP`=`10.66.66.6`

`CAMERA_USER_NAME`=`admin`

`CAMERA_USER_PASS`=`123456`

`PTZ_1`=`31&onestep=0&sit=31&17062865540080.5238427280103255&_=1706286554008`

`PTZ_2`=`33&onestep=0&sit=33&17062865331300.5001876041888236&_=1706286533130`


## FAQ

#### What does the application give you?

The application will allow you to easily integrate your Wanswiev camera, e.g. with Home Assistan.
Thanks to this, you will be able to get the full potential from your old IP camera.
Home Assistant will gain the ability to take live screenshots of the camera image and record what it sees, because the original camera stream is not compatible due to headers.

#### Where can I get commands for PTZ presets?

First, you need to create these two PTZ presets in your camera's admin panel.
Once you have created them, you can click on one of them and through DevTools in your browser you will be able to see what XHR request was sent. Once you have this, all you need to do next is copy the string from the entire command, e.g.:

```http
  http://10.66.66.8/decoder_control.cgi?loginuse=admin&loginpas=123456&command=33&onestep=0&sit=33&17065591672480.15122452876391757&_=1706559167249
```
Here is your's command to call camera to for. example PTZ 1
**33&onestep=0&sit=33&17065591672480.15122452876391757&_=1706559167249**
