#include "common.h"
#include <sys/stat.h>
#include "HttpProtocol.h"

char *CHttpProtocol::pass=(char*)PASSWORD;
CHttpProtocol::CHttpProtocol(void)
{
	bio_err=0;
	m_strRootDir=(char*)"../resource"; //资源文件的路径
	ErrorMsg=(char*)"";
    //创建上下文环境
  	ErrorMsg=initialize_ctx();
	if(ErrorMsg==(char*)"")
	{
		ErrorMsg=load_dh_params(ctx, (char*)ROOTKEYPEM);
	}
	else
	printf("%s \n",ErrorMsg);
}

CHttpProtocol::~CHttpProtocol(void)
{
	// 释放SSL上下文环境
	SSL_CTX_free(ctx);
}

char * CHttpProtocol::initialize_ctx()
{
    const SSL_METHOD *meth;
    
    if(!bio_err)
	{
		//初始化OpenSSL库,加载OpenSSL将会用到的算法
		SSL_library_init();
		// 加载错误字符串
		SSL_load_error_strings();	
		// An error write context 
		bio_err = BIO_new_fp(stderr, BIO_NOCLOSE);
    }
	else
	{
		return (char*)"initialize_ctx() error!";
	}
    
    // Create our context
    meth = SSLv23_method();
	//meth = SSLv23_server_method();
    ctx = SSL_CTX_new(meth);

    //指定所使用的证书文件
    if(!(SSL_CTX_use_certificate_chain_file(ctx, SERVERPEM)))
	{
		char * Str = (char*)"SSL_CTX_use_certificate_chain_file error!";
		return Str;
	}

	// 设置密码回调函数
    SSL_CTX_set_default_passwd_cb(ctx, password_cb);

	// 加载私钥文件
    if(!(SSL_CTX_use_PrivateKey_file(ctx, SERVERKEYPEM, SSL_FILETYPE_PEM)))
	{
		char * Str = (char*)"SSL_CTX_use_PrivateKey_file error!";
		return Str;
	}

    // 加载受信任的CA证书
    if(!(SSL_CTX_load_verify_locations(ctx, ROOTCERTPEM, 0)))
	{
		char * Str = (char*)"SSL_CTX_load_verify_locations error!";
		return Str;
	}
	return (char*)"";
}

char * CHttpProtocol::load_dh_params(SSL_CTX *ctx, char *file)
{
    DH *ret = 0;
    BIO *bio;

    if ((bio = BIO_new_file(file,"r")) == NULL)
	{
		char * Str = (char*)"BIO_new_file error!";
		return Str;
	}

    ret = PEM_read_bio_DHparams(bio, NULL, NULL, NULL);
    BIO_free(bio);
    /*
    if(SSL_CTX_set_tmp_dh(ctx, ret) < 0)
	{
		char * Str = (char*)"SSL_CTX_set_tmp_dh error!";
		return Str;
	}
	*/
	return (char*)"";
}

int CHttpProtocol::password_cb(char *buf, int num, int rwflag, void *userdata)
{ 
    if((unsigned int)num < strlen(pass)+1)
	{
		return(0);
	}

    strcpy(buf, pass);
    return(strlen(pass));
}

void CHttpProtocol::err_exit(char * str)
{
	printf("%s \n",str);
	exit(1);
}

void CHttpProtocol::Disconnect(PREQUEST pReq)
{
	// 关闭套接字：释放所占有的资源
	int	nRet;
	printf("Closing socket! \r\n");
	
	nRet = close(pReq->Socket);
	if (nRet == SOCKET_ERROR)
	{
		// 处理错误
		printf("Closing socket error! \r\n");
	}

//	HTTPSTATS	stats;
//	stats.dwRecv = pReq->dwRecv;
//	stats.dwSend = pReq->dwSend;
//	SendMessage(m_hwndDlg, DATA_MSG, (UINT)&stats, NULL);
}

