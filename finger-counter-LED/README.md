# Finger-to-LED System
This project links **hand-tracking detection in Python** with an **Arduino** that lights up LEDs based on detected finger positions.

You have three main components:
- `fingerCounter.py` → Detects fingers using OpenCV + MediaPipe and sends data to Arduino
- `handTrackingModule.py` → Custom hand tracking helper
- `fingertoled.ino` → Arduino code that reads serial data and controls 5 LEDs

---

## 🚀 How it Works
1. Python detects your hand using your webcam
2. Python counts which fingers are open (thumb → pinky)
3. Python sends a 5-character string like:
   - `"10110"` → Finger open/close status
4. Arduino receives it and turns LEDs ON/OFF accordingly

---

## 🧱 Project Structure
```

fingertoled/
│
├── fingerCounter.py
├── handTrackingModule.py
├── fingertoled.ino
├── requirements.txt
└── README.md

```

---

## 🛠️ Requirements (Python + Arduino)
### **Arduino IDE Extensions Needed**
To run `fingertoled.ino` smoothly, install these inside **Arduino IDE**:

1. **Boards Manager:**
   - Install **Arduino AVR Boards** (for Arduino Uno, Nano, Mega)

2. **Extensions (from Library Manager):**
   - **No extra Arduino libraries are required** for this project.
   - All functions used (`Serial`, `digitalWrite`, etc.) come from the built-in core.

3. **Optional helpful extensions:**
   - **Serial Monitor Plus** (better debugging)
   - **Arduino IDE Themes** (just for UI)

---

## 🛠️ Python Requirements
```

opencv-python
mediapipe
pyserial

````

---

## ▶️ How to Run
### **1. Upload Arduino Code**
Open `fingertoled.ino` in Arduino IDE → upload to your board.
Make sure baud rate = **9600**.

### **2. Install Python Dependencies**
```sh
pip install -r requirements.txt
````

### **3. Run the Python Script**

```sh
python fingerCounter.py
```

Make sure:

* Webcam works
* COM port matches your Arduino

---

## 🧪 Testing

* When you open 3 fingers → Python prints `00111`
* Arduino receives it
* LEDs 3, 4, 5 turn ON accordingly

---

## 🐞 Troubleshooting

**Arduino not receiving data?**

* Check COM port
* Make sure Python uses the same baud rate
* Remove any extra `
  ` or `
  ` issues (already handled in your code)

**Mediapipe slow?**

* Reduce webcam resolution

---

Enjoy your smart gesture-controlled LEDs! 💡🤘


