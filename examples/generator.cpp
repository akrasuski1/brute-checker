#include <cstdio>
#include <cstdlib>
#include <cstring>

void generate_testcase(FILE* in,FILE* out,int cnt){
	srand(cnt);
	int a=rand()%10;
	int b=rand()%10;
	fprintf(in,"%d %d",a,b);
	fprintf(out,"%d %d %d",a,b,a+b);
}

int main(int argc,char* argv[]){
	if(argc<4){
		printf("Usage: %s testcase_number input_directory/test_name output_diectory/test_name\n",argv[0]);
		printf("Example:\n%s 23 in/test23.in out/test23.out\n",argv[0]);
		return 1;
	}
	int cnt=atoi(argv[1]);
	FILE* in=fopen(argv[2],"w+");
	if(!in){
		printf("Error opening input file\n");
		return 1;
	}
	FILE* out=fopen(argv[3],"w+");
	if(!out){
		printf("Error opening output file\n");
		return 1;
	}
	generate_testcase(in,out,cnt);
	fclose(in);
	fclose(out);
}
