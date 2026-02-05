import usb.core
import usb.util

# Find all devices
devs = usb.core.find(find_all=True)

if not devs:
    print("No USB devices found at all. (Check your specific USB port permissions)")
else:
    print("Scanning USB devices...\n")
    for dev in devs:
        try:
            # We need the Hexadecimal values for your config
            vid = hex(dev.idVendor)
            pid = hex(dev.idProduct)
            print(f"Found Device: {vid}:{pid}")
            
            # Try to get the product name to confirm it's the Rongta
            # (This might fail if macOS has locked the device, hence the try/except)
            manufacturer = usb.util.get_string(dev, dev.iManufacturer)
            product = usb.util.get_string(dev, dev.iProduct)
            print(f"  - Name: {manufacturer} {product}")
            
        except Exception as e:
            # If we can't read the name, it's likely the printer (macOS locks printers tightly)
            print(f"  - Name: [Locked/Unknown Device] (Likely your Printer)")
        print("-" * 30)
