% Function that returns a random action drawn from a given mixed strategy
%
% Input:
%   x = Mixed strategy
% Output:
%   a = Random action drawn from x
%%

function a = randomAction(x)

    % How many actions
    n = length(x); % e.g [0.1 0.4 0.5]
    a = n;
    r = rand;
    x = cumsum(x);

    for k = 1:n-1,
        if r < x(k),
            a = k;
            break;
        end
    end
end