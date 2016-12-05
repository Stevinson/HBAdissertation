% Workspace for HBA agent.
% Edward Stevinson 17/7/16
%
% Input:
%   M = Predefined models. M{k,1} contains a pointer to the algorithm of
%   model k, M{k,2} contains the workspace for the algorithm of model k.
%
%   likelihood = Likelihood function for model posteriors
%
%   Prior = prior distribution over types (summing to 1), or automatic
%   prior formulation (see code below)
%
% Output:
%   W = Workspace for HBA
%% 

function W = HBA_agent_workspace(M,likelihood,Prior)
    import tools.*
    import tree_types.*

    % If correct models are given (for experiments)
    W.givencorrect = false;
    
    % Predefined models
    W.M = M;
    % Likelihood function
    W.likelihood = likelihood;

    % Prior
    if (sum(Prior) ~= 1)
        K = 1:size(W.M,1);

        if strcmp(Prior,'UNIFORM'),
            Prior = ones(1,length(K));
        else
            switch Prior
                case 'UTILITY',
                    Y = @(p) p(1);

                case 'STACKELBERG',
                    Y = @(p) p(2);

                case 'WELFARE',
                    Y = @(p) sum(p);

                case 'FAIRNESS',
                    Y = @(p) prod(p);

                otherwise,
                    error('Unknown prior formulation.');
            end

            for k = K,
                Prior(k) = Y( tree_types.tree_br(1,t_max,[],Mod{k,2},G) );
            end
        end

        Prior = Prior(K) / sum(Prior(K));
    end

    W.Prior = Prior;
end

