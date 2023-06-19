vid = VideoReader("ball.mp4");
matVid = read(a);
img = matVid(:,:,:,100);
bwImg = im2bw(c,100/256);
b1=bwImg(2:2:size(img,1),:,:);
b2=bwImg(1:2:size(img,1),:,:);
figure
imshow(bwImg)
figure
montage({b1 b2})
