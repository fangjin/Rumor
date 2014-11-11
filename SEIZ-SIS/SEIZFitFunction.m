function y = SEIZFitFunction(params)

global data dt beta b p l rho eps;

time=data(1,:)';                 % Time
trueI=data(2,:)';                % Actual Tweets from data

S0 = params(1); E0 = params(2); I0 = params(3); Z0 = params(4); 
beta = params(5); b = params(6); p = params(7); 
l = params(8); rho = params(9); eps = params(10);

[T,Y] = forward_euler(@dSEIZ, dt, [time(1) time(end)],[S0 E0 I0 Z0]);
I = Y(:,3);

same = ismember(T, time);
I_subset = I(find(same==1));

y = abs(trueI - I_subset);                         % Fit error

end