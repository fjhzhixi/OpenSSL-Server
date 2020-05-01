#include "common.h"

#include <map>
using namespace std;

class CHttpProtocol
{
public:
	char * ErrorMsg;				// 判断是否初始化过程中出错的消息
	SOCKET m_listenSocket;			// 监听套接字
	map<char *, char *> m_typeMap;	// 保存content-type和文件后缀的对应关系的map
	HANDLE m_hExit;

	char * m_strRootDir;			// web资源文件的根目录
	UINT	m_nPort;				// http server的端口号

	BIO *bio_err;
	static char * pass;
	SSL_CTX *ctx;
	char * initialize_ctx();												// 初始化ctx
	char * load_dh_params(SSL_CTX *ctx, char *file);						// 加载ctx参数
	static int password_cb(char *buf, int num, int rwflag, void *userdata);

public:
	CHttpProtocol(void);
	int TcpListen(); 
	void err_exit(char * str);
	
	void StopHttpSrv();														// 停止http服务
	bool StartHttpSrv();													// 开始http服务

	static void * ListenThread(LPVOID param);								// 监听线程
	static void * ClientThread(LPVOID param);								// 客户线程

	bool RecvRequest(PREQUEST pReq, LPBYTE pBuf, DWORD dwBufSize);			// 接受http请求
	int Analyze(PREQUEST pReq, LPBYTE pBuf);								// 分析http请求
	void Disconnect(PREQUEST pReq);											// 断开连接
	void CreateTypeMap();													// 创建类型映射
	void SendHeader(PREQUEST pReq);											// 发送http头
	int FileExist(PREQUEST pReq);											// 判断文件是否存在
	
	void GetCurrentTime(LPSTR lpszString);									// 得到系统当前时间
	bool GetLastModified(HANDLE hFile, LPSTR lpszString);					// 得到文件的上次修改时间
	bool GetContentType(PREQUEST pReq, LPSTR type);							// 得到文件类型
	void SendFile(PREQUEST pReq);											// 发送文件
	bool SendBuffer(PREQUEST pReq, LPBYTE pBuf, DWORD dwBufSize);			// 发送缓冲区内容
public:
	int SSLRecvRequest(SSL *ssl,BIO *io, LPBYTE pBuf, DWORD dwBufSize);	// 接受https请求
	bool SSLSendHeader(PREQUEST pReq, BIO *io);								// 发送https头
	bool SSLSendFile(PREQUEST pReq, BIO *io);								// 由SSL通道发送文件
	bool SSLSendBuffer(PREQUEST pReq, LPBYTE pBuf, DWORD dwBufSize);
public:
	~CHttpProtocol(void);
	void Test(PREQUEST pReq);
	void MsgTrans(CHttpProtocol *pHttpProtocol, SSL *ssl, BIO *io, unsigned char *msgBuf, int msgLen);
};
