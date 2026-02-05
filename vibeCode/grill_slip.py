from escpos.printer import Usb
from datetime import datetime
import random

# YOUR PRINTER IDS
VENDOR_ID = 0x0fe6
PRODUCT_ID = 0x811e

def print_grill_slip(tasks):
    try:
        p = Usb(VENDOR_ID, PRODUCT_ID)
        
        # Start numbering orders at a random "busy lunch rush" number
        order_num = random.randint(10, 99)

        for task in tasks:
            # --- 1. THE BLACK HEADER (White on Black) ---
            p.set(align='center', invert=True)
            
            # The "Side" number or Order Number (Massive)
            p.set(align='center', invert=True, bold=True, width=3, height=3)
            p.text(f" {order_num} \n")
            
            # Destination (e.g., EAT-IN or TAKE-OUT)
            p.set(align='center', invert=True, bold=True, width=1, height=1)
            p.text("  EAT-IN  \n")
            
            # Turn off black background
            p.set(invert=False)
            
            # --- 2. TIME & REGISTER ---
            p.set(align='left', bold=False, font='b') # Tiny font
            time_str = datetime.now().strftime("%H:%M")
            p.text(f"Reg 1 - {time_str}\n")
            p.text("--------------------------------\n")

            # --- 3. THE ITEM (Your Task) ---
            # Cooks need to see this from far away, so we make it huge.
            p.set(align='left', bold=True, font='a', width=2, height=2)
            
            # Truncate if too long to fit on one line
            display_task = task[:12].upper() 
            p.text(f"1 {display_task}\n")
            
            # --- 4. MODIFIERS (The "Grill Instructions") ---
            # This is where they usually put "NO ONION". 
            # We will put productivity modifiers.
            p.set(align='left', bold=True, width=1, height=1, font='b') # Red/Bold look
            
            p.text("    ONLY FOCUS\n")
            p.text("    NO   DISTRACTIONS\n")
            p.text("    XTRA EFFORT\n")

            # --- 5. CUT ---
            # Grill slips are short. We feed just enough to clear the cutter.
            p.text("\n\n\n") 
            p.cut()
            
            # Increment order number for next task
            order_num += 1

    except Exception as e:
        print(f"Error: {e}")

# Your "Orders"
kitchen_orders = [
    "Finish Code",
    "Email Prof",
    "Laundry"
]

if __name__ == "__main__":
    print_grill_slip(kitchen_orders)
