function MSEIZ_Trust_fit()

    clear; clc; %close all;
    global data dt beta b p l rho eps   alpha m delta gamma;
    
    % Open tweets data file and load data.
    file = '../rumor_data/paper/15accumulated-trust-Boston.txt';
    fid = fopen(file);
    C_data = textscan(fid, '%f %f');
    tweets_truth_accumulated = C_data{2}; 
    
    % Open doubt data file and load data.
    file = '../rumor_data/paper/15accumulated-doubt-Boston.txt';
    fid = fopen(file);
    C_data = textscan(fid, '%f %f');
    tweets_doubt_accumulated = C_data{2}; 
    
    % Scale tweets to population.
    %ps = 1e5;   
    ps=1;
    tweets_truth_accumulated = tweets_truth_accumulated / ps;
    tweets_doubt_accumulated = tweets_doubt_accumulated / ps;
    
    % Compute time array and dt.
    time = (1:length(tweets_truth_accumulated));
    dt = 0.01;
    
    % Set data matrix for system fitting. Order: time, trust, doubt.
    data = zeros(3, length(time) );
    data(1,:) = time;
    data(2,:) = tweets_truth_accumulated;
    data(3,:) = tweets_doubt_accumulated;
             
    % Fit the Rumor (tweet) data to MSEIZ model that incorporates Trust and Doubt. 
    % Parameter order: S0 E0 I0 Z0 beta b p l rho eps  alpha m delta gamma
    options = optimset('MaxFunEvals',1E8,'MaxIter',1E8,'TolFun',1e-8,'TolX',1e-8);
    fit=lsqnonlin('MSEIZ_TrustFitFunction',[1e6 10 10 10 1 1 0.5 0.5 1 1 1 0.5 1 1],...
                                    [0 0 0 0 0 0 0 0 0 2e-5 0 0 0 2e-5],...
                                    [5e6 1e4 1e4 1e4 20 20 1 1 20 20 20 1 20 20],options);
    % Get fitting results.
    S0 = fit(1); E0 = fit(2); I0 = fit(3); Z0 = fit(4); 
    beta = fit(5); b = fit(6); p = fit(7); 
    l = fit(8); rho = fit(9); eps = fit(10);
    alpha = fit(11); m = fit(12); delta = fit(13); gamma=fit(14);
    
    [T,Y] = forward_euler(@dMSEIZ, dt, [time(1) time(end)],[S0 E0 I0 Z0]);
    %[T,Y] = ode45(@dSEIZ1,[time(1) time(end)],[S0 E0 I0 Z0]);
    S = Y(:,1);  E = Y(:,2);  I = Y(:,3);  Z = Y(:,4);
    N = S+E+I+Z;
    
    keyboard;
    
    % Display results.
    % Plot solution of ODE system.
    figure; hold on; 
    plot(T,ps*S,'b');
    plot(T,ps*E,'r');
    plot(T,ps*I,'g');
    plot(T,ps*Z,'k');
    plot(T, ps*N,'m');
    legend ({'S' 'E' 'I' 'Z' 'N'})  
    
    figure; hold on; 
    plot(T,S./N,'b');
    plot(T,E./N,'r');
    plot(T,I./N,'g');
    plot(T,Z./N,'k');
    plot(T,N./N,'m');
    legend ({'S' 'E' 'I' 'Z' 'N'})  

    % Plot true truth tweet data to fit results (I).
    figure; hold on; 
    plot(time,ps*tweets_truth_accumulated, 'b.');
    plot(T, ps*I, 'r-');
    xlabel('Time (h)'); ylabel('I (Cummulated Tweets)'); legend({'Tweet Data' 'Fit'});
    title('Modified SEIZ Model Fit to Believer Tweet Data'); box on; grid on;
    
    % Compute Error and place on plot.
    same = ismember(T, time);
    I_subset = I(find(same==1));
    err_ave = ps*mean (abs(I_subset-tweets_truth_accumulated));
    err_norm = norm(I_subset-tweets_truth_accumulated) / norm(tweets_truth_accumulated);
    text(time(20),ps*I( round(length(I)/2) ), strcat('Error: ',num2str(err_norm)));
    text(time(20),ps*I( round(length(I)/3) ), strcat('Mean Deviation: ',num2str(err_ave)));
    
     % Plot true sceptic tweet data to fit results (Z).
    figure; hold on; 
    plot(time,ps*tweets_doubt_accumulated, 'b.');
    plot(T, ps*Z, 'r-');
    xlabel('Time (h)'); ylabel('Z (Cummulated Tweets)'); legend({'Tweet Data' 'Fit'});
    title('Modified SEIZ Model Fit to Sceptic Tweet Data'); box on; grid on;
    
    % Compute Error and place on plot.
    same = ismember(T, time);
    Z_subset = Z(find(same==1));
    err_ave = ps*mean (abs(Z_subset-tweets_doubt_accumulated));
    err_norm = norm(Z_subset-tweets_doubt_accumulated) / norm(tweets_doubt_accumulated);
    text(time(20),ps*Z( round(length(Z)/2) ), strcat('Error: ',num2str(err_norm)));
    text(time(20),ps*Z( round(length(Z)/3) ), strcat('Mean Deviation: ',num2str(err_ave)));
    keyboard;
end
