a = [1 3 5; 7 8 0];
for i=1:size(a,1)
    for j=1:size(a,2)
        b = a(i,j);
        if b == 0
            disp(i)
            disp(j)
        end
    end
end
