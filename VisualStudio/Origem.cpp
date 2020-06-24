#include <opencv2/opencv.hpp>
#include <iostream>
#include <vector>
#include <stdint.h>
#include "opencv2/highgui/highgui.hpp"
#include <string> 
#include <math.h>
#include <thread>
#include <chrono>
#include <vector>
#include <windows.h>
#include "Arduino.h"
#include "SerialPort.h"
#include <direct.h>


using namespace std;
using namespace cv;
using namespace chrono;


class Camera {

public:
	Camera();
	void SalvarFrame(string, string);
private:
	Mat frame;
	VideoCapture cap;
};

void Camera::SalvarFrame(string path, string nomeImg) {
	if (!cap.open(0))
		return;
	cap >> frame;
}

Camera::Camera() {
	cap.set(cv::CAP_PROP_FRAME_WIDTH, 1280);
	cap.set(cv::CAP_PROP_FRAME_HEIGHT, 720);
	cap.set(cv::CAP_PROP_FPS, 30);
	cap.set(cv::CAP_PROP_EXPOSURE, -7);
}

char flagSen = 0, flagCam = 0;
bool fimCamera = 0;

string dat = __DATE__;
string hora = __TIME__;

time_t t = std::time(0);   // get time now
long long int now = duration_cast<microseconds>(system_clock::now().time_since_epoch()).count();

string dir = "C:/Users/thiag/Desktop/NAVEM/VisualStudio/imagens/" + to_string(now) + "_" + to_string(now) + "_" + to_string(now) + "_" + to_string(now) + "_" + to_string(now) + "_" + to_string(now);
string path = dir + "/";


void* chamadaCamera(int z) {

	ofstream meufile;
	meufile.open(path + "/Contador de Dados.json");

	vector<Mat>frames;
	vector<float> Dados;
	vector<float>DadosAntes;

	Dados.reserve(800);
	DadosAntes.reserve(800);
	frames.reserve(100);

	VideoCapture cap(0);

	//cap.set(cv::CAP_PROP_FRAME_WIDTH, 1280);
	//cap.set(cv::CAP_PROP_FRAME_HEIGHT, 720);

	const int quantidadeFrames = 100;
	double tempos[quantidadeFrames];

	Mat frame;
	if(ColetaDeDados)Sleep(10000);

	auto iniFOR = std::chrono::high_resolution_clock::now();
	for (int j = 0; j < quantidadeFrames; j++){
		cout << j << endl;
		auto start = std::chrono::high_resolution_clock::now();
		limpaBuffer();
		if (!ColetaDeDados(j)) break;
		if (!EscritaArquivoDados(meufile, j)) break;
		int aux = cap.read(frame);
		auto stop = std::chrono::high_resolution_clock::now();
		
		double elapsedTimeFrame = std::chrono::duration_cast<std::chrono::microseconds>(stop - start).count();
		tempos[j] = elapsedTimeFrame;
		
		if (!aux) {
			cout << "deu ruim!";
			break;
		}

		frames.push_back(frame);

		if (j == 99) {
			fimCamera = 1;
		}

	}

	auto fimFOR = std::chrono::high_resolution_clock::now();
	double elapsedTimeFOR = std::chrono::duration_cast<std::chrono::microseconds>(fimFOR - iniFOR).count();
	cout << "Tempo do for em segundos:" << elapsedTimeFOR/1000000 << endl;

	int soma = 0;
	for (int i = 0; i < quantidadeFrames; i++) {
		soma += tempos[i];
	}

	cout << "Tempo medio coleta dados em micro: " << soma / quantidadeFrames << endl;

	printf("Gravando...\n");
	meufile.close();

	for (int i = 0; i < frames.size(); i++) {
		if (i < 10) {
			imwrite(path + '0' + to_string(i) + ".jpg", frames[i]);
		}
		else {
			imwrite(path + to_string(i) + ".jpg", frames[i]);
		}

	}
	for (int i = 0; i < Dados.size(); i++) {
		cout << Dados[i] << endl;

	}

	printf("Finalizou thread camera\n");
	flagCam = 1;
	return NULL;
}

int main(){
	_mkdir(dir.c_str());

	thread th1(chamadaCamera, 3);

	th1.join();

	return 0;
}