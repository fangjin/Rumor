function y = SISFitFunction(params)

global data dt a b;

time=data(1,:)';                 % Time
trueI=data(2,:)';                % Actual Tweets from data

S0 = params(1); I0 = params(2); a = params(3); b = params(4); 

[T,Y] = forward_euler(@dSIS, dt, [time(1) time(end)],[S0 I0]);
%[T,Y] = ode45(@dSIS,[time(1) time(end)],[S0 I0]);
I = Y(:,2);

same = ismember(T, time);
I_subset = I(find(same==1));

%I_subset = I( find(histc(time,T)==1) );

y = abs(trueI - I_subset);                         % Fit error

end