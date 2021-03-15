echo "wait for 120 second"
#sleep 240
#need enough time for pi to reboot and load modules required by camera, and connect to wifi if this script is run by crontab on reboot, this sleep is importtant because crontab start to count time before wifi is ready, if sleep time is too short, user may not even able to see the username command prompt, particularly when the script is end up with shutdown.

source $pyduino/bash/pyduino_variables.sh
cd $local_photo_address
DATE=$(date +"%Y-%m-%d_%H%M")_sa3.jpg


echo "taking photos"
raspistill -vf  -o $DATE  2>> camera_error
echo "sleep for 5 sec"
sleep 5

scp $local_photo_address/$DATE $ssh_scp_photo_address  2>> camera_error
