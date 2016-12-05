% Function which generates all possible pure counter profiles for a given
% player i
%
% Input:
%   i: player id to be countered
%   m: m(i) = number of actions for player i
%
% Output:
%   P:
%       P{l,1} = absolute number of profile l
%       P{l,2} = vector of actions in profile l
%       [Note: P{l,1} = crd2ind(P{l,2},m)] 
% 
% Edward Stevinson 20/7/16
%%

function P = counterProfiles(i,m)

    %% Prepare procedure
    % Matrix containing number of actions of each player
    m_ = m;    
    % Number of players
    n = length(m); 
    % Act{i} = vector of action numbers for player i
    Act = cell(1,n);
    for j = 1:n,
        Act{j} = 1:m(j);
    end

    if i > 0, % i=0 means no player countered
        m(i) = 1;
    end
    
    % Generate profiles
    L = prod(m); % Number of counter profiles
    P = cell(L,2);

    p = ones(1,n);
    crd = p;

    J = 1:n;

    for l = 1:L, % For each counter profile
        for j = J,
            crd(j) = Act{j}(p(j));
        end

        P{l,1} = crd2ind(crd,m_); % Pure profile number
        P{l,2} = crd;

        for j = J,
            if (p(j) < m(j)) && all(p(j+1:n) == m(j+1:n)),
                p(j) = p(j)+1;
                p(j+1:n) = 1;
                break;
            end
        end
    end
end