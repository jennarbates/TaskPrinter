from escpos.printer import Usb

# 1. Hardware ID Constants (The "Name Tag" of your printer)
# VENDOR_ID = 0x0fe6  (Rongta)
# PRODUCT_ID = 0x811e (RP331)
# ---------------------------------------------------------
try:
    # 2. Connect to the printer
    # 'p' is now your remote control for the device.
    p = Usb(0x0fe6, 0x811e)

    # --- YOUR CODE GOES HERE ---
    
    p.text("Connection Successful!\n")
    p.cut()

except Exception as e:
    print(f"Printer Error: {e}")
