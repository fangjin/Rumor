function [TOUT, YOUT] = forward_euler( f, dt, T, Y0 )
    % Set-up dimensions of output time and solution arrays.
    TOUT = (T(1):dt:T(2))';
        
    % Apply initial conditions.
    YOUT(1,:) = Y0;
            
    for j = 2:size(TOUT)
        Y = YOUT(j-1,:);
        temp = f(TOUT(j),Y);
        A = dt.*temp + Y;
        
        YOUT(j,:) = A';
        %disp(TOUT(j));
    end
end