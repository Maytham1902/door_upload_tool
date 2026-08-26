# door_upload_tool
Multi-threaded batch software uploader for train door control systems (DCUs). Features dynamic IP subnet resolving, Tkinter UI, and ReportLab PDF report export.


🚀 Step-by-Step Usage Instructions
1. Configure the Upload Parameters
   Launch the application and complete the initial setup parameters in the Configuration panel:
   - Select Firmware Binary: Click Browse... to select the firmware or payload file (.bin, .hex, .img) you wish to load into the DCUs.
   - Specify Train Unit Number: Type the 2-digit Train Unit ID (e.g., 01, 14). The application automatically formats unit IDs for network resolution.
   - Select Car Set Type: Choose either single or long from the dropdown menu. This adjusts the target IP subnets dynamically:
       a. Single Car Sets: Maps targets to 10.93.XX.XXX
       b. Long Car Sets: Maps targets to 10.94.XX.XXX2.
2. Initiate the Batch Upload
   - Click Start Batch Upload.
   - The application populates the status table with all mapped Door Control Units (Door 1L through Door 4R) and their corresponding target IP addresses.
   - The multi-threaded upload engine kicks off, attempting simultaneous UDP/TFTP socket transfers across all mapped DCU endpoints in parallel.
   - Watch the Status column update in real time (PENDING $\rightarrow$ UPLOADING... $\rightarrow$ SUCCESS / VERIFIED or FAILED).
3. Generate Maintenance Documentation
   - Once all target channels complete their transfer cycles, the Export PDF Checksheet button becomes enabled.
   - Click Export PDF Checksheet and pick a directory to save the verification file.
   - The tool generates an official, structured PDF report capturing the Train Unit ID, configuration type, selected firmware filename, timestamp, and final status across every door channel for compliance logging.

⚠️ Safety & Operational Checklist
  - Hardware Connection: Ensure your field laptop is connected to the active train network interface or switch before starting.
  - Clear Door Zones: Always ensure door leaves and surrounding danger zones are clear of personnel and equipment before triggering software uploads.
