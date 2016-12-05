% General template for an opponent modelling agent algorithm. The template
% uses Monte-Carlo tree search for forward planning.
%
%%

function algorithm = myTemplate(MC_plays,MC_depth,transition,prepare_workspace,update_workspace,opponent_strategies,...
                        expected_payoffs,MC_prepare_episode,MC_sample_actions)

    % Specify algorithm
    algorithm = @alg;
    
    % Output mixed strategy and updated workspace
    function [x_i,possibleMoves, W] = alg(i,r,s,t,W,a_pre)
        
        % Temporary
        possibleMoves = getValidMoves(s,i);
        
        %% Temporary fix making t>2 to make HBA act second. fix!!! 
        if t > 2,
            
            % Update workspace
            W = update_workspace(i,r,s,t,W,a_pre);

            % Update template data
            W = opponent_strategies(s_pre,a_pre,r,s,t,W);

            W.E = expected_payoffs(s,W);
            W = Q_update(s_pre,a_pre,r,s,W);

            % Monte Carlo planning
            % mc_playouts;
            %x_i = monteCarlo();

            % Compute strategy
            %x_i = real_strat(expected_payoffs(s,W),t);
            %x_i = ones(1,W.m_i) / W.m_i;
            
        % If on the first iteration    
        else
            % Extend workspace
            extend_workspace;

            % Prepare workspace (NB. removed s_pre and a_pre: these may need to be put back in)
            W = prepare_workspace(i,r,s,t,W);

            % Random strategy
            m = size(possibleMoves,1);
            j = randi([1 m]);
            x_i = possibleMoves(j,:);
        end


        %% Add extra information the agent's workspace
        function extend_workspace
            
            import othello_scripts.*

            % Monte Carlo planning
            W.MC_plays = MC_plays;
            % Continue playout until end of game
            % W.MC_depth = MC_depth;
            W.transition = transition;
            
            % Useful variables
            %W.n = length(m);
            %W.m = m; W.m_i = m(i);
            W.J = [1:(i-1),(i+1):2]; %% Working in this line
        end


        %% Monte Carlo Tree Search 
        function mc_playouts
            
            % Generate playouts
            rng_set = rng; rng(t); % Initialise random number generator

            for play_id = 1:W.MC_plays
                
                % Copy data
                s_ = s; % temp state
                t_ = t; % temp time step

                % Randomly select opponent type according to beliefs
                W_ = MC_prepare_episode(W);

                % Perform playout
                a_ = actions;

                % Change instead to traverse until the game ends - while(~endGame)
                for d = 1:W.MC_depth
                    
                    % At the moment not using UCT
                    
                    % State transition
                    s_pre_ = s_;

                    [s_,r_,term] = W_.transition(s_,a_);

                    % Prepare next actions
                    a_pre_ = a_;

                    W_ = opponent_strategies(s_pre_,a_pre_,r_,s_,t_,W_);
                    W_.E = expected_payoffs(s_,W_);


                    % Break if reached the end of the game
                    if (game_end) || (r_(i) > 0)
                        break;
                    end

                    t_ = t_ + 1;

                    % Get next actions
                    a_ = actions;
                
                end
            end

            % Restore generator state
            rng(rng_set);


            %%
            % Sample joint action for state s_ at time t_

            function a = actions
                % Own action
                a = zeros(1,W.n);
                a(i) = tools.rndact(plan_strat(W_.E,t_));

                % Others' actions
                a(W.J) = MC_sample_actions(a(i),W_);
            end
        end
    end
end