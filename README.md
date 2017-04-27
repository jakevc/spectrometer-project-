# spectrometer-project
In this project you are given a csv file that contains absorptivity data of an iron/ortho-phenanthroline complex in units of L/(mg*cm), and data containing the emission spectra of several candidate LED light sources for use in a spectrometer. The goal is to determine which LED is most useful for detecting the absorbance of the iron/ortho-phenanthroline complex.

![figure_1](https://cloud.githubusercontent.com/assets/17414791/25508500/5c9f3184-2b67-11e7-8175-ffeb9b0c4d45.png)
![figure_2](https://cloud.githubusercontent.com/assets/17414791/25508522/7b03d896-2b67-11e7-9748-473920b179c6.png)


After analysis of the light source, the spectrometer was built using an Arduino Genuino UNO. The Arduino Spectrometer was built, and programmed in arduino, the arduino script is provided in this repository. A python script was written as a program that can be run to get Absorbance of a blank, and a sample in a cuvette using either a red or green LED as a light source. The python script, and a picture of the program output from an ipython interpreter is provided.
![specdata](https://cloud.githubusercontent.com/assets/17414791/25508525/7eaca770-2b67-11e7-8be4-35fde974359e.png)
