# MQTT Debugger with GUI

This application is a graphical MQTT client built using `Tkinter` and `Paho-MQTT` for Python. It allows users to connect to an MQTT broker, subscribe to topics, and publish messages. It supports both regular MQTT and WebSockets protocols, and provides multiple modes for message handling.

## Features

- **Protocol Selection**: Choose between MQTT (default) and WebSockets for the connection protocol.
- **Settings Panel**: Configure the broker address, port, username, and password.
- **Modes** (Multiple modes can be selected at once.):
  - **Print**: Display the full message as received.
  - **Timer**: Show the time interval between consecutive messages.
  - **Abbreviate**: Limit message length to 999 characters.

- **Subscription and Publishing**: Subscribe to any topic and publish messages to the broker.
- **Message Display**: All received messages and application logs are displayed in a scrollable text area on the right.

## Prerequisites

Before running this application, ensure that you have the following installed:

- **Python 3.6+**
- Required Python packages:
  - `paho-mqtt`
  - `tkinter` (Included with most Python installations)

You can install `paho-mqtt` with the following command:

```bash
pip install paho-mqtt
```

## How to Use

1. **Clone/Download the Script**: Download the `debuggerGUI.py` file to your machine.
2. **Run the Application**:
   - From your terminal or command prompt, navigate to the directory containing the script.
   - Run the script using Python:
     ```bash
     python debuggerGUI.py
     ```

### Main Window

When you launch the application, you will see the main window divided into two sections:

1. **Left Panel**: This is the settings panel where you can configure the connection and select the modes for message handling.
2. **Right Panel**: This section displays the received messages and logs from the application.

### Steps to Connect

1. **Select the Protocol**: Choose between Regular MQTT and WebSockets using the radio buttons.
2. **Broker Address and Port**: Enter the address and port of your MQTT broker (defaults: `test.mosquitto.org` on port `1883` for MQTT, and port `9001` for WebSockets).
3. **Optional**: Enter your username and password if your broker requires authentication.
4. **Select Modes**: Choose one or more message processing modes (Print, Timer, Abbreviate).
5. **Click 'Connect'**: Press the `Connect` button to initiate the connection to the broker. Connection status will be displayed on the right side.
6. **Subscribe to a Topic**: Enter the topic you'd like to subscribe to, then press the `Subscribe` button. Messages from this topic will be displayed in the right panel.
7. **Publish a Message**: Enter the topic and message you'd like to publish, then click the `Publish` button.

### Disconnecting

The connection will automatically stop when you close the application window.

## Troubleshooting

### WebSockets Issues

1. **Incorrect Port**: Ensure that you're using the correct port for WebSockets (commonly `9001` or `8080`).
2. **Broker Configuration**: Ensure that your broker supports WebSockets. For example, Mosquitto requires specific configuration to enable WebSockets.

### Firewall Settings

Make sure that your firewall allows connections to the specified ports on your broker.

## License

This project is open-source and free to use. Feel free to modify and improve it for your own purposes!
