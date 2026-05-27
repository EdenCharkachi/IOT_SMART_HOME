# Start all components (Windows PowerShell)
# 1) Ensure Mosquitto is running in a separate window: mosquitto -v
# 2) Run from project root:
#    powershell -ExecutionPolicy Bypass -File .\scripts\start_all_windows.ps1

python .\db\setup_db.py

Start-Process -NoNewWindow python -ArgumentList ".\manager.py"
Start-Process -NoNewWindow python -ArgumentList ".\emulators\gate_relay_emulator.py"
Start-Process -NoNewWindow python -ArgumentList ".\emulators\parking_sensor_emulator.py"
Start-Process -NoNewWindow python -ArgumentList ".\gui\dashboard.py"

Write-Host "Started: manager + gate relay + sensor emulator + GUI"
Write-Host "Optional manual control: python .\emulators\gate_button_emulator.py"
