function [dy] = dI( t, y )

    global a b;
    
    S = y(1);
    I = y(2);
    dy(1,1) = -1*b*S*I + a*I;
    dy(1,2) = b*S*I - a*I;
    dy = dy; 
end