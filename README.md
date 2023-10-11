# Picomotor8742
This is a project to implement a [labscript_device](https://docs.labscriptsuite.org/projects/labscript-devices/en/latest/index.html) for accessing the Newport (previously named New Focus) [8742](https://www.newport.com/p/8742) picomoter controller used for high precision optics adjustment in the optical setup of our [RbYb Tweezer Lab](https://porto.jqi.umd.edu/).

**If you are a member of the Lab, please access the project's [OneNote](https://onedrive.live.com/view.aspx?resid=601343494F74D454%215914&id=documents&wd=target%28Setting%20up%20Hardware%20Vol.%202.one%7C4494AEAA-32A1-4BE6-AB27-3721055533CD%2FObjective%20Stage%20Computer%20Control%7C5C5A9393-C272-44DD-8A4B-437DD485D3B3%2F%29) page.**

## Author Info:
**Created by:** Juntian "Oliver" Tu  
**E-mail:** [juntian@umd.edu](mailto:juntian@umd.edu)  
**Address:** 2261 Atlantic Building, 4254 Stadium Dr, College Park, MD 20742

## Environment Requirement
The project is developed in `Python 3` and based on NewPort's [**PicomotorApp**](https://www.newport.com/p/8742) under the 64-bit Windows environment.

This implementation is a part of the [Labscript suite](https://docs.labscriptsuite.org/en/latest/) in the master computer in our lab and could not run without the Labscript platform.

The `TwoPicomotor8081` related classes are designed specifically for controlling the two Newport [8081](https://www.newport.com/p/8081) motorized tilt aligners in our lab. You may need to adjust the code to have it fit your setup if you are employing the class in the first place.

## Project Structure:
The project includes two sets of separate labscript_devices, namely `Picomotor8742` and `TwoPicomotor8081`, the latter is an integrated version of the former one aiming to control 10 picomotors through three 8742 modules specifically designed for our lab. For both of them, the control computer communicates with the 8742s through TCP/IP channels that should be configured in the connection_table file before running the Blacs.

Due to the pre-programming nature of labscript, when running a sequence, all picomotor motion would be executed before PulseBlaster starts to output triggers so no in-sequence motion is allowed.

Since the 8742 could only control one picomotor at a time and Blacs main thread worker will be blocked until all motions are finished, a separate thread is included in the program to handle the motor motion and to avoid blocking the main thread of Blacs. 


An independent `config.ipynb` is included to manually change the settings of the picomotor controller outside the labscript implementation.

## Acknowledgements:
Thanks to **P. T. Starkey** and **C. J. Billington** from Monash University for the development and maintenance of Labscript.