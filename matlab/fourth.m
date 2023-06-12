clear all
close all

vid = VideoReader("ball.mp4");
matVid = read(vid);
matVid(:,:,:,102) = 0;
index = [];
for i=1:size(matVid,4)
    d = matVid(:,:,:,i);
    if d==0
        index = [index i];
    end
end
disp(index)
%plot(index)
