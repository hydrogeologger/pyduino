create a new file called 'credential.h' with the following contents
// Replace with your actual SSID and password:
//https://arduino.stackexchange.com/questions/40411/hiding-wlan-password-when-pushing-to-github
//create a profile in sparkfun with the following items:
//"winddir","windspeedmps","rainmm","dailyrainmm","tempcel","humidity","barotempcel","hectopascals","soiltempcel","soilmoisture","uv_up","uv_down","ir_up","ir_down","vis_up","vis_down"

----------------------------------------------
#define SPARKFUN_SERVER_ADDR "your bare web address in quote, no port number, no http://"
#define SPARKFUN_SERVER_KEY_PUBLIC "your publickey in the quote"
#define SPARKFUN_SERVER_KEY_PRIVATE "your private in the quote"
#define REPORT_INTERVAL_SECOND 60
#define SPARKFUN_SERVER_PORT 8080
