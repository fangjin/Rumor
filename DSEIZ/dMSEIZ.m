function [dy] = dMSEIZ( t, y )

    global beta b p l rho eps  alpha m delta gamma;
    
    S = y(1);
    E = y(2);
    I = y(3);
    Z = y(4);
    
    N = S+E+I+Z;
    
    dy(1,1) = -1*beta*S*(I/N) - b*S*(Z/N);        % S
    dy(1,2) = (1-p)*beta*S*(I/N) + (1-l)*b*S*(Z/N) - rho*E*(I/N) - eps*E - alpha*E*(Z/N) - delta*E;       % E
    dy(1,3) = p*beta*S*(I/N) + rho*E*(I/N) + eps*E + m*gamma*I*(Z/N) - (1-m)*gamma*I*(Z/N);
    dy(1,4) = l*b*S*(Z/N) + alpha*E*(Z/N) + delta*E - m*gamma*I*(Z/N) + (1-m)*gamma*I*(Z/N);
end