void CHttpProtocol::CreateTypeMap()
{
	// 初始化map字典
    m_typeMap[(char*)".doc"]	= (char*)"application/msword";
	m_typeMap[(char*)".bin"]	= (char*)"application/octet-stream";
	m_typeMap[(char*)".dll"]	= (char*)"application/octet-stream";
	m_typeMap[(char*)".exe"]	= (char*)"application/octet-stream";
	m_typeMap[(char*)".pdf"]	= (char*)"application/pdf";
	m_typeMap[(char*)".ai"]	= (char*)"application/postscript";
	m_typeMap[(char*)".eps"]	= (char*)"application/postscript";
	m_typeMap[(char*)".ps"]	= (char*)"application/postscript";
	m_typeMap[(char*)".rtf"]	= (char*)"application/rtf";
	m_typeMap[(char*)".fdf"]	= (char*)"application/vnd.fdf";
	m_typeMap[(char*)".arj"]	= (char*)"application/x-arj";
	m_typeMap[(char*)".gz"]	= (char*)"application/x-gzip";
	m_typeMap[(char*)".class"]	= (char*)"application/x-java-class";
	m_typeMap[(char*)".js"]	= (char*)"application/x-javascript";
	m_typeMap[(char*)".lzh"]	= (char*)"application/x-lzh";
	m_typeMap[(char*)".lnk"]	= (char*)"application/x-ms-shortcut";
	m_typeMap[(char*)".tar"]	= (char*)"application/x-tar";
	m_typeMap[(char*)".hlp"]	= (char*)"application/x-winhelp";
	m_typeMap[(char*)".cert"]	= (char*)"application/x-x509-ca-cert";
	m_typeMap[(char*)".zip"]	= (char*)"application/zip";
	m_typeMap[(char*)".cab"]	= (char*)"application/x-compressed";
	m_typeMap[(char*)".arj"]	= (char*)"application/x-compressed";
	m_typeMap[(char*)".aif"]	= (char*)"audio/aiff";
	m_typeMap[(char*)".aifc"]	= (char*)"audio/aiff";
	m_typeMap[(char*)".aiff"]	= (char*)"audio/aiff";
	m_typeMap[(char*)".au"]	= (char*)"audio/basic";
	m_typeMap[(char*)".snd"]	= (char*)"audio/basic";
	m_typeMap[(char*)".mid"]	= (char*)"audio/midi";
	m_typeMap[(char*)".rmi"]	= (char*)"audio/midi";
	m_typeMap[(char*)".mp3"]	= (char*)"audio/mpeg";
	m_typeMap[(char*)".vox"]	= (char*)"audio/voxware";
	m_typeMap[(char*)".wav"]	= (char*)"audio/wav";
	m_typeMap[(char*)".ra"]	= (char*)"audio/x-pn-realaudio";
	m_typeMap[(char*)".ram"]	= (char*)"audio/x-pn-realaudio";
	m_typeMap[(char*)".bmp"]	= (char*)"image/bmp";
	m_typeMap[(char*)".gif"]	= (char*)"image/gif";
	m_typeMap[(char*)".jpeg"]	= (char*)"image/jpeg";
	m_typeMap[(char*)".jpg"]	= (char*)"image/jpeg";
	m_typeMap[(char*)".tif"]	= (char*)"image/tiff";
	m_typeMap[(char*)".tiff"]	= (char*)"image/tiff";
	m_typeMap[(char*)".xbm"]	= (char*)"image/xbm";
	m_typeMap[(char*)".wrl"]	= (char*)"model/vrml";
	m_typeMap[(char*)".htm"]	= (char*)"text/html";
	m_typeMap[(char*)".html"]	= (char*)"text/html";
	m_typeMap[(char*)".c"]		= (char*)"text/plain";
	m_typeMap[(char*)".cpp"]	= (char*)"text/plain";
	m_typeMap[(char*)".def"]	= (char*)"text/plain";
	m_typeMap[(char*)".h"]		= (char*)"text/plain";
	m_typeMap[(char*)".txt"]	= (char*)"text/plain";
	m_typeMap[(char*)".rtx"]	= (char*)"text/richtext";
	m_typeMap[(char*)".rtf"]	= (char*)"text/richtext";
	m_typeMap[(char*)".java"]	= (char*)"text/x-java-source";
	m_typeMap[(char*)".css"]	= (char*)"text/css";
	m_typeMap[(char*)".mpeg"]	= (char*)"video/mpeg";
	m_typeMap[(char*)".mpg"]	= (char*)"video/mpeg";
	m_typeMap[(char*)".mpe"]	= (char*)"video/mpeg";
	m_typeMap[(char*)".avi"]	= (char*)"video/msvideo";
	m_typeMap[(char*)".mov"]	= (char*)"video/quicktime";
	m_typeMap[(char*)".qt"]		= (char*)"video/quicktime";
	m_typeMap[(char*)".shtml"]	= (char*)"wwwserver/html-ssi";
	m_typeMap[(char*)".asa"]	= (char*)"wwwserver/isapi";
	m_typeMap[(char*)".asp"]	= (char*)"wwwserver/isapi";
	m_typeMap[(char*)".cfm"]	= (char*)"wwwserver/isapi";
	m_typeMap[(char*)".dbm"]	= (char*)"wwwserver/isapi";
	m_typeMap[(char*)".isa"]	= (char*)"wwwserver/isapi";
	m_typeMap[(char*)".plx"]	= (char*)"wwwserver/isapi";
	m_typeMap[(char*)".url"]	= (char*)"wwwserver/isapi";
	m_typeMap[(char*)".cgi"]	= (char*)"wwwserver/isapi";
	m_typeMap[(char*)".php"]	= (char*)"wwwserver/isapi";
	m_typeMap[(char*)".wcgi"]	= (char*)"wwwserver/isapi";

}

