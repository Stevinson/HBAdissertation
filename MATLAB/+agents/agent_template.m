% General template for an opponent modelling agent algorithm. The template
% uses Monte-Carlo tree search for forward planning.
%
% Input:
    %   MC_plays = Number of Monte-Carlo playouts
    %   MC_depth = Depth of Monte-Carlo playouts
    %   tran = Transition function of environment
    %   prepare_workspace
    %   update_workspace
    %   opponent_strategies
    %   expected_payoffs
    %   MC_prepare_episode
    %   MC_sample_actions
%
% Output:
    %   algorithm = An agent algorithm based on this template
%%

function algorithm = agent_template(MC_plays, MC_depth, tran,prepare_workspace, update_workspace,...
                            opponent_strategies, expected_payoffs, MC_prepare_episode, MC_sample_actions) % INPUTS DELETED

    % Specify algorithm - i.e. the function below
    algorithm = @alg; 

    function [] = alg(i,m,s_pre,a_pre,r,s,t,W)
        
        if t > 1,
            % Update workspace
            W = update_workspace();

            % Update template data
            W = opponent_strategies();

            x_i = ones(1,W.m_i) / W.m_i; % ?
        else
            % Extend workspace
            extend_workspace;

            % Prepare workspace
            W = prepare_workspace();

            % Random strategy
            x_i = ones(1,W.m_i) / W.m_i;
        end


        %% Extend workspace for template
        function extend_workspace
            import tools.*
            % Monte Carlo planning
            W.MC_plays = MC_plays;
            W.MC_depth = MC_depth;
            W.tran = tran;
        end

        %% Monte Carlo Tree Search
        function mc_playouts           
            % Generate playouts
            rng_set = rng; rng(t);

            for p = 1:W.MC_plays,
                % Copy data
                s_ = s; t_ = t;

                % Prepare episode
                W_ = MC_prepare_episode(W);

                % Perform playout
                a_ = actions;

                for d = 1:W.MC_depth,
                    % State transition
                    s_pre_ = s_;

                    [s_,r_,term] = W_.tran(s_,a_);

                    % Prepare next actions
                    a_pre_ = a_;

                    W_ = opponent_strategies(s_pre_,a_pre_,r_,s_,t_,W_);
                    W_.E = expected_payoffs(s_,W_);

                    % Update Q-table
                    W_ = Q_update(s_pre_,a_pre_,r_,s_,W_);

                    % Next transition
                    if term || (r_(i) > 0), break; end

                    t_ = t_ + 1;

                    % Get next actions
                    a_ = actions;
                end

                % Store Q-table
                W.Q = W_.Q;
            end

            % Restore generator state
            rng(rng_set);


            %% Sample joint action for state s_ at time t_

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