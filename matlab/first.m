clear all
close all

a = VideoReader("ball.mp4");
b = read(a);
for i=100:106!a.NumFrames
    c = b(:,:,:,i);
    imresize(c,[2 3])
    !c = im2bw(b(:,:,:,i));
    !d = rgb2gray(c);
    !imhist(d);
    imshow(c)

end