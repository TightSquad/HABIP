clear all
%% Initialize variables.
save_mat_filename = 'ramp_dir_change_3.mat'
filename = 'C:\Users\stevy\OneDrive\Documents\Steven''s Stuff\RIT 5\Senior Design\HABIP_Code\MATLAB\test_data\ramp_dir_change\LOG_2.TXT';
delimiter = ',';

%% Format for each line of text:
%   column1: text (%q)
%	column2: text (%q)
%   column3: double (%f)
%	column4: double (%f)
% For more information, see the TEXTSCAN documentation.
formatSpec = '%q%q%f%f%[^\n\r]';

%% Open the text file.
fileID = fopen(filename,'r');

%% Read columns of data according to the format.
% This call is based on the structure of the file used to generate this
% code. If an error occurs for a different file, try regenerating the code
% from the Import Tool.
dataArray = textscan(fileID, formatSpec, 'Delimiter', delimiter, 'EmptyValue' ,NaN, 'ReturnOnError', false);

%% Close the text file.
fclose(fileID);

%% Post processing for unimportable data.
% No unimportable data rules were applied during the import, so no post
% processing code is included. To generate code which works for
% unimportable data, select unimportable cells in a file and regenerate the
% script.

%% Allocate imported array to column variable names
hour_min = dataArray{:, 1};
sec_ms = dataArray{:, 2};
z_gyro = dataArray{:, 3};
motor_speed = dataArray{:, 4};


%% Clear temporary variables
clearvars filename delimiter formatSpec fileID dataArray ans;

length_data = size(sec_ms,1);

hour = [];
min = [];
sec = [];
ms = [];
rpm = [];

for i = 1:size(sec_ms,1)
    hour_min_hex = hour_min(i);
    sec_ms_hex = sec_ms(i);
    %motor_speed_voltage = (motor_speed(i) / 4096) * 3.3
    motor_speed_rpm = (((motor_speed(i) / 4096) * 3.3) * 2590) - 2590;

    
    hour_min_bin = hexToBinaryVector(hour_min_hex, 16, 'MSBFirst');
    sec_ms_bin = hexToBinaryVector(sec_ms_hex, 16, 'MSBFirst');
    
    hour_bin = hour_min_bin(1:8);
    min_bin = hour_min_bin(9:16);
    
    sec_bin = sec_ms_bin(1:6);
    ms_bin = sec_ms_bin(7:16);

    hour_temp = bi2de(hour_bin, 'left-msb');
    min_temp = bi2de(min_bin, 'left-msb');
    sec_temp = bi2de(sec_bin, 'left-msb');
    ms_temp = bi2de(ms_bin, 'left-msb');

    hour = [hour; hour_temp];
    min = [min; min_temp];
    sec = [sec; sec_temp];
    ms = [ms; ms_temp];
    rpm = [rpm; motor_speed_rpm];
end

save(save_mat_filename);

plot(z_gyro)
