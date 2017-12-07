# Display a value on IKEA's Sparsnäs

Connect an IR-LED to your Raspberry Pi and make the LED blink into the Sparsnäs IR-sensor. Now you have a remote wireless display that can show a number representing whatever you want. Use it to display a time countdown to an event. The cpu temperature. The current number of visitors on your web site. How much free space you have on your hard drive. Network latency when you're gaming. Or something else. Yeah, the number will have the letter W tagged on to it. Live with it. No you can't display negative numbers.

The number to be displayed on Sparsnäs is picked up from a settings file that the python script checks every few seconds, continuously updating the displayed number. Preferably start the script at boot and then change the number to display whenever you want by updating the settings file.

With the default setting of "pulses per KWh" set to 10000 in Sparsnäs the highest number that is feasible to display is around 3000 or so. This corresponds roughly to 10 Hertz and the system seems to struggle beyond that. To display larger numbers just use a lower pulse per KWh setting in Sparsnäs and update the python code accordingly.

Accuracy. Well, it's so so. Remember that we are not transmitting the number to display in its native format but as a time delay which can vary just so very slightly due to varying system load in the Raspberry. There is an offset setting in the python code that you can fine tune to get the correct values displayed. A higher offset value renders a slightly higher number on the display. 




# Prerequisites

Install pigpio on your Raspberry:
```
sudo apt-get install pigpio python-pigpio python3-pigpio -y
sudo systemctl enable pigpiod.service
sudo systemctl start pigpiod.service
```  
The default GPIO pin used is gpio 17 (which equals to pin 11 on a Model 3 Pi). You can of course choose to use any other pin by updating the python code.

The settings file ```sparsnas.display``` should contain one single line with the number to display.


