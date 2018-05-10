# raspi-death
**A collection of scripts for launching a deauthentication attack from a Raspberry Pi**


## Overview
The goal of this project was to hack Alexa. That obviously wasn't going to happen (#seniorspring)
so the new goal became to prank my parents (my dad, specifically) who got 
an Alexa for Christmas. I wanted to know if I could build a little device such that 
any time my dad asked Alexa a question, I could disconnect her from the internet. 
Alexa would be reconnected by the time he'd try to trouble shoot, but any time he said "Alexa" 
she'd get disconnected again.

I call the attack/prank "mansplaining" (credz to Prof. Mickens). Any time you ask Alexa
a question, you shoot out spoofed pockets over the network (deauth packets) 
and render her unable to answer

This whole thing took me way longer than it should have and don't look too closely 
at my code, thanks.

## Hardware / System Components
* Raspberry Pi Model 2B+ running Raspbian 4.1.37 -v7+
* Panda Wireless PAU06 3000Mbps Wireless Adapter

## Software Components
* Aircrack-ng (install using apt-get)
* Python 2.7.9

## File Structure
* main.sh -- driver script--scans network for APs + client info,
	calls parse.py to parse that info, sets wireless adapter
	to correct wifi channel to prep for attack
* parse.py -- parses output from network scan to find the AP 
	the client you wish to disconnect is connected to and
	what channel it's on, writes two new bash scripts
	that will 1) set the adapter to the correct channel
	2) launch the actual deauth attack

## Usage
./main.sh INTERFACE CLIENT\_MAC

Where INTERFACE is the wifi interface you'd like to use 
(you can list available interfaces using iwconfig, it's probably wlan0)

and CLIENT\_MAC is the MAC address of the client that you'd like
to deauthenticate from the network once the voice command is heard

