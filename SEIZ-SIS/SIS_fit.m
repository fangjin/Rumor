function SIS_fit()

    clear; clc; %close all;
    global data dt a b;
    
    % Open data file.
    file = '/Riot_vertex.txt';
    fid = fopen(file);
    
     % Load data.
    C_text = textscan(fid, '%s', 2, 'delimiter', '\t');
    C_data = textscan(fid, '%f %f');
    tweets_accumulated = C_data{2};        
    
    % Normalize tweets to population.
    ps = 1e5;
    tweets_accumulated = tweets_accumulated / ps;
    
    % Compute time array sand dt.
    time = (1:length(tweets_accumulated));
    dt = 0.5;
    
    % Set data matrix for system fitting.
    data = zeros(2, length(time));
    data(1,:) = time;
    data(2,:) = tweets_accumulated;
             
    % Fit the Rumor (tweet) data to SIS Model. Parameter order: S0 I0 a b
    options = optimset('MaxFunEvals',1E8,'MaxIter',1E8,'TolFun',1e-8,'TolX',1e-8);
    fit=lsqnonlin('SISFitFunction',[1 1 1 1],[0 0 0 0],[20 5 10 10],options); % Nonlinear least squares fit 
    %fit=lsqnonlin('SISFitFunction',[100 1 1 1],[0 0 0 0],[10000 500 10 10],options); % Nonlinear least squares fit 
    
    % Compute fitting results.
    S0 = fit(1); I0 = fit(2); a = fit(3); b = fit(4);
    [T,Y] = forward_euler(@dSIS, dt, [time(1) time(end)],[S0 I0]);
    S = Y(:,1);  I = Y(:,2);
    N = S + I;
    R0 = b/a;
    
    % Display results.
    % Plot solution of ODE system.

    figure; hold on; 
    set(gca,'FontName','Times New Roman','FontSize',20)
    plot(T,S./N,'b', 'LineWidth',2.5);
    plot(T,I./N,'r', 'LineWidth',2.5);
    plot(T,N./N,'m', 'LineWidth',2.5);
    legend ({'S' 'I' 'N'});
    print(gcf,'-dpng','SIS_Riot_vertex_total.png');
    
    % Plot true tweet data to fit results (I).
    figure; hold on; 
    set(gca,'FontName','Times New Roman','FontSize',20)
    plot(time,ps*tweets_accumulated, 'b.', 'MarkerSize',14);
    plot(T, ps*I, 'r-', 'LineWidth',2.5);
    xlabel('Time (h)'); ylabel('I (Cummulated Tweets)');
    hleg1 = legend({'Tweet Data' 'Fit'});
    set(hleg1,'Location','NorthWest')
    title('SIS Model Fit to Tweet Data'); box on; grid on;
    
    % Compute error and write on plot.
    same = ismember(T, time);
    I_subset = I(find(same==1));
    err_ave = ps*mean (abs(I_subset-tweets_accumulated));
    err_norm = norm(I_subset-tweets_accumulated) / norm(tweets_accumulated);
           
    text(time(120),ps*I( round(length(I)/2.5) ), strcat('Error: ',num2str(err_norm)), 'FontSize',18);
    text(time(120),ps*I( round(length(I)/3) ), strcat('Mean Deviation: ',num2str(err_ave)), 'FontSize',18);

    print(gcf,'-dpng','SIS_Riot_vertex.png');
   % keyboard;
end
