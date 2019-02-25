/* Программа управления шаговым двигателем и
измерения расстояния УЗ датчиком, установленным на вал двигателя.
Создано   - 28.12.2018
Изменено - 22.02.2019
*/
#include <Stepper.h>
#define STEPS 4 // Количество импульсов на 1 шаг
Stepper stepper(STEPS, 8, 9, 10, 11);
char data; // данные принятые с COM
int direction; // направление вращения 1 или -1
int trig_pin = 3;// пины соединения с дальномером
int echo_pin = 2;
int distance = 0; // измеренное расстояние

void setup()
{
	stepper.setSpeed(500);
	Serial.begin(9600);
	pinMode(trig_pin, OUTPUT);
	pinMode(echo_pin, INPUT);
}
void loop()
{
	if(Serial.available() )  { // приём команд с COM порта
    	data = Serial.read();
    	// Serial.println(data);
    	switch (data){
        case 'R':
	    	Povorot_sector(-1);
	    	Stop_Motor();
        break;
	    case 'L':
	    	Povorot_sector(1);
	    	Stop_Motor();	
        break;
	    case 'C':
	    	Ranging_cycle();
	    	Stop_Motor();
        break;
        case 'S':
	    	Ranging_sector();
	    	Stop_Motor();
        break;
        default:
        	Stop_Motor();
        break;     

	}	
	distance = RangFiltr();
	Serial.println(distance);
}
}

int Ranging(){ //возвращает измеренное расстояние в см
	int dist;
	int duration;
	digitalWrite(trig_pin, LOW);
	delayMicroseconds(2);
	digitalWrite(trig_pin, HIGH);
	delayMicroseconds(10);
	digitalWrite(trig_pin, LOW);
	duration = pulseIn(echo_pin, HIGH);
	dist = duration / 58;
	return dist;
}

int RangFiltr(){ // вычисляет среднее из 3-х близких значений
				  // если одно любое отличается более чем на delta
				  // вычисляет среднее из 2-х. Мажоритарный алгоритм.
	int r [3];
	int f_dist;
	int delta;  // ошибка измерения
	delta = 4;
	for (int i = 0; i < 3; i++){
		r[i] = Ranging();
		delay(10);
	}
// все три отсчёта верны
	if ((abs(r[0] - r[1]) < delta) and (abs(r[0] - r[2]) < delta) and (abs(r[1] - r[2]) < delta)) {
		f_dist = (r[0] + r[1] + r[2]) / 3; }
// ошибка первого отсчёта
	if ((abs(r[0] - r[1]) > delta) and (abs(r[0] - r[2]) > delta) and (abs(r[1] - r[2]) < delta)) {
		f_dist = (r[1] + r[2]) / 2;	}
// ошибка второго отсчёта
	if ((abs(r[0] - r[1]) > delta) and (abs(r[0] - r[2]) < delta) and (abs(r[1] - r[2]) > delta)) {
		f_dist = (r[0] + r[2]) / 2;	}
// ошибка третьего отсчёта
	if ((abs(r[0] - r[1]) < delta) and (abs(r[0] - r[2]) > delta) and (abs(r[1] - r[2]) > delta)) {
		f_dist = (r[0] + r[1]) / 2;	}
	return f_dist;
}
void Ranging_cycle(){ // поворачивает УЗ датчик на ~180 гр. вправо,
					  // на каждом шаге измеряет дальность,
					  // передает её на монитор
					  // и возвращает датчик в исходное
	for (int i = 0; i < 6; i++){
		Povorot_sector(-1);
		distance = RangFiltr();
		Serial.println(distance);
	}
	stepper.step(-4);
	Povorot_180(1);
}

void Povorot_180(int direction){ // поворот на 180 гр. 
								 // в заданном напрвлении	
	for(int i = 0; i < 25; i++){
		stepper.step(direction*STEPS);
	}
}

void Povorot_sector(int direction){	
	for(int i = 0; i < 4; i++){
		stepper.step(direction*STEPS);
	}
}

void Stop_Motor(){		// отключение питания от двигателя
	for (int i = 8; i < 12; i++)
	{
		digitalWrite(i, LOW);
	}
}

void Ranging_sector(){	// сканирование сектора 180 градусов
	for (int i = 0; i < 100; i++){
		stepper.step(-1);
		distance = RangFiltr();
		Serial.println(distance);
	}
	Povorot_180(1);
}
