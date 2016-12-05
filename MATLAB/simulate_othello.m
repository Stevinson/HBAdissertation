% Simulate game
% Edward Stevinson 15/7/16
%%

function state = simulate_othello(A,tran,state,t_max,options)
    
    import othello_scripts.*
    
    % Check options are being used
    use_options = (nargin > 4) && isstruct(options);

    %% Prepare simulation
    n = size(A,1);  % number of agents
    I = 1:n;        
    r = zeros(1,n); % reward
    a = cell(1,2);
    %s_pre = s;
    Pay = zeros(t_max+1,n); %  Pay(t,i) is payoff to player i at time t
    % problem here is the number of actions changes each time step!!
    Prf = cell(1,n); % Prf{i}(t,:) is mixed strategy of player i at time t

    % Fill the empty payoff matrices
    for (j = 1:2)
        Prf{j} = zeros(t_max+1,2);
    end

    %% Perform simulation
    for t = 1:t_max,
      
        % Print the iteration number
        fprintf('%i ',t);
        
        % If options are being used then plot the state
        if (use_options)
            options.plot(state);
             pause(0.05); % Pause for ease watching
        end

        % Collect actions player whose turn it is        
        actions(state.turn);
        
        % Save action
        action = Prf{state.turn}(t,:);
        
        % Use actions to transition board, notify if reached end of the game (also changes the turn variable)
        [state,r,game_end] = transition(state,action);

        % Update the main payoff matrix
        Pay(t,:) = r;

%         if is_hba,
%             HBA.Pos{t} = A{1,2}.Pos;
%             %HBA.TypX{t} = A{1,2}.Typ_X;
%         end

        % Terminate simulation
        if (game_end)
            break; 
        end
        
    end

    % Plot final state
        if (use_options)
            options.plot(state);
        end

%     fprintf('\n');
% 
%     % Finalise workspaces
%     t = t + 1;
%     actions;
%     t = t - 1;
% 
%     % Return data
%     Pay = Pay(1:t,:);
% 
%     for j = I,
%         Prf{j} = Prf{j}(1:t,:);
%     end
% 
%     if is_hba,
%         HBA.Pos = HBA.Pos(1:t);
%         %HBA.TypX = HBA.TypX(1:t);
%     end


    %% Get actions from agents
    function actions(i) % can remove the i here i think?
        
        import othello_scripts.*

        i = state.turn; % i is the player whose turn it is 
        j = state.opponent;
        
        %j = state.opponent;
        
        a_pre = a; % store previous actions
            
        %for i = 1:2
            % Get strategy, all possible moves, and workspace
            [Prf{i}(t,:), possibleMoves, A{i,2}] = A{i,1}(i, r, state, t, A{i,2}, a_pre);
        %end
        a{i} = Prf{i}(t,:);
        a{j} = [99 99];
%         % Does a players workspace change when it is the other player's turn?
%         Prf{j}(t,:) = [99 99];
        
        %% Note that unlike in the example I am storing a coordinate in Prf and not all the actions. This may need changing.
        % Sample action - a(i) = rndact(Prf{player_no}(t,:));
    end
end
