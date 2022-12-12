from struct import unpack
import time

class RTPDatagram:
    '''
    RTP protocol datagram parser
    Based on github.com/plazmer/pyrtsp with minor cosmetic changes
    '''

    #def __init__(self, datagram):
    def __init__(self):
        self.version = 0
        self.padding = 0
        self.extension = 0
        self.csrc_count = 0
        self.marker = 0
        self.payload_type = 0
        self.sequence_number = 0
        self.timestamp = 0
        self.sync_source_id = 0
        self.csrs = []
        self.extension_header = b''
        self.extension_header_id = 0
        self.extension_header_len = 0
        self.payload = b''
        self.t0 = 0
        self.t1 = 0
        self.first_frame = 0
        self.seq0 = 0
        self.seq1 = 0
        self.is_idr_frame = 0
        #self.datagram = datagram
    '''
    @property
    def datagram(self):
        return self.__datagram
    '''
    #@datagram.setter
    def datagram(self, data):
        ver_p_x_cc, m_pt, self.sequence_number, self.timestamp, self.sync_source_id = unpack('!BBHII', data[:12])
        self.version =     (ver_p_x_cc & 0b11000000) >> 6
        self.padding =     (ver_p_x_cc & 0b00100000) >> 5
        self.extension =   (ver_p_x_cc & 0b00010000) >> 4
        self.csrc_count =   ver_p_x_cc & 0b00001111
        self.marker =      (m_pt & 0b10000000) >> 7
        self.payload_type = m_pt & 0b01111111

        '''
        now = time.time()
        sec = int(now)
        msec = int((now - sec) * 1000)
        diff = msec - self.timestamp
        print("diff=%d|local ms=%ld|remote ms=%ld" %(diff, msec, self.timestamp))
        '''

        i = 0
        for i in range(0, self.csrc_count, 4):
            self.csrc.append(unpack('!I', d[12+i:16+i]))

        if self.extension:
            i = self.csrc_count * 4
            (self.extension_header_id, self.extension_header_len) = unpack('!HH', data[12+i:16+i])
            self.extension_header = data[16+i:16+i+self.extension_header_len]
            i += 4 + self.extension_header_length

        self.payload = data[12+i:]
        self.__datagram = data

        if self.payload[0:7].hex() == '1c800000016764':
            self.is_idr_frame = 1
            #print(self.payload[0:7].hex())

        if self.is_idr_frame == 1:
            if self.marker == 0:
                if self.first_frame == 0:
                    self.first_frame = 1
                    self.t0 = time.time()
                    self.seq0 = self.sequence_number
            else:
                self.is_idr_frame = 0
                self.first_frame = 0
                self.t1 = time.time()
                self.seq1 = self.sequence_number

            if self.marker == 1:
                print("delay=%d|t0=%f|t1=%f|count=%ld" %(self.t1*1000 - self.t0*1000, self.t0, self.t1, self.seq1-self.seq0))
                #print("delay=%d|count=%ld" %(self.t1*1000 - self.t0*1000, self.seq1-self.seq0))
                #print("%d,%d" %(self.t1*1000 - self.t0*1000, self.seq1-self.seq0))
