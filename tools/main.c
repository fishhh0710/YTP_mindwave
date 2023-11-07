#include <stdio.h>
// #include <stdlib.h>
// #include <vector>
#define SYNC 0xAA
#define EXCODE 0x55
// vector<int> v;
int opt[2000010]={-999999999};
int ti = 1;
int poor_signal = 1;
int min(int a,int b){
    if(a<b)return a;
    return b;
}
int max(int a,int b){
    if(a>b)return a;
    return b;
}
int parsePayload(unsigned char *payload, unsigned char pLength){
    unsigned char bytesParsed = 0;
    unsigned char code;
    unsigned char length;
    unsigned char extendedCodeLevel;
    int i;

    /* Loop until all bytes are parsed from the payload[] array... */
    while (bytesParsed < pLength) {
        /* Parse the extendedCodeLevel, code, and length */
        extendedCodeLevel = 0;
        while (payload[bytesParsed] == EXCODE) {
            extendedCodeLevel++;
            bytesParsed++;
        }
        code = payload[bytesParsed++];
        if (code & 0x80)
            length = payload[bytesParsed++];
        else
            length = 1;

        /* TODO: Based on the extendedCodeLevel, code, length,
        * and the [CODE] Definitions Table, handle the next
        * "length" bytes of data from the payload as
        * appropriate for your application.
        */
        if(!(code==0x02||code==0x80))continue;
        int res = 0;
        for (i = 0; i < length; i++) {
            int temp = payload[bytesParsed + i] & 0xFF;
            if((temp&(128)))temp-=256;
            // printf(" %02X ", temp);
            res*=256;
            res+=temp;
        }
        if(code==0x02){
            if(res>16){
                if(!poor_signal){
                    printf("PoorSignal\n");
                    fflush(stdout);
                }
                poor_signal = 1;
            }
            else if(res==0){
                // printf("%d !!",res);
                // return ;
                if(poor_signal){
                    printf("GreatSignal\n");
                    fflush(stdout);
                }
                poor_signal = 0;
            }
        }
        else if(code==0x80&&!poor_signal){
            // printf("EXCODE level: %d CODE: 0x%02X length: %d\n",
            //     extendedCodeLevel, code, length);
            // printf("Data value(s):");
            // printf("%d\n",res);
            if(!poor_signal){
                opt[min(ti,1000000)] = res;
                ti++;
            }
        }

        /* Increment the bytesParsed by the length of the Data Value */
        bytesParsed += length;
    }
    // printf("--------------------------------\n");
    return (0);
}

int main(int argc, char **argv) {
    int checksum;
    unsigned char payload[256];
    unsigned char pLength;
    unsigned char c;
    unsigned char i;
    int tt = 0,lasti = 0;
    /* TODO: Initialize 'stream' here to read from a serial data
    * stream, or whatever stream source is appropriate for your
    * application. See documentation for "Serial I/O" for your
    * platform for details.
    */
    FILE *stream = 0;
    stream = fopen("COM3", "r");
    int connect = 0;
    int last = 999999999;
    int cd = 0;
    /* Loop forever, parsing one Packet per loop... */
    while (ti<100000) {
        /* Synchronize on [SYNC] bytes */
        fread(&c, 1, 1, stream);
        if (c != SYNC) continue;

        fread(&c, 1, 1, stream);
        if (c != SYNC) continue;

        /* Parse [PLENGTH] byte */
        while (1) {
            fread(&pLength, 1, 1, stream);
            if( (pLength == 170) ) continue;
            break;
        }
        if (pLength > 169) continue;
        if(connect==0){
            connect = 1;
            printf("Connected\n");
            fflush(stdout);
        }
        // printf("OK\n");

        /* Collect [PAYLOAD...] bytes */
        fread(payload, 1, pLength, stream);

        /* Calculate [PAYLOAD...] checksum */
        checksum = 0;
        for (i = 0; i < pLength; i++) checksum += payload[i];
        checksum &= 0xFF;
        checksum = ~checksum & 0xFF;

        /* Parse [CKSUM] byte */
        fread(&c, 1, 1, stream);

        /* Verify [CKSUM] byte against calculated [PAYLOAD...] checksum */
        if (c != checksum) continue;

        /* Since [CKSUM] is OK, parse the Data Payload */
        parsePayload(payload, pLength);

        int mx = -100000000,mn = 100000000;
        if(lasti==ti)continue;
        for(int i=max(0,ti-10);i<=ti;i++){
            // printf("%d ",opt[i]);
            mx = max(mx,opt[i]);
            mn = min(mn,opt[i]);
        }
        if(!poor_signal&&mx-mn>490&&(double)(mx-mn)/last>1.5&&cd==0&&(double)(mx-mn)/last<30.0){
            printf("Click! %lf\n",(double)(mx-mn)/last);
            // printf()
            fflush(stdout);
            lasti = ti;
            cd = 500;
        }
        else{
            last = mx-mn;
        }
        if(cd==1){
            printf("Cd_ends\n");
            fflush(stdout);
        }
        if(cd)cd--;
    }

    return (0);
}
