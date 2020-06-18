#pragma once
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


using namespace std;
using namespace chrono;

char output[MAX_DATA_LENGTH];
char commport[] = "\\\\.\\COM4";
char* port = commport;
char write_array[1] = { 'oi' };
int quantidadeDados = 100;

SerialPort arduino(port);

int Conexão() {
	if (arduino.isConnected()) {
		cout << "Connection made" << endl;
		return 1;
	}
	else {
		cout << "Error in port name" << endl;
	}
	return 0;
}

void limpaBuffer() {
	for (int j = 0; j < sizeof(output); j++) {
		output[j] = '\0';
	}
}

void EscritaArquivoDados(ofstream &myfile, int i) {

	if (i == 0) {
		myfile << "{";
		myfile << "\"Dados\"";
		myfile << ": [\n";
	}

	if (output[4] && output[39] != '.') {
		cout << "virgula no lugar errado!" << endl;
	}

	int samples = 8;
	int size_char = 7*6;
	bool fim = false;

	for (int j = 0; j < samples; j++) {
		myfile << "{";
		myfile << "\"i\":" + to_string(i) + "," + '\n';

		myfile << "\"AccX\":" + string("\"") + output[0+((size_char)*j)] + output[1+((size_char)*j)] + output[2 + ((size_char)*j)] + output[3 + ((size_char)*j)] + output[4 + ((size_char)*j)]
		+ output[5 + ((size_char)*j)]  +  output[6 + ((size_char)*j)] + "\"" + "," + "\n";

		myfile << "\"AccY\":" + string("\"") + output[7 + ((size_char)*j)] + output[8 + ((size_char)*j)] + output[9 + ((size_char)*j)] + output[10 + ((size_char)*j)] + output[11 + ((size_char)*j)]
		+ output[12 + ((size_char)*j)] + output[13 + ((size_char)*j)] + "\"" + "," + "\n";

		myfile << "\"AccZ\":" + string("\"") + output[14 + ((size_char)*j)] + output[15 + ((size_char)*j)] + output[16 + ((size_char)*j)] + output[17 + ((size_char)*j)] + output[18 + ((size_char)*j)]
		+ output[19 + ((size_char)*j)] + output[20 + ((size_char)*j)] +  "\"" + "," + "\n";

		myfile << "\"GyrX\":" + string("\"") + output[21 + ((size_char)*j)] + output[22 + ((size_char)*j)] + output[23 + ((size_char)*j)] + output[24 + ((size_char)*j)] + output[25 + ((size_char)*j)]
		+ output[26 + ((size_char)*j)] + output[27 + ((size_char)*j)] + "\"" + "," + "\n";

		myfile << "\"GyrY\":" + string("\"") + output[28 + ((size_char)*j)] + output[29 + ((size_char)*j)] + output[30 + ((size_char)*j)] + output[31 + ((size_char)*j)] + output[32 + ((size_char)*j)]
		+ output[33 + ((size_char)*j)] + output[34 + ((size_char)*j)] + "\"" + "," + "\n";

		myfile << "\"GyrZ\":" + string("\"") + output[35 + ((size_char)*j)] + output[36 + ((size_char)*j)] + output[37 + ((size_char)*j)] + output[38 + ((size_char)*j)] + output[39 + ((size_char)*j)]
		+ output[40 + ((size_char)*j)] + output[41 + ((size_char)*j)] +  string("\"") + "\n";

		if (i == quantidadeDados - 1 && j == samples - 1) fim = true;
		if (i <= quantidadeDados - 1 && fim == false) myfile << "},\n";
	}

	if (i == quantidadeDados - 1) {
		myfile << "}\n";
		myfile << "]\n";
		myfile << "}";
	}
}

int ColetaDeDados() {
	auto start = std::chrono::high_resolution_clock::now();
	char* charArray = write_array;
	arduino.writeSerialPort(charArray, 1);
	Sleep(100);
	arduino.readSerialPort(output, MAX_DATA_LENGTH);

	if (output[0] && output[MAX_DATA_LENGTH - 1] == '\0') {
		cout << "Um erro aconteceu nos dados!" << endl;
		return 0;
	} 

	return 1;
}