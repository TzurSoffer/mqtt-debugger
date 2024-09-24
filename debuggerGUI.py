import paho.mqtt.client as mqtt
import json
import time
import tkinter as tk
from tkinter import messagebox, scrolledtext


class DebuggerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MQTT Debugger")
        self.client = None
        self.callbacks = []

        # Default settings
        self.broker_address = "test.mosquitto.org"
        self.port = 1883
        self.username = None
        self.password = None
        self.protocol = "MQTT"  # Default protocol
        self.modes = []  # Modes will be stored as a list

        # Create GUI layout
        self.create_interface()

    def create_interface(self):
        """Creates the main GUI layout with a left-side settings panel and right-side received message display."""
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Left settings panel
        self.left_frame = tk.Frame(self.main_frame, width=300)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        # Protocol Selection
        tk.Label(self.left_frame, text="Protocol").pack(anchor=tk.W)
        self.protocol_var = tk.StringVar(value="MQTT")
        tk.Radiobutton(self.left_frame, text="Regular", variable=self.protocol_var, value="MQTT", command=self.update_port).pack(anchor=tk.W)
        tk.Radiobutton(self.left_frame, text="WebSockets", variable=self.protocol_var, value="WebSockets", command=self.update_port).pack(anchor=tk.W)

        # Broker Address
        tk.Label(self.left_frame, text="Broker Address").pack(anchor=tk.W)
        self.broker_entry = tk.Entry(self.left_frame)
        self.broker_entry.insert(0, self.broker_address)
        self.broker_entry.pack(fill=tk.X, pady=5)

        # Port Number
        tk.Label(self.left_frame, text="Port").pack(anchor=tk.W)
        self.port_entry = tk.Entry(self.left_frame)
        self.port_entry.insert(0, str(self.port))
        self.port_entry.pack(fill=tk.X, pady=5)

        # Username
        tk.Label(self.left_frame, text="Username").pack(anchor=tk.W)
        self.username_entry = tk.Entry(self.left_frame)
        self.username_entry.pack(fill=tk.X, pady=5)

        # Password
        tk.Label(self.left_frame, text="Password").pack(anchor=tk.W)
        self.password_entry = tk.Entry(self.left_frame, show="*")
        self.password_entry.pack(fill=tk.X, pady=5)

        # Mode Selection (multiple can be selected)
        tk.Label(self.left_frame, text="Select Modes").pack(anchor=tk.W)
        self.mode_var1 = tk.IntVar(value=0)
        self.mode_var2 = tk.IntVar(value=0)
        self.mode_var3 = tk.IntVar(value=0)

        tk.Checkbutton(self.left_frame, text="Print", variable=self.mode_var1, command=self.update_modes).pack(anchor=tk.W)
        tk.Checkbutton(self.left_frame, text="Timer", variable=self.mode_var2, command=self.update_modes).pack(anchor=tk.W)
        tk.Checkbutton(self.left_frame, text="Abbreviate", variable=self.mode_var3, command=self.update_modes).pack(anchor=tk.W)

        # Connect Button
        self.connect_btn = tk.Button(self.left_frame, text="Connect", command=self.connect_to_broker)
        self.connect_btn.pack(pady=10)

        # Subscribe Topic
        tk.Label(self.left_frame, text="Topic to Subscribe").pack(anchor=tk.W)
        self.topic_entry = tk.Entry(self.left_frame)
        self.topic_entry.pack(fill=tk.X, pady=5)

        self.subscribe_btn = tk.Button(self.left_frame, text="Subscribe", command=self.subscribe)
        self.subscribe_btn.pack(pady=10)

        # Publish Section
        tk.Label(self.left_frame, text="Topic to Publish").pack(anchor=tk.W)
        self.pub_topic_entry = tk.Entry(self.left_frame)
        self.pub_topic_entry.pack(fill=tk.X, pady=5)

        tk.Label(self.left_frame, text="Message to Publish").pack(anchor=tk.W)
        self.pub_msg_entry = tk.Entry(self.left_frame)
        self.pub_msg_entry.pack(fill=tk.X, pady=5)

        self.publish_btn = tk.Button(self.left_frame, text="Publish", command=self.publish)
        self.publish_btn.pack(pady=10)

        # Right message display panel
        self.right_frame = tk.Frame(self.main_frame, bg="white")
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # ScrolledText widget for displaying received messages
        self.received_text = scrolledtext.ScrolledText(self.right_frame, state="disabled", bg="lightgray", wrap=tk.WORD)
        self.received_text.pack(fill=tk.BOTH, expand=True)

    def update_port(self):
        """Update the default port based on the selected protocol."""
        protocol = self.protocol_var.get()
        if protocol == "MQTT":
            self.port_entry.delete(0, tk.END)
            self.port_entry.insert(0, "1883")
        elif protocol == "WebSockets":
            self.port_entry.delete(0, tk.END)
            self.port_entry.insert(0, "9001")  # Default WebSocket port; adjust as needed

    def update_modes(self):
        """Update the list of callbacks based on the selected modes."""
        self.callbacks.clear()  # Clear previous selections
        if self.mode_var1.get():
            self.callbacks.append(self.printf)
        if self.mode_var2.get():
            self.callbacks.append(self.timer)
        if self.mode_var3.get():
            self.callbacks.append(self.abbreviate)

    def connect_to_broker(self):
        """Connect to the MQTT broker based on the selected protocol and settings."""
        self.broker_address = self.broker_entry.get()
        try:
            self.port = int(self.port_entry.get())
        except ValueError:
            messagebox.showerror("Invalid Port", "Please enter a valid port number.")
            return

        self.username = self.username_entry.get() if self.username_entry.get() else None
        self.password = self.password_entry.get() if self.password_entry.get() else None
        self.protocol = self.protocol_var.get()

        if self.protocol == "WebSockets":
            self.client = mqtt.Client(transport="websockets")
        else:
            self.client = mqtt.Client()

        if self.username and self.password:
            self.client.username_pw_set(self.username, self.password)

        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect

        try:
            self.client.connect(self.broker_address, self.port)
            self.client.loop_start()
            # Provide immediate feedback
            self.update_text_area(f"Attempting to connect to broker {self.broker_address}:{self.port} using {self.protocol}...\n")
        except Exception as e:
            messagebox.showerror("Connection Error", f"Failed to connect: {e}")

    def on_connect(self, client, userdata, flags, rc):
        """Callback for when the client receives a CONNACK response from the server."""
        if rc == 0:
            self.update_text_area("Connection Successful\n")
            #messagebox.showinfo("Connected", f"Connected to broker {self.broker_address}:{self.port}.")
        else:
            self.update_text_area(f"Connection failed with code {rc}\n")
            messagebox.showerror("Connection Failed", f"Failed to connect, return code {rc}")
            self.client.loop_stop()

    def on_disconnect(self, client, userdata, rc):
        """Callback for when the client disconnects from the broker."""
        if rc != 0:
            self.update_text_area("Unexpected disconnection.\n")
            messagebox.showwarning("Disconnected", "Unexpectedly disconnected from broker.")
        else:
            self.update_text_area("Disconnected from broker.\n")
            messagebox.showinfo("Disconnected", "Disconnected from broker.")

    def subscribe(self):
        """Subscribe to a topic and configure the message callback."""
        topic = self.topic_entry.get()
        if not topic:
            messagebox.showwarning("Input Error", "Please enter a topic.")
            return

        try:
            self.client.subscribe(topic)
            self.client.on_message = self.on_message
            self.update_text_area(f"Subscribed to {topic}\n")
            #messagebox.showinfo("Subscribed", f"Subscribed to {topic}")
        except Exception as e:
            messagebox.showerror("Subscription Error", f"Failed to subscribe to {topic}: {e}")

    def publish(self):
        """Publish a message to a topic."""
        topic = self.pub_topic_entry.get()
        message = self.pub_msg_entry.get()
        if not topic or not message:
            messagebox.showwarning("Input Error", "Please enter both topic and message.")
            return

        try:
            self.client.publish(topic, json.dumps({"content": message}))
            self.update_text_area(f"Published to {topic}: {message}\n")
            #messagebox.showinfo("Published", f"Message published to {topic}")
        except Exception as e:
            messagebox.showerror("Publish Error", f"Failed to publish message: {e}")

    def on_message(self, client, userdata, message):
        """Handle received MQTT messages and apply the selected modes."""
        for callback in self.callbacks:
            callback(client, userdata, message)

    def printf(self, client, userdata, message):
        """Print the received message."""
        data = message.payload.decode("utf-8")
        self.update_text_area(f"{message.topic}: {data}\n")

    def timer(self, client, userdata, message):
        """Display the time since the last message."""
        current_time = time.time()
        if not hasattr(self, "last_message_time"):
            time_diff = 0
        else:
            time_diff = current_time - self.last_message_time
        self.last_message_time = current_time
        self.update_text_area(f"Time since last message: {time_diff:.2f} seconds\n")

    def abbreviate(self, client, userdata, message):
        """Abbreviate the received message to 999 characters."""
        data = message.payload.decode("utf-8")
        abbreviated_data = data[:999] + ("..." if len(data) > 999 else "")
        self.update_text_area(f"{message.topic}: {abbreviated_data}\n")

    def update_text_area(self, text):
        """Update the right-hand text area with received messages."""
        self.received_text.configure(state="normal")
        self.received_text.insert(tk.END, text)
        self.received_text.configure(state="disabled")
        self.received_text.see(tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = DebuggerApp(root)
    root.mainloop()
