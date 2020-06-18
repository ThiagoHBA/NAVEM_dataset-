#include<iostream>
#include<string>
#include <string.h>
#include <stdint.h>
#include <stdlib.h>
#include"SerialPort.h"
#include <Windows.h>
#include <vector>
#include <chrono>
#include <fstream>


//#pragma warning(disable:4996)

using namespace std;
using namespace chrono;

char output[MAX_DATA_LENGTH];
char output2[MAX_DATA_LENGTH];
char incomingData[MAX_DATA_LENGTH];

char commport[] = "\\\\.\\COM4";
char* port = commport;
char nsei[1] = { 'oi' };
char* teste;
int i = 0;

int ChamadaArduino() {
	ofstream myfile;
	myfile.open("C:/Users/thiag/Desktop/ldr/DadosCount.txt");

	int quantidadeDados = 100;
	double tempos[100];

	SerialPort arduino(port);

	if (arduino.isConnected()) {
		cout << "Connection made" << endl;
	}
	else {
		cout << "Error in port name" << endl;
	}

	for (int j = 0; j < MAX_DATA_LENGTH; j++) {
		output[j] = '\0';
	}

	if (myfile.is_open()) {
		myfile << "{";
		myfile << "\"Dados\"";
		myfile << ": [\n";
	}

	while (arduino.isConnected()) {
		if (i == quantidadeDados) {
			myfile << "}\n";
			myfile << "]\n";
			myfile << "}";
			break;
		}

		auto start = std::chrono::high_resolution_clock::now();
		char* charArray = nsei;

		arduino.writeSerialPort(charArray, 1);
		for (int j = 0; j < MAX_DATA_LENGTH; j++) {
			output[j] = '\0';
		}

		Sleep(98);
		arduino.readSerialPort(output, MAX_DATA_LENGTH);

		if (output[0] == '\0' && output[41] == '\0') {
			cout << "deu errado!" << endl;
			Sleep(1);
		}

		if (i == 0) {
			for (int j = 0; j < MAX_DATA_LENGTH; j++) {
				output[j] = '\0';
			}

			auto stop = std::chrono::high_resolution_clock::now();
			double elapsedTime = std::chrono::duration_cast<std::chrono::microseconds>(stop - start).count();
			tempos[i] = elapsedTime;
			i++;
			continue;
		}

		if (output[2] != '.') {
			myfile << "{";
			myfile << "i:" + to_string(i) + '\n';
			myfile << "FALHA!!\n";
			myfile << "},\n";
			auto stop = std::chrono::high_resolution_clock::now();
			double elapsedTime = std::chrono::duration_cast<std::chrono::microseconds>(stop - start).count();

			tempos[i] = elapsedTime;
			cout << output << endl;
			i++;
			continue;
		}

		myfile << "{";
		myfile << "i:" + to_string(i) + '\n';
		cout << i << endl;

		myfile << "\"AccX\":" + string("\"") + output[0] + output[1] + output[2] + output[3] + output[4]
			+ output[5] + output[6] + "\"" + "\n";

		myfile << "\"AccY\":" + string("\"") + output[7] + output[8] + output[9] + output[10] + output[11]
			+ output[12] + output[13] + "\"" + "\n";

		myfile << "\"AccZ\":" + string("\"") + output[14] + output[15] + output[16] + output[17] + output[18]
			+ output[19] + output[20] + "\"" + "\n";

		myfile << "\"GyrX\":" + string("\"") + output[21] + output[22] + output[23] + output[24] + output[25]
			+ output[26] + output[27] + "\"" + "\n";

		myfile << "\"GyrY\":" + string("\"") + output[28] + output[29] + output[30] + output[31] + output[32]
			+ output[33] + output[34] + "\"" + "\n";

		myfile << "\"GyrZ\":" + string("\"") + output[35] + output[36] + output[37] + output[38] + output[39]
			+ output[40] + output[41] + string("\"") + "\n";

		if (i < quantidadeDados - 1) myfile << "},\n";

		auto stop = std::chrono::high_resolution_clock::now();
		double elapsedTime = std::chrono::duration_cast<std::chrono::microseconds>(stop - start).count();
		tempos[i] = elapsedTime;
		i++;
	}
	myfile.close();

	ofstream fileTempos;
	fileTempos.open("C:/Users/thiag/Desktop/ldr/Tempos_ArduinoPC.txt");

	if (fileTempos.is_open()) {
		fileTempos << "{";
		fileTempos << "\"Dados\"";
		fileTempos << ": [\n";
	}

	for (int i = 0; i < quantidadeDados; i++) {

		if (i == quantidadeDados) {
			fileTempos << "}\n";
			fileTempos << "]\n";
			fileTempos << "}";
			break;
		}

		fileTempos << "\"i\":" + string("\"") + to_string(i) + "\"" + "\n";
		fileTempos << "\"Tempo\":" + string("\"") + to_string(tempos[i]) + "\"" + "\n";

		if (i < quantidadeDados - 1)	fileTempos << "},\n";
	}

	cout << "fim" << endl;
	fileTempos.close();
	return 0;
}
