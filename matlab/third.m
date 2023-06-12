clear all
close all

vid = VideoReader("ball.mp4");
matVid = read(vid);
b = matVid(400:1200,70:700,:,:);
for i=1:size(b,4)
   d(:,:,:,i) = im2bw(b(:,:,:,i),59/256);
   [r, c] = find(d(:,:,:,i)==1);
   if isempty(r)
       mr(i) = 0;
   else
       mr(i) = max(r);
   end
end
y = size(d,1);
h = y-mr;
plot(h);
dif = diff(h)/0.02;
figure
plot(dif);
mh = max(h);
for j=1:length(h)
    if h(j) == mh
       f = j;
       disp(f);
    end
end