int CHttpProtocol::TcpListen()
{
	int sock;
    struct sockaddr_in sin;
    
    if((sock=socket(PF_INET,SOCK_STREAM,0))<0) // 设置套接字协议族等信息
    	err_exit((char*)"Couldn't make socket");
    
    memset(&sin,0,sizeof(sin));
    sin.sin_addr.s_addr=INADDR_ANY;            
    sin.sin_family=PF_INET;
    sin.sin_port=htons(8000);                  // 设置访问端口为本地8000
    
    if(bind(sock,(struct sockaddr *)&sin, sizeof(struct sockaddr))<0) // 绑定套接字
    	err_exit((char*)"Couldn't bind");
    listen(sock,5);                           // 设置队列
	//printf("TcpListen Ok\n");

    return sock;
}

bool isdigit(char x) {
	return x >= '0' && x <= '9';
}

int CHttpProtocol::SSLRecvRequest(SSL *ssl,BIO *io, LPBYTE pBuf, DWORD dwBufSize)
{
	//printf("SSLRecvRequest \n");
	char buf[BUFSIZZ];
    int r, length=0;

	memset(buf, 0, BUFSIZZ);	//初始化缓冲区
	while(1)
	{
		r = BIO_gets(io, buf, BUFSIZZ-1);
		//printf("r = %d\r\n",r);
		switch(SSL_get_error(ssl, r))
		{
			case SSL_ERROR_NONE:
				memcpy(&pBuf[length], buf, r);
				// printf("%s\n", buf);
				length += r;
				//printf("Case 1... \r\n");
				break;
			default:
				//printf("Case 2... \r\n");
				break;
		}
		// 直到读到代表HTTP头部结束的空行
		if(!strcmp(buf,"\r\n") || !strcmp(buf,"\n"))
		{
			// 如果为POST类型报文，则会继续读完后边的报文体
			if(pBuf[0] == 'P' && pBuf[1] == 'O' && pBuf[2] == 'S' && pBuf[3] == 'T') {
				
				// printf("GET POST request!\n");
				char *str_p = strstr((char *)pBuf, "Content-Length: ");
				int pos = str_p - (char *)pBuf;
				pos = pos + 16;
				int data_length = 0;
				while(isdigit(pBuf[pos])) {
					data_length = data_length * 10 + pBuf[pos] - '0';
					pos++;
				}
				// printf("%d\n", data_length);
				
				while(data_length > 0) {
					r = BIO_gets(io, buf, data_length + 1);
					switch(SSL_get_error(ssl, r)) {
						case SSL_ERROR_NONE:
							memcpy(&pBuf[length], buf, r);
							// printf("%s\n", buf);
							length += r;
							data_length -= r;
							break;
						default:
							break;
					}
				}
				// printf("GET POST end!\n");
			}
			printf("IF...\r\n");
			break;
		}
  }
	// 添加结束符
	pBuf[length] = '\0';
	return length;
}
bool CHttpProtocol::StartHttpSrv()
{
	CreateTypeMap();
	
	printf("*******************Server starts************************ \n");
	
	pid_t pid;
	m_listenSocket = TcpListen();          // 设置监听进程，负责处理请求

	pid = fork();
	if (pid < 0) printf("ERROR: fork error!\n");
	else if (pid == 0) {
		ListenThread(this);
	}
	
	// pthread_t listen_tid;
	// pthread_create(&listen_tid,NULL,&ListenThread,this);	// 创建线程运行ListenThread函数
}

