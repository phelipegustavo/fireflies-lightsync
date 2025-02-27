<div align="center">
  <img src="./fireflies-light-sync.svg" />
</div>

<h1 align="center">
Fireflies Light Sync  
</h1>

This project provides a graphical user interface (GUI) for controlling the Logitech G203 Prodigy / G203 LightSync Mouse LED settings. It allows users to easily interact with the mouse's LED features without needing to use the command line interface (CLI) directly.

Inspired by and based on [g203-led](https://github.com/smasty/g203-led).

![image](https://github.com/user-attachments/assets/9bfdd926-b285-4899-bd10-0ae0c588d9c6)


## How to install

To install the app, run the following commands:

```
git clone https://github.com/phelipegustavo/fireflies-lightsync.git
cd fireflies-lightsync
./install-ubuntu
```

After that, you should be able to open the app from the applications menu. A sudo password is required.

## Project Structure

```
fireflies-lightsync*
├── src
│   ├── main.py               # Entry point of the application
│   ├── gui
│   │   ├── __init__.py       # GUI package initializer
│   │   ├── main_window.py    # Main window class for the GUI
│   ├── lib
│   │   ├── __init__.py       # CLI package initializer
│   │   └── g203_led.py       # CLI logic for controlling the mouse
├── requirements.txt          # Project dependencies
└── README.md                 # Project documentation
```

## Features

- Off - Disable leds
- Fixed - Single color mode
- Wave - Cycle all colors from left to right
- Breathing - Single color Breathing
- DPI settings - **TBD**
- Custom Colors - **TBD**

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bug fixes.

### Installation

To install the required dependencies, run the following command:

```
pip install -r requirements.txt
```

### Usage

To start the application, run the following command:

```
sudo python src/main.py
```

This will launch the GUI, allowing you to control the LED settings of your Logitech G203 mouse.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
