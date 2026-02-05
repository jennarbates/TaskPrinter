# TaskPrinter 🖨️

A collection of Python scripts to control a Rongta RP331 thermal receipt printer from macOS. This project turns a standard POS printer into a personal task manager, daily scheduler, and fun receipt generator.

## 🛠️ Hardware
* **Printer:** Rongta RP331 (80mm Thermal Printer)
* **Connection:** USB
* **Paper:** Standard 80mm Thermal Receipt Paper

## 📋 Prerequisites (macOS)

Before running the scripts, you need specific system libraries to allow Python to talk to USB devices on a Mac.

1.  **Install Homebrew** (if not installed)
2.  **Install libusb:**
    ```bash
    brew install libusb
    ```
3.  **Python 3.x**

## ⚙️ Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/jennarbates/TaskPrinter.git](https://github.com/jennarbates/TaskPrinter.git)
    cd TaskPrinter
    ```

2.  **Set up the Virtual Environment:**
    *Note: It is critical to recreate the venv if you move the project folder.*
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install python-escpos google-api-python-client google-auth-httplib2 google-auth-oauthlib
    ```

## 🔑 Configuration

### 1. USB Printer IDs
All scripts use the following constants for the Rongta RP331. If you use a different printer, update these at the top of the scripts.
* **Vendor ID:** `0x0fe6`
* **Product ID:** `0x811e`

### 2. Google Calendar API (Optional)
1.  Go to Google Cloud Console and create a project.
2.  Enable the **Google Calendar API**.
3.  Create **OAuth Desktop Credentials**.
4.  Download the JSON file, rename it to `credentials.json`, and place it in the root of this folder.

---

## 📚 Developer Cheat Sheet (python-escpos)

Reference for writing your own scripts.

### Basic Setup

```python
from escpos.printer import Usb
from escpos.exceptions import USBNotFoundError

# --- CONFIGURATION SECTION ---
# These are the specific IDs for your Rongta RP331
VENDOR_ID = 0x0fe6
PRODUCT_ID = 0x811e

def run_ultimate_demo():
    """
    This function runs through every major capability of the printer.
    """
    try:
        # 1. CONNECTION
        # We initialize the printer object. The 'profile' argument helps
        # the library know roughly what "dialect" of commands to use.
        # "TM-T88IV" is a standard Epson profile that works well for Rongta.
        p = Usb(VENDOR_ID, PRODUCT_ID, profile="TM-T88IV")

        # --- SECTION 1: TEXT FORMATTING ---
        
        # Reset everything to default before starting
        p.set(align='center', bold=True, double_height=True, double_width=True)
        p.text("FEATURE TEST\n")
        p.text("RP331 PRINTER\n")
        
        # Reset to normal (Always do this after big text!)
        p.set(align='left', bold=False, normal_text=True)
        p.text("\n") # Spacer

        # A. Alignment
        p.set(align='left')
        p.text("Left Aligned Text\n")
        
        p.set(align='center')
        p.text("Center Aligned Text\n")
        
        p.set(align='right')
        p.text("Right Aligned Text\n")

        # B. Fonts & Styles
        p.set(align='left', bold=True)
        p.text("Bold Mode: ON\n")
        p.set(bold=False) # Turn it off!

        p.set(invert=True)
        p.text(" Inverted Mode (White/Black) ")
        p.set(invert=False) # Turn it off!
        p.text("\n")

        p.set(font='b')
        p.text("Font B: This is the 'compressed' font.\n")
        p.text("It is useful for fitting lots of data on one line.\n")
        p.set(font='a') # Back to standard Font A

        # --- SECTION 2: SIZING ---
        
        p.text("\n--- TEXT SIZING ---\n")
        # The .set() method takes width and height multipliers (1-8)
        
        p.set(width=2, height=2)
        p.text("2x Size (Standard Header)\n")

        p.set(width=3, height=3)
        p.text("3x Size (Kitchen)\n")
        
        p.set(width=1, height=1) # Reset to normal
        
        # --- SECTION 3: GRAPHICS & BARCODES ---
        
        p.text("\n--- OBJECTS ---\n")

        # A. QR Codes
        # Native QR generation. 'size' controls the pixel size of each dot.
        p.set(align='center')
        p.text("Scan for Python:\n")
        p.qr("https://www.python.org", size=5)
        p.text("(QR Code Size 5)\n\n")

        # B. Barcodes
        # Useful for tracking tickets or inventory.
        # 'CODE39' is the standard alphanumeric barcode.
        # pos='OFF' hides the text numbers below the bars.
        p.text("Ticket #12345:\n")
        p.barcode('12345', 'CODE39', height=64, width=3, pos='OFF')
        p.text("\n")

        # --- SECTION 4: HARDWARE CONTROL ---

        # A. Cash Drawer
        # If you had a cash drawer plugged into the back, this would pop it open.
        # It sends a pulse to pin 2.
        # p.cashdraw(2) 
        
        # B. Raw Commands (Advanced)
        # Sometimes you need to send a raw hexadecimal code that the library 
        # doesn't support. You can send raw bytes like this.
        # Example: This is the command to "Beep" (ESC B <n> <t>) on some models.
        # p._raw(b'\x1B\x42\x03\x02') 

        # --- SECTION 5: THE CUT ---
        
        p.set(align='center')
        p.text("\n")
        p.text("End of Test.\n")
        p.text("Jenna's Terminal\n")
        
        # CRITICAL: Always feed a few lines before cutting!
        # The cutter is physically located about 1 inch *above* the print head.
        # If you cut immediately, you will chop off your last line of text.
        p.text("\n\n\n\n") 
        
        p.cut()

        print("Success! Test slip printed.")

    except USBNotFoundError:
        print("❌ Error: Printer not found.")
        print("Check if the USB cable is loose or if the printer is off.")
    
    except Exception as e:
        print(f"❌ An error occurred: {e}")
        # Common fix tip for Mac users
        if "Access denied" in str(e) or "Resource busy" in str(e):
            print("\n💡 TIP: Mac has locked the driver.")
            print("Run: lpadmin -x <your_printer_queue_name> to remove it.")

if __name__ == "__main__":
    run_ultimate_demo()
```
