========================================================================
TRAIN DOOR SYSTEM BATCH UPLOADER v2.0
========================================================================

A standalone Windows desktop application designed to automate firmware 
deployments across Train Control Network (TCN) Door Control Units (DCUs).

This distribution is completely self-contained. IT DOES NOT REQUIRE PYTHON, 
PIP, OR ANY ADDITIONAL SOFTWARE PACKAGES INSTALLED ON THE TARGET COMPUTER.

------------------------------------------------------------------------
1. QUICK START (FOR FIELD TECHNICIANS)
------------------------------------------------------------------------
1. Extract the 'TrainDoorBatchUploader' folder to any location on your PC.
2. Double-click 'TrainDoorBatchUploader.exe' to launch the program.
3. Click 'Browse...' to select the target firmware binary file (.bin / .hex).
4. Enter the 2-digit Train Unit ID (e.g., 01, 14).
5. Select the Car Set Type ('single' or 'long').
6. Click 'Start Batch Upload' to begin parallel transmission across all DCUs.
7. Click 'Export PDF Checksheet' upon completion to save an official report.

------------------------------------------------------------------------
2. KEY FEATURES
------------------------------------------------------------------------
* Zero Dependencies: Runs out-of-the-box on any standard Windows 10/11 PC.
* Multi-Threaded Loader: Parallel UDP/TFTP uploads to all doors simultaneously.
* Automatic IP Resolver: Maps unit numbers and car set types directly to DCU 
  subnets (10.93.x.x for single sets, 10.94.x.x for long sets).
* Compliance Documentation: Automatically compiles verification reports 
  and maintenance checksheets into PDF format.

------------------------------------------------------------------------
3. SYSTEM REQUIREMENTS
------------------------------------------------------------------------
* Operating System: Windows 10 or Windows 11 (64-bit)
* Network: Active Ethernet connection to the Train Control Network / DCU link.
* Rights: Standard User privileges (Admin rights not required to run executable).

------------------------------------------------------------------------
4. SAFETY & OPERATIONAL NOTICE
------------------------------------------------------------------------
* Authorized Personnel Only: This software is intended for qualified train 
  electrical technicians and maintenance engineering staff.
* Pre-Execution Check: Verify all door zones are clear of obstruction and 
  personnel prior to initiating firmware upload routines.
========================================================================
