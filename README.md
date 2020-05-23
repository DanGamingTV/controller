## remo.tv is an open telerobotics platform designed for controling and sharing control of robots online in real time.

##EV3dev guide
Install ev3dev on your ev3 and establish an SSH connection before proceeding.
Guides for this are at [ev3dev.org](https://ev3dev.org)


1. Install the required software libraries and tools. Make sure you don’t get any errors in the console when doing the step below. If you have an issue, you can run this line again, and that will usually fix it!

   ```sh
   sudo apt update
   sudo apt upgrade -y
   sudo apt install ffmpeg python-serial python-dev libgnutls28-dev espeak python-smbus python-pip git
   ```

2. Download the remotv control scripts from our github

   ```sh
   git clone https://github.com/DanGamingTV/ev3-controller.git ~/remotv
   ```

3. Install python requirements

   ```sh
   sudo python -m pip install -r ~/remotv/requirements.txt
   ```

4. Open the new `remotv` directory

   ```sh
   cd remotv
   ```

5. Copy `controller.sample.conf` to `controller.conf`

   ```sh
   cp controller.sample.conf controller.conf
   ```

## Configure the controller

1. Edit the `controller.conf` file created in the previous section.
   ```sh
   nano controller.conf
   ```
2. Configure the `[robot]` section

   - `owner` should be the username you have registered the robot under on the remo.tv site.
   - `robot_key` is the API key for your robot that you made on the site.
      - Your API key is LONG. It should look something like `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6InJib3QtNTVjZjJmMjUtNjBhNS00ZDJkLTk5YzMtOGZmOGRiYWU4ZDQ1IiwiaWF0IjoxNTczNTExMDA2LCJzdWIiOiIifQ.LGXSBSyQ4T4X5xU_w3QJD6R3lLjrrkw_QktOIDzRW5U`. If it is not this long, you have not copied the full key.
      
## Starting up
SSH into your robot, and make sure it has internet access.
Navigate into the ~/remotv folder
```sh
cd ~/remotv
```
Then run this
```sh
brickrun -- echo YOURLINUXPASSWORDHERE | python3 controller.py
```
