% Transition function
% Edward Stevinson 17/7/16
% Input:
%   s = State
%   a = Joint action
%
% Output:
%   s_ = Successor state
%   r = Joint reward
%   term = 1 iff. s_ is a terminal state
%%

function [board, reward, termination, score] = transition(state, action)

    import othello_scripts.*
    
    % Initialise
    board = state;
    turn = state.turn;

    % If there is a best move, make it
    
    if (action(1,1) ~= 99)
        xstart = action(1,1); ystart = action(1,2);
        [bool, board] = makeMove(state, turn, xstart, ystart);
    end

    
%     [bool, tilesToFlip] = isValidMove(state, turn, xstart, ystart);
%  
%     if bool == true
%  
%         % Place piece on board
%         tile = state.positions(xstart, ystart);
%     
%         % Now flip pieces affected by this move
%         for i = 1:size(tilesToFlip,1)
%             state.positions(x,y) = tile;
%         end
%     
%         % Get the score after the transition
%         score = getScore(state);
%         
%     end

    
    % Change whose turn it is
    if (board.turn==1)
        board.turn = 2;
        board.opponent = 1;
    else
        board.turn = 1;
        board.opponent = 2;
    end
    
    turn = board.turn;
    
    moves = getValidMoves(board, turn);
    score = getScore(board);
    % End game if opponent has no valid move
    if (isempty(moves)) && (action(1,1) == 99)
        termination = true; %% change this to state.end = true i.e. its a property of the state 'class' % Add state.winner variable
        if (score(1,1) > score(1,2))
            % Black has won
            reward = [1,0];
        elseif (score(1,1) < score(1,2))
            reward = [0,1];
        else 
            % Draw
            reward = [0,0];
        end  
        return
    end
    % If the game is not over...
    termination = false;
    reward = [0, 0];
end

    
    
    
    
    
 