function [dy] = dSEIZ( t, y )

    global beta b p l rho eps;
    
    S = y(1);
    E = y(2);
    I = y(3);
    Z = y(4);
    
    N = S+E+I+Z;
    
    dy(1,1) = -1*beta*S*(I/N) - b*S*(Z/N);        % S
    dy(1,2) = (1-p)*beta*S*(I/N) + (1-l)*b*S*(Z/N) - rho*E*(I/N) - eps*E;       % E
    dy(1,3) = p*beta*S*(I/N) + rho*E*(I/N) + eps*E;
    dy(1,4) = l*b*S*(Z/N);
end