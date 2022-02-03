import os
import time
from ItsAGramLive import ItsAGramLive
import subprocess

# CONFIG 
CHANNEL_ID="" # GET IT ON: https://www.youtube.com/account_advanced
INSTAGRAM_USERNAME=""
INSTAGRAM_PASSWORD=""
SLEEP_TIME=5 # TIMEOUT AFTER TRY

# DETECT IF CHANNEL IS LIVE
cmd_check_is_live = 'streamlink https://www.youtube.com/channel/' + CHANNEL_ID + '/live'
cmd_check_is_live_return = 1

while cmd_check_is_live_return != 0 : # LOOP UNTIL THERE'S SOMETHING LIVE

    cmd_check_is_live_return = os.system(cmd_check_is_live)

    if cmd_check_is_live_return == 0 : 
        print("CHANNEL IS LIVE. STARTING RESTRAMING")
        
        # DOWNLOAD LIVE
        live_link = "https://www.youtube.com/channel/" + CHANNEL_ID + "/live"
        cmd_to_download_video = "streamlink " + live_link + " best -o live.mp4"

        process = subprocess.Popen(['streamlink', live_link, 'best', '-o', 'live.mp4'], 
                                stdout=subprocess.PIPE,
                                universal_newlines=True)
        time.sleep(5) # WAIT A LITTLE BIT. SHOULD IMPROVE THIS CODE
        # START INSTAGRAM_LIVE
        # quit()
        live = ItsAGramLive(
            username=INSTAGRAM_USERNAME,
            password=INSTAGRAM_PASSWORD
        )

        if live.login():  
            print("You'r logged in")  
        
            if live.create_broadcast():  
        
                if live.start_broadcast():
                    # STREAM TO INSTAGRAM
                    ffmpeg_cmd = 'ffmpeg ' \
                                '-re -nostdin -i "' + os.path.join(os.getcwd(), 'live.mp4') + '" ' \
                                '-vcodec libx264 -preset:v ultrafast ' \
                                '-acodec aac ' \
                                '-vf "transpose=clock" ' \
                                '-f flv "' + live.stream_server + live.stream_key + '"'
        
                    print('CTRL+C to quit.')  
                    try:  
                        subprocess.call(ffmpeg_cmd, shell=True)  
                    except KeyboardInterrupt:  
                        pass  
                    except Exception as error:  
                        print(error)  
                        live.end_broadcast()  
        
                    live.end_broadcast()
    time.sleep(SLEEP_TIME)
