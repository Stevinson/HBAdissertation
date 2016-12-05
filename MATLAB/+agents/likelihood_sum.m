%% 
% Sum likelihood function
% Edward Stevinson 18/7/16
%
% Input:
%   w = Time window (i.e. using past w entries)
%
% Output:
%   f = Sum likelihood function

function f = likelihood_sum(w)
    f = @f_w;

    function L = f_w(H)
        len = size(H,2);

        if len > w,
            H = H(:,(len-w+1):len);
        end

        L = sum(H,2);
    end
end