void * CHttpProtocol::ListenThread(LPVOID param)
{
	printf("Starting ListenThread... \n");
	
	CHttpProtocol *pHttpProtocol = (CHttpProtocol *)param;

	SOCKET		socketClient;
	pthread_t	client_tid;
	struct sockaddr_in	SockAddr;
	PREQUEST	pReq;
	socklen_t	nLen;
	DWORD		dwRet;

	while(1)	// 循环等待用户连接请求
	{	
		//printf("while!\n");
		nLen = sizeof(SockAddr);		
		// 套接字等待连接，返回已接受的客户机连接的套接字
		socketClient = accept(pHttpProtocol->m_listenSocket, (LPSOCKADDR)&SockAddr, &nLen);
		//printf("%s ",inet_ntoa(SockAddr.sin_addr));
		if (socketClient == INVALID_SOCKET)
		{  
			printf("INVALID_SOCKET !\n");
			break;
		}		
		pReq = new REQUEST;
		//pReq->hExit  = pHttpProtocol->m_hExit;
		pReq->Socket = socketClient;
		pReq->hFile = -1;
		pReq->dwRecv = 0;
		pReq->dwSend = 0;
		pReq->pHttpProtocol = pHttpProtocol;
		pReq->ssl_ctx=pHttpProtocol->ctx;

	    // 创建client进程处理request
		//printf("New request");
		pid_t pid;
		pid = fork();
		if (pid < 0) printf("ERROR: fork error!\n");
		else if (pid == 0) {
			ClientThread(pReq);
		}
	} //while

		return NULL;
}
	
