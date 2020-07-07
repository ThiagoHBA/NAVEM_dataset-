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
char write_array_success[1] = { 's' };
char write_array_fail[1] = {'f'};
char write_array_end[1] = { 'e' };
char led[1] = { '1' };
// int quantidadeDados = 1000;

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

int VerificaçãoDosDados(char* output) {
	if (output[0] == '\0' || output[MAX_DATA_LENGTH - 1] == '\0') {
		cout << "Um erro aconteceu nos dados!" << endl;
		cout << "Primeiro valor do array: " << output[0] << endl;
		cout << "Ultimo valor do array: " << output[MAX_DATA_LENGTH - 1] << endl;
		return 0;
	}

	if (output[4] != '.'  || output[40] != '.' || output[85] != '.') {
		cout << "virgula no lugar errado!" << endl;
		cout << "Virgula do inicio:" << output[4] << endl;
		cout << "Virgula do meio:" << output[40] << endl;
		cout << "Virgula final: " << output[85] << endl;
		return 0;
	}
	return 1;
}

int EscritaArquivoDados(ofstream &myfile, int i, int quantidadeDados) {

	if (i == 0) {
		myfile << "{";
		myfile << "\"Dados\"";
		myfile << ": [\n";
	}
	
	if (!VerificaçãoDosDados(output)) {
		char* charArray = write_array_fail;
		arduino.writeSerialPort(charArray, 1);
		return 0;
	}

	int samples = 8;
	int size_char = 9*10;
	bool fim = false;
	for (int j = 0; j < samples; j++) {

		myfile << "{";
		myfile << "\"i\":" + to_string(i) + "," + '\n';

		myfile << "\"AccX\":" + string("\"") + output[0+((size_char)*j)] + output[1+((size_char)*j)] + output[2 + ((size_char)*j)] + output[3 + ((size_char)*j)] + output[4 + ((size_char)*j)]
		+ output[5 + ((size_char)*j)]  +  output[6 + ((size_char)*j)] + output[7 + ((size_char)*j)] + output[8 + ((size_char)*j)] + "\"" + "," + "\n";

		myfile << "\"AccY\":" + string("\"") + output[9 + ((size_char)*j)] + output[10 + ((size_char)*j)] + output[11 + ((size_char)*j)] + output[12 + ((size_char)*j)] + output[13 + ((size_char)*j)]
		+ output[14 + ((size_char)*j)] + output[15 + ((size_char)*j)] + output[16 + ((size_char)*j)] + output[17 + ((size_char)*j)] +  "\"" + "," + "\n";

		myfile << "\"AccZ\":" + string("\"") + output[18 + ((size_char)*j)] + output[19 + ((size_char)*j)] + output[20 + ((size_char)*j)] + output[21 + ((size_char)*j)] + output[22 + ((size_char)*j)]
		+ output[23 + ((size_char)*j)] + output[24 + ((size_char)*j)] + output[25 + ((size_char)*j)] + output[26 + ((size_char)*j)] + "\"" + "," + "\n";

		myfile << "\"GyrX\":" + string("\"") + output[27 + ((size_char)*j)] + output[28 + ((size_char)*j)] + output[29 + ((size_char)*j)] + output[30 + ((size_char)*j)] + output[31 + ((size_char)*j)]
		+ output[32 + ((size_char)*j)] + output[33 + ((size_char)*j)] + output[34 + ((size_char)*j)] + output[35 + ((size_char)*j)] + "\"" + "," + "\n";

		myfile << "\"GyrY\":" + string("\"") + output[36 + ((size_char)*j)] + output[37 + ((size_char)*j)] + output[38 + ((size_char)*j)] + output[39 + ((size_char)*j)] + output[40 + ((size_char)*j)]
		+ output[41 + ((size_char)*j)] + output[42 + ((size_char)*j)] + output[43 + ((size_char)*j)] + output[44 + ((size_char)*j)] + "\"" + "," + "\n";

		myfile << "\"GyrZ\":" + string("\"") + output[45 + ((size_char)*j)] + output[46 + ((size_char)*j)] + output[47 + ((size_char)*j)] + output[48 + ((size_char)*j)] + output[49 + ((size_char)*j)]
		+ output[50 + ((size_char)*j)] + output[51 + ((size_char)*j)] + output[52 + ((size_char)*j)] + output[53 + ((size_char)*j)] + string("\"") +  "," + "\n";

		myfile << "\"MagX\":" + string("\"") + output[54 + ((size_char)*j)] + output[55 + ((size_char)*j)] + output[56 + ((size_char)*j)] + output[57 + ((size_char)*j)] + output[58 + ((size_char)*j)]
		+ output[59 + ((size_char)*j)] + output[60 + ((size_char)*j)] + output[61 + ((size_char)*j)] + output[62 + ((size_char)*j)] +  string("\"") + "," + "\n";

		myfile << "\"MagY\":" + string("\"") + output[63 + ((size_char)*j)] + output[64 + ((size_char)*j)] + output[65 + ((size_char)*j)] + output[66 + ((size_char)*j)] + output[67 + ((size_char)*j)]
		+ output[68 + ((size_char)*j)] + output[69 + ((size_char)*j)] + output[70 + ((size_char)*j)] + output[71 + ((size_char)*j)] + string("\"") + "," + "\n";

		myfile << "\"MagZ\":" + string("\"") + output[72 + ((size_char)*j)] + output[73 + ((size_char)*j)] + output[74 + ((size_char)*j)] + output[75 + ((size_char)*j)] + output[76 + ((size_char)*j)]
		+ output[77 + ((size_char)*j)] + output[78 + ((size_char)*j)] + output[79 + ((size_char)*j)] + output[80 + ((size_char)*j)] +  string("\"") + "," + "\n";

		myfile << "\"deltat\":" + string("\"") + output[81 + ((size_char)*j)] + output[82 + ((size_char)*j)] + output[83 + ((size_char)*j)] + output[84 + ((size_char)*j)] + output[85 + ((size_char)*j)]
		+ output[86 + ((size_char)*j)] + output[87 + ((size_char)*j)] + output[88 + ((size_char)*j)] + output[89 + ((size_char)*j)] +  string("\"") +  "," + "\n";
		
		long long int time_since_epoch = duration_cast<microseconds>(system_clock::now().time_since_epoch()).count();
		myfile << "\"time_usec\":" + string("\"") + to_string(time_since_epoch) + string("\"") + '\n';

		if (i == quantidadeDados - 1 && j == samples - 1) fim = true;
		if (i <= quantidadeDados - 1 && fim == false) myfile << "},\n";
	}

	if (i == quantidadeDados - 1) {
		myfile << "}\n";
		myfile << "]\n";
		myfile << "}";
		char* charArray = write_array_end;
		arduino.writeSerialPort(charArray, 1);
	}
	return 1;
}

int ColetaDeDados(int i) {
	char* charArray = write_array_success;
	arduino.writeSerialPort(charArray, 1);
	Sleep(120);
	arduino.readSerialPort(output, MAX_DATA_LENGTH);


	return 1;
}
