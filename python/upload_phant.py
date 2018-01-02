
import time

def upload_phant(pht,parsed_data,screen_display):
    log_attempts=1
    while log_attempts<6:
        try:
            ##pht.log(iter([ parsed_data[key] for key in pht.fields]))
            # http://stackoverflow.com/questions/43414407/iterate-at-a-function-input-in-python/43414660#43414660
            pht.log(*[parsed_data[key] for key in pht.fields])
            if screen_display: print "uploaded"
            break
        except Exception, e:
            if screen_display: print "upload failed at attempt,"+str(log_attempts)+" " + str(e)
            log_attempts+=1
            time.sleep(30)
            continue