void * CHttpProtocol::ClientThread(LPVOID param)
{
	printf("Starting ClientThread... \n");
	int nRet;
	SSL *ssl;
	BYTE buf[8196];
	BIO *sbio,*io, *ssl_bio;
	PREQUEST pReq = (PREQUEST)param;
	CHttpProtocol *pHttpProtocol = (CHttpProtocol *)pReq->pHttpProtocol;
	//pHttpProtocol->CountUp();				// 计数
	SOCKET s = pReq->Socket;
	
	sbio = BIO_new_socket(s, BIO_NOCLOSE);	// 创建一个socket类型的BIO对象
	ssl=SSL_new(pReq->ssl_ctx);				// 创建一个SSL对象
  	SSL_set_bio(ssl, sbio, sbio);			// 把SSL对象绑定到socket类型的BIO上
    nRet = SSL_accept(ssl);					// 连接客户端
	printf("SSL_accept return: %d\n", nRet);
	if(nRet == -1) {
		printf("SSL_error: %d\n", SSL_get_error(ssl, nRet));
	}
    if(nRet <= 0)
		{
			//pHttpProtocol->err_exit((char*)"SSL_accept()error! \r\n");
			return 0;
		}
		
    io = BIO_new(BIO_f_buffer());			//封装了缓冲区操作的BIO，写入该接口的数据一般是准备传
											//入下一个BIO接口的，从该接口读出的数据一般也是从另一
											//个BIO传过来的。
    ssl_bio = BIO_new(BIO_f_ssl());			//封装了openssl 的SSL协议的BIO类型，也就是为SSL协议增
											//加了一些BIO操作方法。
    BIO_set_ssl(ssl_bio, ssl, BIO_CLOSE);	// 把ssl(SSL对象)封装在ssl_bio(SSL_BIO对象)中
    BIO_push(io, ssl_bio);					// 把ssl_bio封装在一个缓冲的BIO对象中，这种方法允许
											// 我们使用BIO_*函数族来操作新类型的IO对象,从而实现对SSL连接的缓冲读和写 
	
	// 接受request data
	printf("****************\r\n");
	int msgLen = 0;
	if ((msgLen = pHttpProtocol->SSLRecvRequest(ssl,io,buf,sizeof(buf))) < 0)
	{
		pHttpProtocol->err_exit((char*)"Receiving SSLRequest error!! \r\n");
	}
	else
	{
			printf("Request received!! lenght: %d\n", msgLen);
			printf("%s \n", buf);		
			//return 0;								
	}
	if (msgLen > 0) {
		// 将接收到的请求，发送给后台web服务器
		pHttpProtocol->MsgTrans(pHttpProtocol, ssl, io, buf, msgLen);
	}
	/*
	nRet = pHttpProtocol->Analyze(pReq, buf);
	if (nRet)
	{	
		pHttpProtocol->Disconnect(pReq);
		delete pReq;
		pHttpProtocol->err_exit((char*)"Analyzing request from client error!!\r\n");
	}

	// 生成并发送头部
	if(!pHttpProtocol->SSLSendHeader(pReq,io))
	{
		pHttpProtocol->err_exit((char*)"Sending fileheader error!\r\n");
	}
	BIO_flush(io);

	// 向client传送数据
	if(pReq->nMethod == METHOD_GET)
	{
		printf("Sending..............................\n");
		if(!pHttpProtocol->SSLSendFile(pReq,io))
		{
			return 0;
		}
	}
	printf("File sent!!");
	*/
	//pHttpProtocol->Test(pReq);
	pHttpProtocol->Disconnect(pReq);
	delete pReq;
	SSL_free(ssl);
	return NULL;
}

