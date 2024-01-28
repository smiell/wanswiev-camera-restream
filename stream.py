import time, cv2, requests, os, sys
from flask import Flask, Response, request, jsonify
from imutils.video import VideoStream

app = Flask(__name__)

# Camera Log-in credentials
camera_ip_address = os.environ.get('CAMERA_IP')
camera_admin_user = os.environ.get('CAMERA_USER_NAME')
camera_admin_pass = os.environ.get('CAMERA_USER_PASS')

# Set two custom PTZ preset
ptz_preset1 = os.environ.get('PTZ_1')
ptz_preset2 = os.environ.get('PTZ_2')

# Check if varaibles are available and not empty
if not all([camera_ip_address, camera_admin_user, camera_admin_pass, ptz_preset1, ptz_preset2]):
        print('One or more required environment variables are missing or empty. Exiting...')
        sys.exit(1)

camera_url = f"http://{camera_ip_address}/videostream.cgi?loginuse={camera_admin_user}&loginpas={camera_admin_pass}"

vs = VideoStream(camera_url).start()
time.sleep(2)  # Give some time to initialize

def generate_frames():
    while True:
        frame = vs.read()

        if frame is None:
            time.sleep(2)
            continue

        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/camera/ch0')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Base Url to control camera PTZ
cameraAPIPtzUrl = f"http://{camera_ip_address}/decoder_control.cgi?loginuse={camera_admin_user}&loginpas={camera_admin_pass}"

def send_ptz_command(preset_number):
    # Appropriate commands for PTZ presets
    if preset_number == 2:
        command = ptz_preset2
    elif preset_number == 1:
        command = ptz_preset1
    else:
        return "Invalid preset number", 400

    response = requests.get(cameraAPIPtzUrl + f"&command={command}")
    return response.text, response.status_code

@app.route('/camera/control/ptz/<int:preset_number>', methods=['POST'])
def ptz(preset_number):
    result, status_code = send_ptz_command(preset_number)
    return jsonify(result=result, status=status_code)

# Base Url to control camera IR
cameraAPIControl = f"http://{camera_ip_address}/camera_control.cgi?loginuse={camera_admin_user}&loginpas={camera_admin_pass}"

def toggle_ir(command):
    # Appropriate commands for camera control
    if command == 'on':
        commandToSend = "14&value=0&17061360422880.47475485418809016&_=1706136042289"
    elif command == 'off':
        commandToSend = "14&value=1&17061360769750.8988460571190899&_=1706136076975"
    else:
        return "Invalid control command", 400
    
    response = requests.get(cameraAPIControl + f"&param={commandToSend}")
    return response.text, response.status_code

@app.route('/camera/control/ir/<string:IrOnOff>', methods=['POST'])
def ir(IrOnOff):
    result, status_code = toggle_ir(IrOnOff)
    return jsonify(result=result, status=status_code)

# Endpoint to reset the camera
cameraAPIReboot = f"http://{camera_ip_address}/reboot.cgi?loginuse={camera_admin_user}&loginpas={camera_admin_pass}"

def reboot():
    response = requests.get(cameraAPIReboot)
    return response.text, response.status_code

@app.route('/camera/control/reboot', methods=['POST'])
def CameraReboot():
    result, status_code = reboot()
    return jsonify(result=result, status=status_code)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
