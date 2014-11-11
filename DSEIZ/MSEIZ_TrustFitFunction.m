function y = MSEIZ_TrustFitFunction(params)
          
global data dt beta b p l rho eps   alpha m delta gamma;

time=data(1,:)';                 % Time
trueI=data(2,:)';                % Actual Trust Tweets from data
trueZ=data(3,:)';                % Actual Doubt Tweets from data
trueE=data(4,:)';				 % Actual Exposed Tweets from data

S0 = params(1); E0 = params(2); I0 = params(3); Z0 = params(4); 
beta = params(5); b = params(6); p = params(7); 
l = params(8); rho = params(9); eps = params(10);
alpha = params(11); m = params(12); delta=params(13); gamma=params(14);


[T,Y] = forward_euler(@dMSEIZ, dt, [time(1) time(end)],[S0 E0 I0 Z0]);
E = Y(:,2);
I = Y(:,3);
Z = Y(:,4);

same = ismember(T, time);
I_subset = I(find(same==1));
Z_subset = Z(find(same==1));
E_subset = E(find(same==1));

y = abs(trueI - I_subset) + abs(trueZ - Z_subset) + abs(trueE - E_subset);                   % Fit error
end