// 用于与后台Web服务器交互
void CHttpProtocol::MsgTrans(CHttpProtocol *pHttpProtocol, SSL *ssl, BIO *io, unsigned char *msgBuf, int msgLen) {
	int skfd;
	unsigned char buf[8196];
	struct sockaddr_in sockAddr;
	
	printf("Starting connecting to webserver!\n");
	
	if ((skfd = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
		printf("ERROR: webserver socket error!\n");
		return;
	}
	
	memset(&sockAddr, 0, sizeof(sockaddr_in));
	sockAddr.sin_family = AF_INET;
	sockAddr.sin_addr.s_addr = inet_addr("0.0.0.0");
	sockAddr.sin_port = htons(HTTPPORT);
	// 与Web服务器建立TCP连接
	if(connect(skfd, (struct sockaddr *)(&sockAddr), sizeof(sockaddr))) {
		printf("ERROR: webserver connect error!\n");
		close(skfd);
		return;
	}
	
	// 发送请求报文
	unsigned int size = 0, nodeSize = 0, msize = 0;
	while(size < msgLen) {
		if( (nodeSize = write(skfd, msgBuf + size, msgLen - size)) < 0) {
			printf("ERROR: webserver sending error!\n");
			close(skfd);
			return;
		}
		size += nodeSize;
	}
	
	
	printf("OK: finished sending to webserver!\n");
	
	
	// 接收Web服务器的相应，并转发会浏览器
	// bool flag = true;
	while(memset(buf, 0, sizeof(buf)), (msize = read(skfd, buf, sizeof(buf) - 5)) > 0) {
		size = 0;
		{
			// printf("Changing!\n");
			const char str_http[] = "Location: http://";
			char *str_p = strstr((char *)buf, str_http);
			if (str_p != NULL) {
				// printf("Changing!\n");
				int pos = str_p - (char *)buf;
				pos = pos + 14;
				for (int i = msize - 1; i >= pos; i--) {
					buf[i + 1] = buf[i];
				}
				buf[pos] = 's';
				msize += 1;
			}
			
		}
		// printf("%d\n", msize);
		while (size < msize) {
			// printf("%d\n", size);
			nodeSize = BIO_write(io, buf + size, msize - size);
			if (nodeSize <= 0) {
				if (!BIO_should_retry(io)) {
					printf("ERROR: BIO_write() error!\n");
					close(skfd);
					return;
				}
			}
			BIO_flush(io);
			size += nodeSize;
			// printf("%d\n", size);
		}
	}
	printf("OK: finished receive from webserver!\n");
	
	close(skfd);	
}

int  CHttpProtocol::Analyze(PREQUEST pReq, LPBYTE pBuf)
{
	// 分析收到的信息
	char szSeps[] = " \n";
	char *cpToken;
	// 防止非法请求
	if (strstr((const char *)pBuf, "..") != NULL)
	{
		strcpy(pReq->StatuCodeReason, HTTP_STATUS_BADREQUEST);
		return 1;
	}

	// 判断ruquest的mothed	
	cpToken = strtok((char *)pBuf, szSeps);	// 缓存中的信息切割
	if (!strcmp(cpToken, "GET"))			// GET命令
	{
		pReq->nMethod = METHOD_GET;
	}
	else if (!strcmp(cpToken, "HEAD"))	// HEAD命令
	{
		pReq->nMethod = METHOD_HEAD;  
	}
	else  
	{
        strcpy(pReq->StatuCodeReason, HTTP_STATUS_NOTIMPLEMENTED);
		return 1;
	}

	// 获取Request-URI
	cpToken = strtok(NULL, szSeps);
	if (cpToken == NULL)   
	{
		strcpy(pReq->StatuCodeReason, HTTP_STATUS_BADREQUEST);
		return 1;
	}

	strcpy(pReq->szFileName, m_strRootDir);
	if (strlen(cpToken) > 1)
	{
		strcat(pReq->szFileName, cpToken);	// 将文件名连接到本地服务器资源文件相对路径
	}
	else
	{
		strcat(pReq->szFileName, "/index.html");
	}
	printf("%s\r\n",pReq->szFileName);
	
	return 0;
}

int CHttpProtocol::FileExist(PREQUEST pReq)
{
	pReq->hFile = open(pReq->szFileName,O_RDONLY);
	if (pReq->hFile == -1)
	{
		strcpy(pReq->StatuCodeReason, HTTP_STATUS_NOTFOUND);
		printf("open %s error\n",pReq->szFileName);
		return 0;
	}
	else 
	{
		//printf("hFile\n");
		return 1;
	}
}
void CHttpProtocol::Test(PREQUEST pReq)
{
		struct stat buf;
		long fl;
		if(stat(pReq->szFileName, &buf)<0)
		{
		   err_exit((char*)"Getting filesize error!!\r\n");
		}
		fl = buf.st_size;
		printf("Filesize = %ld \r\n",fl);
}

void CHttpProtocol::GetCurrentTime(LPSTR lpszString)
{
	char const *week[] = {"Sun,", "Mon,","Tue,","Wed,","Thu,","Fri,","Sat,",};
	char const *month[] = {"Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec",};
	struct tm *st;
	long ct;
	ct = time(&ct);
	st = (struct tm *)localtime(&ct);
    sprintf(lpszString, "%s %02d %s %d %02d:%02d:%02d GMT",week[st->tm_wday], st->tm_mday, month[st->tm_mon],
     1900+st->tm_year, st->tm_hour, st->tm_min, st->tm_sec);
}


bool CHttpProtocol::GetContentType(PREQUEST pReq, LPSTR type)
{
	// 取得文件的类型
    char * cpToken;
    cpToken = strstr(pReq->szFileName, ".");
    strcpy(pReq->postfix, cpToken);
	// 遍历搜索该文件类型对应的content-type
	map<char *, char *>::iterator it = m_typeMap.find(pReq->postfix);
	if(it != m_typeMap.end())
	{
		sprintf(type,"%s",(*it).second);
	}
	return 1;
}


bool CHttpProtocol::SSLSendHeader(PREQUEST pReq, BIO *io)
{
	char Header[2048] = " ";
	int n = FileExist(pReq);
	if(!n)		// 文件不存在
	{
    	err_exit((char*)"The file requested doesn't exist!");
	}

	char curTime[50];
	GetCurrentTime(curTime);
	// 获取文件长度
	struct stat buf;
	long length;
	if(stat(pReq->szFileName, &buf)<0)
	{
	   err_exit((char*)"Getting filesize error!!\r\n");
	}
	length = buf.st_size;
	
	// 获取文件类型
	char ContentType[50] = " ";
 	GetContentType(pReq, (char*)ContentType);

	sprintf((char*)Header, "HTTP/1.1 %s\r\nDate: %s\r\nServer: %s\r\nContent-Type: %s\r\nContent-Length: %ld\r\n\r\n",
			                    HTTP_STATUS_OK, 
								curTime,				// Date
								"Villa Server 192.168.1.49",      // Server"My Https Server"
								ContentType,				// Content-Type
								length);					// Content-length
								
	//if(BIO_puts(io, Header) <= 0)
	if(BIO_write(io, Header,strlen(Header)) <= 0)
	{
		return false;
	}
	BIO_flush(io);
	printf("SSLSendHeader successfully!\n");
	return true;
}


bool CHttpProtocol::SSLSendFile(PREQUEST pReq, BIO *io)
{
	//printf("%s\n",pReq->szFileName);
	int n = FileExist(pReq);
	// 判断文件是否存在
	if(!n)			
	{
		err_exit((char*)"The file requested doesn't exist!");
	}

	static char buf[2048];
    DWORD  dwRead;
    BOOL   fRet;
	int flag = 1,nReq;
    // 读取文件直到结束
    while(1)
	{	
		// 从file中读到buffer中去        
		fRet = read(pReq->hFile, buf, sizeof(buf));
		//printf("%d,%d\n",fRet,pReq->hFile);
		if (fRet<0)
		{
			//printf("!fRet\n");
	    	static char szMsg[512];
		    sprintf(szMsg, "%s", HTTP_STATUS_SERVERERROR);
			//if((nReq = BIO_puts(io, szMsg)) <= 0)
			if((nReq = BIO_write(io, szMsg,strlen(szMsg))) <= 0)
			{
				err_exit((char*)"BIO_write() error!\n");
			}
			BIO_flush(io);
	    	break;
		}
		
		// 完成
		if (fRet == 0)
		{	
			printf("complete \n");
			break;
		}
		// 将buffer中得到内容传给Client
		//if(BIO_puts(io, buf) <= 0)
		if(BIO_write(io, buf, fRet) <= 0)
		{
			if(! BIO_should_retry(io))
			{
				printf("BIO_write() error!\r\n");
				break;
			}
		}
		BIO_flush(io);
		// 统计发送流量
		pReq->dwSend+=fRet;
	}
    // 关闭文件
	if (close(pReq->hFile)==0)
	{
		pReq->hFile = -1;
		return true;
	}
	else
	{
		err_exit((char*)"Closing file error!");
	}
}
