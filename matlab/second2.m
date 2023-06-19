clear all
close all

inp = input('Type Frame number --> ')
vid = VideoReader("ball.mp4");
matVid = read(vid);
s = size(matVid);
b = matVid(400:1200,70:700,:,:);
ss = size(b);
for i=1:s(4)
   d(:,:,:,i) = im2bw(b(:,:,:,i),59/256);
   d1 = d(2:2:ss(1),:,i);
   d2 = d(1:2:ss(1),:,i);
   [r1, c1] = find(d1==1);
   [r2, c2] = find(d2==1);
   if isempty(r1)
       m1 = 0;
   else
       m1 = max(r1);
   end
   if isempty(r2)
       m2 = 0;
   else
       m2 = max(r2);
   end
   mr(2*i-1) = m1;
   mr(2*i) = m2;
end
sss = size(d1);
y = sss(1);
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
aa = matVid;
aa(:,:,:,inp) = 0;
implay(aa);
% make above code as progressive videso 
% find index number of frame that is black image