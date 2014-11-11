function SEIZ_fit()

    clear; clc; %close all;
    global data dt beta b p l rho eps;
    
    % Open data file.
    %file = '../rumor_data/Boston-1day_all_news.txt';
    file = '/Castro_edge.txt';
    fid = fopen(file);
    
    % Load data.
    C_text = textscan(fid, '%s', 2, 'delimiter', '\t');
    C_data = textscan(fid, '%f %f');
    tweets_accumulated = C_data{2}; 
    
    % Scale tweets to population.
    ps = 1e5;
    tweets_accumulated = tweets_accumulated / ps;
    
    % Compute time array and dt.
    time = (1:length(tweets_accumulated));
    dt = 0.1;
    
    % Set data matrix for system fitting.
    data = zeros(2, length(time) );
    data(1,:) = time;
    data(2,:) = tweets_accumulated;
             
    % Fit the Rumor (tweet) data to SEIZ model. 
    % Parameter order: S0 E0 I0 Z0 beta b p l rho eps
    options = optimset('MaxFunEvals',1E8,'MaxIter',1E8,'TolFun',1e-8,'TolX',1e-8);
    fit=lsqnonlin('SEIZFitFunction',[10 0.2 0.2 0.2 1 1 0.5 0.5 1 1],[0 0 0 0 0 0 0 0 0 2e-5],[20 5 5 5 10 10 1 1 10 10],options); % Nonlinear least squares fit 
    
    % Get fitting results.
    S0 = fit(1); E0 = fit(2); I0 = fit(3); Z0 = fit(4); 
    beta = fit(5); b = fit(6); p = fit(7); 
    l = fit(8); rho = fit(9); eps = fit(10);
    
    % Compute I and Z reproductive rates.
%     mu = 1;
%     Roi = (beta*(eps+p*mu)) / (mu*(eps+mu));
%     Roz = l*b/mu;
    Roi = (beta*(eps+p)) / eps;
    Roz = l*b;
    
    %S0 = S0;   
    [T,Y] = forward_euler(@dSEIZ, dt, [time(1) time(end)],[S0 E0 I0 Z0]);
    %[T,Y] = ode45(@dSEIZ1,[time(1) time(end)],[S0 E0 I0 Z0]);
    S = Y(:,1);  E = Y(:,2);  I = Y(:,3);  Z = Y(:,4);
    N = S+E+I+Z;
    
    % Display results.
    % Plot solution of ODE system.
    figure; hold on; 
    set(gca,'FontName','Times New Roman','FontSize',20)
    plot(T,ps*S,'b',  'LineWidth',2.5);
    plot(T,ps*E,'r',  'LineWidth',2.5);
    plot(T,ps*I,'g',  'LineWidth',2.5);
    plot(T,ps*Z,'k',  'LineWidth',2.5);
    plot(T, ps*N,'m',  'LineWidth',2.5);
    legend ({'S' 'E' 'I' 'Z' 'N'})
    print(gcf,'-dpng','SEIZ_Castro_edge_total1.png');
    
    figure; hold on; 
    set(gca,'FontName','Times New Roman','FontSize',20)
    plot(T,S./N,'b',  'LineWidth',2.5);
    plot(T,E./N,'r',  'LineWidth',2.5);
    plot(T,I./N,'g',  'LineWidth',2.5);
    plot(T,Z./N,'k',  'LineWidth',2.5);
    plot(T,N./N,'m',  'LineWidth',2.5);
    legend ({'S' 'E' 'I' 'Z' 'N'})
    print(gcf,'-dpng','SEIZ_Castro_edge_total2.png');

    % Plot true tweet data to fit results (I).
    figure; hold on; 
    set(gca,'FontName','Times New Roman','FontSize',20)
    
    plot(time,ps*tweets_accumulated, 'b.',  'MarkerSize',14);
    plot(T, ps*I, 'r-', 'LineWidth',2.5);
    xlabel('Time (h)'); ylabel('I (Cummulated Tweets)');
    hleg1 = legend({'Tweet Data' 'Fit'});
    set(hleg1,'Location','NorthWest');
    title('SEIZ Model Fit to Tweet Data'); box on; grid on;
    
    
    % Compute Error and place on plot.
    same = ismember(T, time);
    I_subset = I(find(same==1));
    err_ave = ps*mean (abs(I_subset-tweets_accumulated));
    err_norm = norm(I_subset-tweets_accumulated) / norm(tweets_accumulated);
    text(time(100),ps*I( round(length(I)/2.5) ), strcat('Error: ',num2str(err_norm)), 'FontSize',18);
    text(time(100),ps*I( round(length(I)/3) ), strcat('Mean Deviation: ',num2str(err_ave)), 'FontSize',18);
    print(gcf,'-dpng','SEIZ_Castro_edge.png');
    %keyboard;
end


