1.对硬盘分区
diskpart
select disk 0
clean
convert gpt
rem == 1. System partition =========================
create partition efi size=100
format quick fs=fat32 label="System"
assign letter="S"
rem == 2. Microsoft Reserved (MSR) partition =======
create partition msr size=128
rem == 3. Main partition ===========================
create partition primary 
format quick fs=ntfs label="Main"
assign letter="M"
exit


2.附加vhd
diskpart
select vdisk file=M:\WINSVR2022.VHDX
attach vdisk


3.添加bcd
V:\
cd v:\windows\system32
bcdboot v:\windows /s S: /f UEFI