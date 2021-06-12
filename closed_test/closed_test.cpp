
#include <stdio.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <netdb.h>
#include <string.h>
#include <iostream>
#include <fstream>
#include <unistd.h>

int main(int argc, char *argv[])
{
 struct sockaddr_in server;
 int sock;
 char buf[10000];
 char *deststr;
 unsigned int **addrptr;

 if (argc != 4) {
	 printf("Usage : %s dest v delta\n", argv[0]);
	 return 1;
 }
 deststr = argv[1];

 const double v     = std::stod(argv[2]); //10
 const double delta = std::stod(argv[3]); //0.01
 const double dt    = 0.1;


 double x = 0.0;
 double y = 0.0;
 double head = 0.0;
 for(int i=0;i<100;i++) {

	sock = socket(AF_INET, SOCK_STREAM, 0);
	if (sock < 0) {
		perror("socket");
		return 1;
	}

	server.sin_family = AF_INET;
	server.sin_port = htons(8000); /* HTTPのポートは80番です */

	server.sin_addr.s_addr = inet_addr(deststr);
	if (server.sin_addr.s_addr == 0xffffffff) {
		struct hostent *host;

		host = gethostbyname(deststr);
		if (host == NULL) {
			if (h_errno == HOST_NOT_FOUND) {
				/* h_errnoはexternで宣言されています */
				printf("host not found : %s\n", deststr);
			} else {
				/*
				HOST_NOT_FOUNDだけ特別扱いする必要はないですが、
				とりあえず例として分けてみました
				*/
				printf("%s : %s\n", hstrerror(h_errno), deststr);
			}
			return 1;
		}

		addrptr = (unsigned int **)host->h_addr_list;

		while (*addrptr != NULL) {
			server.sin_addr.s_addr = *(*addrptr);

			/* connect()が成功したらloopを抜けます */
			if (connect(sock,
					(struct sockaddr *)&server,
					sizeof(server)) == 0) {
				break;
			}

			addrptr++;
			/* connectが失敗したら次のアドレスで試します */
		}

		/* connectが全て失敗した場合 */
		if (*addrptr == NULL) {
			perror("connect");
			return 1;
		}
	} else {
		if (connect(sock,
						(struct sockaddr *)&server, sizeof(server)) != 0) {
			perror("connect");
			return 1;
		}
	}

	/* HTTPで「/」をリクエストする文字列を生成 */
	memset(buf, 0, sizeof(buf));


		snprintf(buf, sizeof(buf), "GET /calc?x=%lf&y=%lf&head=%lf&v=%lf&delta=%lf HTTP/1.0\r\n\r\n",x,y,head,v,delta);

		/* HTTPリクエスト送信 */
		int n = write(sock, buf, (int)strlen(buf));
	
		if (n < 0) {
			perror("write");
			return 1;
		}

		/* サーバからのHTTPメッセージ受信 */
		while (n > 0) {
			memset(buf, 0, sizeof(buf));
			n = read(sock, buf, sizeof(buf));
			if (n < 0) {
				perror("read");
				return 1;
			}

			break;
		}
		
		char * tp;
		tp = strtok( buf, "$" );

		int count = 0;
		char x_str[1000],y_str[1000],head_str[1000];
		for(int count=0;count<3;count++) {
			tp = strtok( NULL,"$" );

			strcpy(x_str, tp); 

			if(count==0) strcpy(x_str, tp); 
			if(count==1) strcpy(y_str, tp); 
			if(count==2) strcpy(head_str, tp); 
		
		}
		
		double dx_dt    = static_cast<double>(atof(x_str));
		double dy_dt    = static_cast<double>(atof(y_str));
		double dhead_dt = static_cast<double>(atof(head_str));
		x    = x    +dt*dx_dt;
		y    = y    +dt*dy_dt;
		head = head +dt*dhead_dt;

		close(sock);
	}
	// v=10,delta=0.01 の時の計算結果
	const double _x = 0.333333;
	const double _y = 16.84;

	double loss = (x-_x)*(x-_x) + (y-_y)*(y-_y);
	std::cout << loss << std::endl;
 return 0;
}