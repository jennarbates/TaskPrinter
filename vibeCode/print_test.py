from escpos.printer import Usb
from escpos.exceptions import USBNotFoundError

# YOUR IDS (Verified from your scan)
VENDOR_ID = 0x0fe6
PRODUCT_ID = 0x811e

def print_demo():
    try:
        # 1. Connect
        # If this line fails, you might need 'sudo' or to remove the Mac printer queue
        p = Usb(VENDOR_ID, PRODUCT_ID)

        # 2. Print Header
        p.text("Mark is lame and doesn't pull\n")
        
        # 3. Big Text (Bold, 2x Width, 2x Height)
        # We use width=2, height=2 instead of the old 'double_height' params
        p.set(align='center', bold=True, width=2, height=2)
        p.text("RP331 WORKS\n")
        
        # 4. Reset to Normal
        # explicitly set width/height back to 1 to "normalize" text
        p.set(align='left', bold=False, width=1, height=1)
        
        p.text("He's literally just bad\n")
        p.text("--------------------------------\n")
        
        # 5. QR Code & Cut
        p.qr("https://tralfamadore.dev")
        p.text("\n\n")
        p.cut()

        print("Success: Print job sent.")

    except USBNotFoundError:
        print("Error: Printer not found. Check USB connection.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    print_demo()
