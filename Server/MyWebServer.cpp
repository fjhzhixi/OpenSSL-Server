#include "common.h"
#include "HttpProtocol.h"

int main()
{
	CHttpProtocol MyHttpObj;
	MyHttpObj.StartHttpSrv();
	SSL *ssl;
	BYTE buf[4096];
	BIO *io;
	bool bRet;
	bRet = MyHttpObj.SSLRecvRequest(ssl,io,buf,sizeof(buf));
	//printf("stop1\n");
	if(!bRet)
		{
			MyHttpObj.err_exit((char*)"Receiving request error! \n");
		}
		else
			{
				printf("Request received!! \n");
				printf("%s \n",buf);
			}
  	sleep(1000);
	return 0;
}
