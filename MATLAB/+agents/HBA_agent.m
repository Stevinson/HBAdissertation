%%
% Function for ...
% Input:
%   real_strat = Exploration strategy for real actions
%   plan_strat = Exploration strategy for planning procedure
%   MC_plays = Number of Monte-Carlo playouts
%   MC_depth = Depth of Monte-Carlo playouts
%   tran = Transition function of environment
% Output:
%   alg = HBA algorithm
% Edward Stevinson 17/7/16
%%


function algorithm = HBA_agent(MC_plays,MC_depth,tran)
    
    
    % Use template.m to create these inputs
    algorithm = othello_scripts.myTemplate(MC_plays,MC_depth,tran,@prepare_workspace,...
        @update_workspace,@opponent_strategies,@expected_payoffs,@MC_prepare_episode,@MC_sample_actions);

    % On first run of HBA agent, this function is used to prepare the workspace.
    function W = prepare_workspace(i,r,s,t,W)
        
        import othello_scripts.*
        
        % Number of agents playing the game
        W.n = 2;
        
        % Predefined models - k is number of these models
        W.k = size(W.M,1);

        % Separate the info about the types for use in this function.
        if (W.k > 0)
            W.MA = W.M(:,1); % W.MA is the handle for the type
            W.MW = cell(W.k,W.n-1); % W.MW is the type workspace
            for j = 1:W.n-1,
                W.MW(:,j) = W.M(:,2);
            end
            W.model = zeros(1,W.n-1); % ??
        end

        if (W.k == 0)
            error('Must use at least one type provided.');
        end

        % Model posteriors (NB. W.Prior created in HBA_workspace)
        W.Pos = repmat(W.Prior,1,1);

        % Probability history
        if W.k > 1,
            W.H = zeros(W.k,0);
        end
        % Temporarily ignore as I don't know what it does
        % Model (counter) profiles
        W.cPrfM = counterProfiles(i,ones(1,W.n)*W.k);
               
        % Action (counter) profiles
        cPrfA = counterProfiles(i,m); cPrfA_ind = cell(1,W.m_i);
                    
        z = size(cPrfA,1); L = 1:z;
                    
        for k = 1:W.m_i,
            cprf_ind_k = zeros(z,1);
                    
            for l = L,
                cprf = cPrfA{l,2}; cprf(i) = k;
                    
                cprf_ind_k(l) = crd2ind(cprf,m);
            end
                    
            cPrfA_ind{k} = cprf_ind_k;
         end
                    
         W.cPrfA = cPrfA; W.cPrfA_ind = cPrfA_ind;

         %Compute model strategies
         W = opponent_strategies(a_pre,r,s,t,W);
    end

    
    
    %% Each iteration update the history and posteriors
    function W = update_workspace(i,r,s,t,W,a_pre)
        
        K = 1:W.k; % Indices to each type

        
        if (~W.givencorrect) && (W.k > 1)
            
            % Extend probability history
            h = size(W.H,2)+1; % h is the number of history steps used in HBA

            ind = 1; j_ = 1;

            for j = W.J % W.J is the opposition player ID
                
                a_j = a_pre(j); % Opposition previous action

                for k = K % for each of the types
                    
                    % Build up the action history
                    W.H(ind,h) = W.Str{k,j_}(a_j);

                    ind = ind + 1;
                end

                j_ = j_ + 1;
            end

            % Update model posteriors
            L = W.likelihood(W.H);

            k = K(end); j_ = 1;

            for j = W.J,
                ind = (j_-1) * k;

                L_j = L(ind+1:ind+k)' .* W.Prior;

                z = sum(L_j);

                if z > 0,
                    W.Pos(j_,:) = L_j / z;
                else
                    W.Pos(j_,:) = 0;
                end

                j_ = j_ + 1;
            end
        end
    end

    %% Get opponent strategies
    function W = opponent_strategies(s_pre,a_pre,r,s,t,W)
        
        % Predefined models
        Str = cell(W.k,W.n-1);
        % If there is a predefined model...
        if W.k > 0,
            % Iterate over each one...
            for k = 1:W.k,
                j_ = 1;
                for (j = W.J) % nb. W.J = [1:(i-1),(i+1):W.n] i.e. opponent ID (NB. n = number of actor)
                    
                    [Str{k,j_},W.MW{k,j_}] = W.MA{k}(j,W.m,s_pre,a_pre,r,s,t,W.MW{k,j_}); % W.MA is a type handle

                    j_ = j_ + 1;
                end
            end
        end

        W.Str = Str;
    end
    
    
    
    %% Expected payoffs for a state and workspace
    function E = expected_payoffs(s,W)
        
        % Work out how (and for when/ whom) it calculates expected payoffs
        
        % Query Q-table
        % Qs = W.Q.get(s.v);

        if isempty(Qs) || all(Qs < 0.000001),
            % Uniform strategy
            E = zeros(1,W.m_i);
        else
            % Action/Model profiles
            cPrfA = W.cPrfA; L_A = 1:size(cPrfA,1);
            cPrfM = W.cPrfM; L_M = 1:size(cPrfM,1);

            Pos = W.Pos; Str = W.Str;

            phi = zeros(1,L_A(end));

            % All counter actions
            for l_a = L_A,
                cprf_a = cPrfA{l_a,2};

                % All counter models
                sum_m = 0;

                for l_m = L_M,
                    cprf_m = cPrfM{l_m,2};

                    % All other agents
                    prb = 1; j_ = 1;

                    for j = W.J,
                        m_j = cprf_m(j); % Model
                        a_j = cprf_a(j); % Action

                        % Strategy of model m_j for agent j
                        str = Str{m_j,j_};

                        % Model/Action probability
                        prb = prb * Pos(j_,m_j) * str(a_j);

                        j_ = j_ + 1;
                    end

                    sum_m = sum_m + prb;
                end

                phi(l_a) = sum_m;
            end

            % Expected action values
            E = zeros(1,W.m_i);

            for k = 1:W.m_i,
                E(k) = phi * Qs(W.cPrfA_ind{k});
            end
        end
    end

    %% Prepare episode for MCTS
    function W = MC_prepare_episode(W)
       
        % Choose type according to beliefs over opponent's type
        W.model = tools.randomAction(W.Pos(1,:));
        
    end

    %% Sample actions for MCTS
    function a = MC_sample_actions(a_i,W)
        
        a = 0;

        a = tools.rndact(W.Str{W.model(1),1});

    end

end


