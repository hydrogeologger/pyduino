# Credentials
All credentials are stored here

Check host address is correct and replace `********************` with appropriate token

## Logger Credentials
The credentials for logger data are stored here in a JSON file, below is a example:
```json
{
    "thingsboard_host": "www.abc.cloud.edu.au",
    "access_token": "********************"
}
```

## IP Reporting
To add extra location for logger to report IP addresses to, please add the following lines to appropriate shell file
```
# Add comment on secondary location ip is reported to
ACCESS_TOKEN+=("********************")
```