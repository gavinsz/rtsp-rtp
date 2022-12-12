#!/usr/bin/env python3

import logging
from multiprocessing import Pool

from control import RTSPClient
from transport import RTPStream


log = logging.getLogger('streamer')
log_format = '[%(asctime)s] [%(name)s] [%(levelname)s] : %(message)s'
logging.basicConfig(level=logging.INFO,format=log_format)

'''
streams = {
  'entrance': 'rtsp://username:password@10.0.0.1:554/Streaming/Channels/101',
  'kitchen':  'rtsp://username:password@10.0.0.2:554/Streaming/Channels/101',
  'hall':     'rtsp://username:password@10.0.0.3:554/Streaming/Channels/102',
  'wardrobe': 'rtsp://username:password@10.0.0.4:554/Streaming/Channels/102'
}
'''

#streams = {'local': 'rtsp://172.16.110.6:554/live'}
streams = {'local': 'rtsp://192.168.10.172:554/live'}

def save(stream):
    name, url = stream[:2]

    with RTSPClient(url) as client, RTPStream() as stream:
        log.info(f'Connected to <{name}> stream')
        client.setup(stream.port)

        log.info(f'Sending "PLAY" for <{name}>')
        client.play()

        
        log.info(f'Saving chunks for <{name}>')
        with open(f'{name}','wb') as f:
            for chunk in stream.generate():
                #f.write(chunk)
                a = 0

def main():
    pool = Pool(len(streams))
    pool.map(save,streams.items())


if __name__ == '__main__':
    main()
